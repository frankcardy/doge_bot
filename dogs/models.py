from django.db import models
from .doge_scraper import get_postings, extract_dog


# Create your models here.
class Dog(models.Model):
    name = models.CharField(max_length=220, blank=True)
    url = models.URLField()
    breed = models.CharField(max_length=220, blank=True)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=220, blank=True)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        name, price = extract_dog(self.url)
        super(Dog, self).save(*args, **kwargs)
