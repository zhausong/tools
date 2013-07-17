from appengine_django.models import BaseModel
from google.appengine.ext import db

class BlogPost(BaseModel):
    title = db.StringProperty()
    body = db.StringProperty()
    timestamp = db.DateTimeProperty()
    class Admin:
        list_display = ('title', 'timestamp',)
    class Meta:
        ordering = ('-timestamp',)
