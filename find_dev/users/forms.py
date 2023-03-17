from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Profile, Skill, Message


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password1', 'password2')
        labels = {
            'username': 'Логин',
            'first_name': 'Имя'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('id', 'created_at', 'user')
        labels = {
            'name': 'Имя',
            'username': 'Логин',
            'location': 'Город',
            'short_intro': 'Визитка',
            'bio': 'О себе',
            'profile_image': 'Аватарка',
            'social_github': 'Github',
            'social_twitter': 'Twitter',
            'social_linkedin': 'Linkedin',
            'social_website': 'Социальные сети',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        exclude = ('id', 'owner')
        labels = {
            'name': 'Навык',
            'description': 'Описание',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('name', 'email', 'subject', 'body')
        labels = {
            'name': 'Автор',
            'subject': 'Тема',
            'body': 'Текст сообщения',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
