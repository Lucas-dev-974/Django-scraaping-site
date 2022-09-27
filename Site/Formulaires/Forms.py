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

    # Overide
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Manage custom error here
        self.fields['url_to_scrapp'].error_messages['invalid'] = "Veuillez entrer une URL valide !"
        self.fields['name'].error_messages['unique'] = "Un site cible à déjà ce nom, veuillez en saisir un autre !"

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
        widget= forms.URLInput(
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