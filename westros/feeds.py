from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from westros.models import Anime


class LatestAnimeFeed(Feed):
	title = 'Westros'
	link = "//"
	description = "Updates"

	def items(self):
		return Anime.objects.order_by('-pk')[:10]

	def item_title(self, item):
		return Anime.tag

	def item_description(self, item):
		return Anime.epidodes

	def item_link(self, item):
		return reverse('westros:detail',kwargs={'anime_id':item.pk})