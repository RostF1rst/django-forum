import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import UpdateView
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.utils.timezone import now
from faker import Faker

from . import models, forms

import requests


def posts(request):
    list_of_posts = models.Post.objects.order_by('-publication_date')
    posts_filter = request.GET.get('search') or ''
    if posts_filter:
        list_of_posts = list(models.Post.objects.filter(title__contains=posts_filter))
    return render(request, 'posts/posts.html', {"list_of_posts": list_of_posts, 'search': posts_filter})


def show_post(request, post_id):
    try:
        post = get_object_or_404(models.Post, pk=post_id)
        return render(request, 'posts/showpost.html', {"post": post})
    except models.Post.DoesNotExist:
        return HttpResponseNotFound(request)


def create_post(request):
    if request.method == 'GET':
        return render(request=request, template_name='posts/editpost.html')
    elif request.method == 'POST':
        title = request.POST.get('title') or ''
        content = request.POST.get('content') or ''

        if title and content:
            post = models.Post(title=title, content=content, publication_date=now(), author=request.user)
            post.save()
            return HttpResponseRedirect(reverse('block0:show_post', args=[post.id]))
        else:
            error = 'Fill all the fields!'
            return render(request=request, template_name='posts/editpost.html', context={'error': error})


def edit_post(request, post_id):
    post = get_object_or_404(models.Post, pk=post_id)
    if post.author != request.user:
        return HttpResponseNotAllowed(request)
    if request.method == 'GET':
        form = forms.EditPostForm(initial={'title': post.title, 'content': post.content})
        return render(request=request, template_name='posts/editpost.html', context={'post': post, 'form': form})
    elif request.method == 'POST':
        title = request.POST.get('title') or ''
        content = request.POST.get('content') or ''

        if title and content:
            post.title = title
            post.content = content
            post.save()
            return HttpResponseRedirect(reverse('block0:show_post', args=[post.id]))
        else:
            error = 'Fill all the fields!'
            return render(request=request, template_name='posts/editpost.html', context={'post': post, 'error': error})


def exchange(request):
    json_currencies = requests.get(url='https://api.exchangerate-api.com/v4/latest/USD').json()
    currencies = json_currencies.get('rates')

    if request.method == 'GET':
        context = {
            'currencies': currencies
        }

        return render(request=request, template_name='exchange.html', context=context)

    if request.method == 'POST':
        from_amount = float(request.POST.get('from-amount'))
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to-curr')

        converted_amount = round((currencies[to_curr] / currencies[from_curr]) * float(from_amount), 2)

        context = {
            'from_curr': from_curr,
            'to_curr': to_curr,
            'from_amount': from_amount,
            'currencies': currencies,
            'converted_amount': converted_amount
        }

        return render(request=request, template_name='exchange.html', context=context)


def delete_post(request, post_id):
    post = get_object_or_404(models.Post, pk=post_id)
    if post.author == request.user:
        post.delete()
        return HttpResponseRedirect(reverse('block0:posts'))
    else:
        return HttpResponseNotAllowed(request)


def leave_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(models.Post, pk=post_id)
        author = request.user
        content = request.POST.get('content')
        new_comment = models.Comment(related_post=post, author=author, content=content)
        new_comment.save()
    return HttpResponseRedirect(reverse('block0:show_post', args=[post_id]))


def create_fake_posts(request):
    f = Faker()
    users = User.objects.all()
    for i in range(5):
        models.Post.objects.create(
            title=f.sentence(nb_words=5),
            content=f.sentence(nb_words=100),
            publication_date=f.date_time_between(),
            author=random.choice(users)
        )
    return redirect('/')


class EditPostView(LoginRequiredMixin, UpdateView):
    model = models.Post
    template_name = 'posts/editpost.html'
    form_class = forms.EditPostForm

    def get_success_url(self):
        return reverse('block0:show_post', args=(self.object.id,))

    def get_object(self, queryset=None):
        return get_object_or_404(models.Post, pk=self.kwargs['post_id'])

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        post = self.get_object()
        if not user == post.author:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
