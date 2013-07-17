from django.conf.urls.defaults import *
from mysite.blog.views import archive

urlpatterns = patterns('',
    (r'^$', archive),
)
