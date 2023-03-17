from django.forms import ModelForm
from django import forms

from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('id', 'created_at', 'owner', 'vote_total', 'vote_ratio')
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'featured_image': 'Пример работы',
            'demo_link': 'Ссылка на проект',
            'source_link': 'Ссылка на исходный код',
            'tags': 'Тэги',
        }
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('value', 'body')
        labels = {
            'value': 'оцените проект',
            'body': 'добавить комментарий',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
