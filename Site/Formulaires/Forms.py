from dataclasses import fields
from pyexpat import model
from django import forms
from Site.models import *

class ModelTargetSiteForm(forms.ModelForm):
    name = forms.CharField(max_length=70, 
        widget= forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ) 
    )
    
    url_to_scrapp = forms.CharField(max_length=70, 
        widget= forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Target_Site
        fields = ['name', 'url_to_scrapp']


class TargetSiteForm(forms.Form):
    name = forms.CharField(max_length=70, 
        widget= forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ) 
    )
    
    url_to_scrapp = forms.CharField(max_length=70, 
        widget= forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


class ModelThreadForm(forms.ModelForm):
    target_id = models.ForeignKey(Target_Site, on_delete=models.CASCADE)
    title     = forms.CharField(max_length=70,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    number_of_replys = forms.CharField(max_length=10,
        widget=forms.NumberInput()
    )
    author = forms.CharField(max_length=70,
        widget=forms.TextInput(attrs={
            'class': 'control-form'
        })
    )
    publication_date = forms.DateTimeInput(attrs={
        'class': 'form-control'
    })
    content = forms.Textarea()
    scrapped_date = forms.DateTimeInput(attrs={
        'class': 'form-control'
    })


    class Meta:
        model = Threads
        fields = ['target_id', 'title', 'number_of_replys', 'author', 'publication_date', 'content', 'scrapped_date']