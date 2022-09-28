from datetime import date
from django.db import models
import pandas as pd

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

def getNumberOfThreadForDate(year, month):
    # threads = Threads.objects.raw('SELECT * FROM "Site_threads" WHERE SUBSTR(publication_date, 1, 7) = %s', [date]).columns.count(1)
    threads = Threads.objects.filter(publication_date__year = year, publication_date__month = month)
    return threads

def getTotalScrapByMonthBetweenDate(date1 = None, date2 = None):
    threads = Threads.objects.raw('SELECT * FROM "Site_threads" WHERE publication_date BETWEEN %s AND %s', [date1, date2])
    

    dateFormat1 = date(*map(int, date1.split('-')))
    dateFormat2 = date(*map(int, date2.split('-')))

    oldestDate = min([dateFormat1, dateFormat2])
    month_list = [i.strftime("%b:%Y-%m") for i in pd.date_range(start=date1, end=date2, freq='MS')]
    print(month_list)
    months = {}

    for data_date in month_list:
        month_str   = data_date.split(':')[0]
        digit_YearMonth = data_date.split(':')[1].split('-')

        year  = digit_YearMonth[0]
        month = digit_YearMonth[1]
        
        
        scrapped_thread_nu = getNumberOfThreadForDate(year, month).count()

        months[month_str] = {
            'total_scrapped_threads': scrapped_thread_nu
        }


    return months

