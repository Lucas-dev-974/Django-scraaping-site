from django.db import models


class Target_Site(models.Model):
    name     = models.CharField(max_length=75, unique=True)
    url_to_scrapp = models.URLField(max_length=100) 


class Threads(models.Model):
    target_id = models.ForeignKey(Target_Site, on_delete=models.CASCADE)
    title     = models.CharField(max_length=100)
    author    = models.CharField(max_length=75)
    content   = models.TextField()
    publication_date = models.DateTimeField()
    scrapped_date    = models.DateTimeField()
    number_of_replys = models.IntegerField()

    def replys(self):
        replys = Threads_Replys.objects.filter(thread_id = self.id)
        return replys

    # def getBetweenDate(self, date1 = None, date2 = None):
    #     threads = Threads.objects.raw('SELECT * FROM "Site_threads" WHERE publication_date BETWEEN ' + str(date1) + ' AND ' + str(date2)).all()
    #     return threads

class Threads_Replys(models.Model):
    thread  = models.ForeignKey(Threads, on_delete=models.CASCADE)
    author  = models.CharField(max_length=75)
    content = models.TextField()
    publication_date = models.DateTimeField()
    scrapped_date    = models.DateTimeField()


def getThreadsBetweenDate(date1 = None, date2 = None):
    threads = Threads.objects.raw('SELECT * FROM "Site_threads" WHERE publication_date BETWEEN %s AND %s', [date1, date2])
    return threads

def getNumberOfThreadForDate(date):
    threads = Threads.objects.raw('SELECT COUNT(*) FROM "Site_threads" WHERE SUBSTR(publication_date, 1, 7) = %s', [date])