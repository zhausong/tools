from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed
from blog.views import archive
from blog.feeds import RSSFeed

urlpatterns = patterns('',
    url(r'^$', archive),
    url(r'^feeds/(?P<url>.*)/$', feed, {'feed_dict': {'rss': RSSFeed}}),
)
