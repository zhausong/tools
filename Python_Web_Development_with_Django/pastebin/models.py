import datetime
from django.db import models
from django.db.models import permalink
from django.contrib import admin

class Paste(models.Model):
    """A single pastebin item"""
    
    SYNTAX_CHOICES = (
        (0, "Plain"), 
        (1, "Python"), 
        (2, "HTML"), 
        (3, "SQL"), 
        (4, "Javascript"),
        (5, "CSS"),
        )

    content = models.TextField()
    title = models.CharField(blank=True, max_length=30)
    syntax = models.IntegerField(max_length=30, choices=SYNTAX_CHOICES, default=0)
    poster = models.CharField(blank=True, max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
        
    class Meta:
        ordering = ('-timestamp',)
        
    def __unicode__(self):
        return "%s (%s)" % (self.title or "#%s" % self.id, self.get_syntax_display()) 

    @permalink
    def get_absolute_url(self):
        return ('django.views.generic.list_detail.object_detail', 
            None, {'object_id': self.id})

class PasteAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'title', 'poster', 'syntax', 'timestamp')
    list_filter = ('timestamp', 'syntax')

admin.site.register(Paste, PasteAdmin)
