from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .models import Profile, Skill


def login_user(request):
    page = 'register'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except Exception:
            messages.error(request, 'Пользователь не найден')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Логин или пароль не верный')

    return render(request, 'users/login_register.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, 'Успешно вышли из аккаунта')
    return redirect('login_user')


def register_user(request):
    form = CustomUserCreationForm()
    page = 'register_user'

    if request.POST:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, f'Пользователь {user.username} успешно добавлен!')
            login(request, user)
            return redirect('edit_account')
        else:
            messages.error(request, 'Ошибка во время регистрации!')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
    )

    page = request.GET.get('page')
    results = 3
    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    left_index = 1 if (int(page) - 4) < 1 else (int(page) - 4)
    right_index = (int(page) + 5) if (int(page) + 5) < paginator.num_pages else paginator.num_pages + 1
    custom_range = range(left_index, right_index)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'paginator': paginator,
        'custom_range': custom_range,
    }
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact='')
    other_skills = profile.skill_set.filter(description='')
    context = {
        'user_profile': profile,
        'top_skills': top_skills,
        'other_skills': other_skills,
    }
    return render(request, 'users/user_profile.html', context)


@login_required(login_url='login_user')
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login_user')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_account')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login_user')
def create_skill(request):
    form = SkillForm()
    profile = request.user.profile
    if request.POST:
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Навык успешно добавлен!')
            return redirect('user_account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login_user')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.POST:
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill.save()
            messages.success(request, 'Навык успешно обновлен!')
            return redirect('user_account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login_user')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.POST:
        skill.delete()
        messages.success(request, 'Навык успешно удален!')
        return redirect('user_account')
    context = {'object': skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login_user')
def inbox(request):
    profile = request.user.profile
    message_requests = profile.messages.all()
    unread_messages = message_requests.filter(is_read=False).count()
    context = {
        'message_requests': message_requests,
        'unread_messages': unread_messages,
    }
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login_user')
def message_view(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if not message.is_read:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Сообщение отправлено')
            return redirect('user_profile', pk=recipient.id)
    context = {
        'recipient': recipient,
        'form': form,
    }
    return render(request, 'users/message_form.html', context)
