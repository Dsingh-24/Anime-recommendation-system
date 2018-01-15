from django.shortcuts import render, get_object_or_404,get_list_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import Permission, User
from django.views import generic
from django.views.generic import View
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .forms import UserForm
from .models import Anime,Genre,Like
import numpy
import random
from sklearn.naive_bayes import GaussianNB

def homepage(request):
    return render(request, 'westros/homepage.html')
def westros(request):
    if not request.user.is_authenticated():
        return render(request, 'westros/login.html')
    else:
        anime = Anime.objects.all()[:12]
        return render(request, 'westros/westros.html', {'anime': anime})
    return render(request, 'westros/westros.html')
def detail(request, anime_id):
    if not request.user.is_authenticated():
        return render(request, 'westros/login.html')
    else:
        anime = get_object_or_404(Anime, pk=anime_id)
        g=[]
        for i in anime.genres.all():
            g.append(i)
        return render(request, 'westros/detail.html', {'anime': anime,'g':g})
def like(request, anime_id, l_id):
    a=Like()
    if int(l_id)==0 or int(l_id)==1:
        if not request.user.is_authenticated():
            return render(request, 'westros/login.html')
        else:
            a.l=int(l_id)
            a.anime=Anime.objects.get(id=int(anime_id))
            a.user=request.user
            try:
                try:
                    q=Like.objects.get(user=a.user,anime=a.anime)
                    print(q)
                    q.delete()
                    a.save()
                    return detail(request,anime_id)
                except DoesNotExist:
                    a.save()
                    return detail(request,anime_id)
            except NameError:
                a.save()
                return detail(request,anime_id)
    return detail(request,anime_id)
def favanime(request):
    if not request.user.is_authenticated():
        return render(request, 'westros/login.html')
    else:
        fa=[]
        naf=[]
        a=get_list_or_404(Like,user=request.user)
        for i in a:
            if i.l == 1:
               fa.append(i.anime)
            else:
                naf.append(i.anime)
        print(len(fa))
        return render(request,'westros/favanime.html',{'fa':fa,'naf':naf})

def explore(request):
    if not request.user.is_authenticated():
        return render(request,'westros/login.html')
    else:
        animes = Anime.objects.all()[:11520]
        paginator = Paginator(animes,96)
        page=request.GET.get('page')
        try:
            anime = paginator.page(page)
        except PageNotAnInteger:
            anime = paginator.page(1)
        except EmptyPage:
            anime = paginator.page(paginator.num_pages)     
        return render(request,'westros/explore.html',{'anime':anime})


def about_us(request):
    return render(request,'westros/about_us.html')
def tc(request):
    return render(request, 'westros/term-&-conditions.html')
def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'westros/login.html', context)
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                anime = Anime.objects.all()[:12]
                return render(request, 'westros/westros.html', {'anime': anime})
            else:
                return render(request, 'westros/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'westros/login.html', {'error_message': 'Invalid login'})
    return render(request, 'westros/login.html')
def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email_id =  form.cleaned_data['email']
        user.set_password(password)
        user.save()
        subject = "welcome mail"
        messages = "hi "+username+" welcome to Westros"
        from_email = settings.EMAIL_HOST_USER
        to_list = [ email_id , settings.EMAIL_HOST_USER ]
        send_mail(subject , messages, from_email,to_list,fail_silently = True)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                anime = Anime.objects.all()[:12]
                return render(request, 'westros/westros.html', {'anime': anime})
    context = {
        "form": form,
    }
    return render(request, 'westros/register.html', context)

def search(request):
    req=str(request.POST['query']).lower()
    anime_list=[]
    if len(req):
        for i in Anime.objects.all():
            if i.name.lower().find(req)>=0:
                anime_list.append(i)
            if i.tag.lower().find(req)>=0:
                anime_list.append(i)
            for j in i.genres.all():
                if j.Name.lower().find(req)>=0:
                    anime_list.append(i)
                    break                   
        return render(request, 'westros/search.html',{'anime':anime_list})


def recommendations(request):
    if not request.user.is_authenticated():
        return render(request,'westros/login.html')
    else:
        x=[]
        Y=[]
        a=get_list_or_404(Like,user=request.user)
        for i in a:
            x.append(i.anime)
            Y.append(i.l)
        x1=[]
        for i in x:
            try:
                x1.append(i.getData())
            except:
                continue
        X=[]
        for i in x1:
            t=numpy.asarray(i,dtype=float)
            X.append(t)
        Y=numpy.asarray(Y,dtype=float)
        c = GaussianNB()
        c.fit(X, Y)
        T=[]
        t=[]
        for i in Anime.objects.all()[:1100]:
            if i not in x:
                try:
                    T.append(numpy.asarray(i.getData()))
                    t.append(i)
                except:
                    continue
        L=c.predict(T)
        li=[]
        print(len(T))
        for i in range(len(T)):
            if L[i]==1:
                li.append(t[i])
        print (len([i for i in L if i ==0]))
        random.shuffle(li)
        li.reverse()
        return render(request, 'westros/recommendations.html', { 'li': li[:18]})