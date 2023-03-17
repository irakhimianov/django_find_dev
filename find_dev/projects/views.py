from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import ProjectForm, ReviewForm
from .models import Project, Tag


def projects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )

    page = request.GET.get('page')
    results = 3
    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
    left_index = 1 if (int(page) - 4) < 1 else (int(page) - 4)
    right_index = (int(page) + 5) if (int(page) + 5) < paginator.num_pages else paginator.num_pages + 1
    custom_range = range(left_index, right_index)

    context = {
        'projects': projects,
        'search_query': search_query,
        'paginator': paginator,
        'custom_range': custom_range,
    }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    form = ReviewForm()
    project = Project.objects.get(id=pk)
    context = {
        'project': project,
        'form': form,
    }
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        project.vote_count
        messages.success(request, 'Отзыв добавлен!')
        return redirect('project', pk=project.id)

    return render(request, 'projects/project.html', context)


@login_required(login_url='login_user')
def create_project(request):
    form = ProjectForm()
    profile = request.user.profile
    if request.POST:
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('user_account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login_user')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('user_account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login_user')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('user_account')
    context = {'object': project}
    return render(request, 'delete_template.html', context)
