from bugle_project.bugle.models import Blast
from django import forms

class BlastForm(forms.ModelForm):
    class Meta:
        model = Blast
        fields = ('message', 'extended', 'attachment', 'in_reply_to')

