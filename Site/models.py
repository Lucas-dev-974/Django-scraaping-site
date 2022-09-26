from django.db import models


class Target_Site(models.Model):
    name     = models.CharField(max_length=75)
    url_to_scrapp = models.CharField(max_length=100)


class Threads(models.Model):
    target_id = models.ForeignKey(Target_Site, on_delete=models.CASCADE)
    title     = models.CharField(max_length=100)
    author    = models.CharField(max_length=75)
    content   = models.TextField()
    publication_date = models.DateTimeField()
    scrapped_date    = models.DateTimeField()
    number_of_replys = models.IntegerField()

class Threads_Replys(models.Model):
    thread  = models.ForeignKey(Threads, on_delete=models.CASCADE)
    title   = models.CharField(max_length=100)
    author  = models.CharField(max_length=75)
    content = models.TextField()
    publication_date = models.DateTimeField()
    scrapped_date    = models.DateTimeField()
    number_of_replys = models.IntegerField()
