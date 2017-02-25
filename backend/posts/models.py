import datetime
# For unique slug
import uuid

from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink



# Generate unique slug
def unique_slug(title):
    uniqueid = uuid.uuid1().hex[:5]                
    slug = slugify(title) + "-" + str(uniqueid)

    if not Post.objects.filter(slug=slug).exists():
        # If the slug is unique - return it
        return slug
    else:
        # If the post with this slug already exists - try again
        return unique_slug(title)


    
class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=256, default="")
    pub_date = models.DateTimeField(blank=True, null=True)
    # url = models.URLField(default="", null=True, blank=True)
    body = models.TextField(default="", null=True, blank=True)
    
    tags = models.ManyToManyField('Tag',
                                  related_name="posts",
                                  blank=True, null=True)
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

    def save(self, slug="", *args, **kwargs):
        if not self.id:
            self.pub_date = datetime.datetime.now()
            self.slug = unique_slug(self.title)

        return super(Post, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('view_post', None, {'slug': self.slug })

    class Meta:
        ordering = ('-pub_date',)



class Tag(models.Model):
    title = models.CharField(max_length=64)    
    slug = models.SlugField(max_length=64, default="")
    description = models.TextField(max_length=512, blank=True)

    parent = models.ForeignKey('Tag',
                               on_delete=models.CASCADE,                                  
                               related_name="children",default=None, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

        
    @permalink
    def get_absolute_url(self):
        return ('view_tag', None, {'slug': self.slug })
