from django import forms

class AddSharingForm(forms.Form):
    sharingid=forms.CharField(widget=forms.HiddenInput(),required=False)
    title=forms.CharField(max_length=30,required=False)
    file=forms.FileField(required=False)
    content= forms.CharField(widget=forms.Textarea,required=False)
    tags=forms.CharField(required=False)
    