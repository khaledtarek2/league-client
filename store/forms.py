from django import forms
from .models import Item


class ItemForm(forms.ModelForm):  # input for a mutation
    class Meta:
        model = Item
        fields = ("id", "name", "stats", "passive", "active", "category")
