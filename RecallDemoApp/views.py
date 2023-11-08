import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Bot,TranscriptMessage
from .forms import CreateBotForm
from django.conf import settings
import json

# Create your views here.

# main page
def main(request):
  template = loader.get_template("main.html")
  return HttpResponse(template.render())

# page that lists all bots created by this access token
def allbots(request):
  # make an API call to pull updated bot data
  url = "https://api.recall.ai/api/v1/bot/"
  api_key = settings.RECALL_API_KEY
  headers = {
    "accept": "application/json",
    "Authorization": settings.RECALL_API_KEY
  }
  botlist = requests.get(url, headers=headers)
  # convert the api call result to json for parsing
  botsjson = botlist.json()
  # parse the json into individual bot details and put that into a database
  for x in botsjson["results"]:
    BotID=x["id"] # BotID is the primary key
    if not type(x["meeting_metadata"]) is dict: #meeting_metadata is a dictionary within the json. if the data is missing, fill the field with a placeholder
      MeetingTitle="Unknown Meeting Title"
    else:
       MeetingTitle=x["meeting_metadata"]["title"]
    if x["video_url"]: # if there is a video URL, link to it, otherwise send to a no video page.
      VideoURL=x["video_url"]
    else:
      VideoURL="novideo"
    RetentionEnd=x["media_retention_end"]
    CreateTime=x["status_changes"][0]["created_at"] # note: this created at time is for the bot, not the meeting, so it may differ from the meeting start time.
    bot=Bot(BotID,MeetingTitle,VideoURL,RetentionEnd,CreateTime) # build out the data object to be saved.
    bot.save() # save field values

  # pull a list of all bot data from the database
  botslist = Bot.objects.all().values()
  # load template
  template = loader.get_template("allbots.html")
  # build up context data
  context = {
    'botslist': botslist,
  }
  return HttpResponse(template.render(context, request))

def details(request, BotID):
  # pull bot details from the DB
  botdetails = Bot.objects.get(BotID=BotID)
  # load the page template
  template = loader.get_template("details.html")
  # prepate data to be passed to the template
  context = {
    'botdetails': botdetails,
  }
  return HttpResponse(template.render(context, request))


def createbot(request):
    # load template
    template = loader.get_template("createbot.html")
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # build out API call
        url = "https://api.recall.ai/api/v1/bot/"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": settings.RECALL_API_KEY
        }

        # create a form instance and populate it with data from the request:
        form = CreateBotForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            payload = {
                "bot_name": "Meeting Recorder",
                "meeting_url": form.cleaned_data["meetingurl"],
                "transcription_options": {
                  "provider": "assembly_ai"
                }
            }
            response = requests.post(url, json=payload, headers=headers)
            # Back to the home page:
            return HttpResponseRedirect("")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateBotForm()
    context = {
      'form': form,
    }
    return HttpResponse(template.render(context, request))

# basic no video found page
def novideo(request):
    template = loader.get_template("novideo.html")
    return HttpResponse(template.render())

# conversation transcription view
def transcription(request, BotID):
    # load template
    template = loader.get_template("transcription.html")
    # build out API call
    url = "https://api.recall.ai/api/v1/bot/"+str(BotID)+"/transcript/"
    headers = {
        "accept": "application/json",
        "Authorization": settings.RECALL_API_KEY
    }
    # make the call
    response = requests.get(url, headers=headers)
    transcript = response.json()
    BotNum = BotID
    for x in transcript:
        Speaker = x["speaker"]
        Message = ""
        TimeStamp = x["words"][0]["start_timestamp"]
        for y in x["words"]:
          Message += y["text"] + " "
        pk = str(BotNum)+str(TimeStamp)+Speaker
        entry = TranscriptMessage(pk, BotNum, Speaker, TimeStamp, Message)
        entry.save()
    
    transcription = TranscriptMessage.objects.filter(BotNum=BotNum).order_by('TimeStamp').values()

    context = {
      'transcription': transcription,
    }
    
    
   
    return HttpResponse(template.render(context,request))

