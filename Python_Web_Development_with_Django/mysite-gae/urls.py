from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^blog/', include('mysite.blog.urls')),
    (r'^admin/', include('django.contrib.admin.urls')),
)
