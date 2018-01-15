from django.contrib.auth.models import Permission, User
from django.db import models

class Genre(models.Model):
    Name=models.CharField(max_length=100)
    n=models.IntegerField()
    def __str__(self):
        return self.Name


class Anime(models.Model):
    anime_id=models.IntegerField()
    name = models.CharField(max_length=200)
    genres=models.ManyToManyField(Genre)
    tag=models.CharField(max_length=1000)
    epidodes=models.IntegerField()
    rating=models.DecimalField(decimal_places=1,max_digits=2)
    members=models.IntegerField()
    def __str__ (self):
         return self.name+str(self.genres.all())
    def getData(self):
        return [int(self.epidodes),float(self.rating),int(self.members)]


class Like(models.Model):
    user=models.ForeignKey(User)
    anime=models.ForeignKey(Anime)
    l=models.IntegerField()
    def __str__(self):
        if self.l==1:
            return self.user.username+" likes "+self.anime.name
        return self.user.username + " dislikes " + self.anime.name         


