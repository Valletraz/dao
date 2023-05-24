from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'type',
            'title',
            'text',
            'author',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        if description is not None and len(description) < 20:
            raise ValidationError({
                "description": "Новость не может быть менее 20 символов."
            })

        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data["title"]
        if name[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return name


