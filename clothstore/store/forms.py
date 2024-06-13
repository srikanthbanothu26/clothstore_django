from .models import Shirt
from django import forms


class ShirtModelForm(forms.ModelForm):
    class Meta:
        model = Shirt
        exclude = ["created_at"]