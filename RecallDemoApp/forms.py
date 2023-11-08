from django import forms


class CreateBotForm(forms.Form):
    meetingurl = forms.URLField(label="MeetingURL", max_length=2000)

