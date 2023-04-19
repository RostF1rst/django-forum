import random
import requests
from faker import Faker
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views.generic import UpdateView, CreateView, DetailView, ListView
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, reverse, redirect

from . import models, forms


class ShowPostView(DetailView):
    template_name = 'posts/showpost.html'
    model = models.Post


class PostListView(ListView):
    template_name = 'posts/posts.html'
    model = models.Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter')
        return context

    def get_queryset(self):
        filter_value = self.request.GET.get('filter') or ''
        new_context = models.Post.objects.filter(title__contains=filter_value).order_by('-publication_date')
        return new_context


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
        return HttpResponseForbidden(request)


def leave_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(models.Post, pk=post_id)
        author = request.user
        content = request.POST.get('content')
        new_comment = models.Comment(related_post=post, author=author, content=content)
        new_comment.save()
    return HttpResponseRedirect(reverse('block0:show_post', args=[post_id]))


def create_fake_posts(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden(request)

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

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        post = self.get_object()
        if not user == post.author:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CreatePostView(LoginRequiredMixin, CreateView):
    model = models.Post
    template_name = 'posts/editpost.html'
    form_class = forms.EditPostForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('block0:show_post', args=(self.object.id,))
