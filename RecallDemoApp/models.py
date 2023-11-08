from django.db import models

# Create your models here.

class Bot(models.Model):
    BotID = models.CharField(max_length=255,primary_key=True)
    MeetingTitle = models.CharField(max_length=255,null=True)
    VideoURL = models.URLField(max_length=2000,null=True)
    RetentionEnd = models.DateTimeField(null=True)
    CreateTime = models.DateTimeField(null=True)
   
class TranscriptMessage(models.Model):
    ID = models.CharField(max_length=255,primary_key=True)
    BotNum = models.CharField(max_length=255)
    Speaker = models.CharField(max_length=255)
    TimeStamp = models.DecimalField(max_digits = 20,decimal_places=3)
    Message = models.CharField(max_length=9999)


