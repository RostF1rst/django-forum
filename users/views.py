from django.urls import reverse
from faker import Faker
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
import block0.models
from . import forms
from .forms import RegistrationForm

app_name = "users"


def user_page(request, pk):
    requested_user = get_object_or_404(User, pk=pk)
    posts = block0.models.Post.objects.filter(author__exact=requested_user).order_by('-publication_date')
    return render(request=request, template_name='registration/userpage.html',
                  context={'requested_user': requested_user, 'posts': posts})


def create_fake_user(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden(request)

    f = Faker('ru_RU')
    for i in range(3):
        p = f.profile()
        passwd = f.password()
        print(passwd)
        User.objects.create(
            username=p['username'],
            email=p['mail'],
            password=passwd
        )
    return redirect('/')


def settings(request):
    if request.method == 'POST':
        form = forms.AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['avatar']
            request.user.profile.avatar = file
            request.user.profile.save()
        return redirect(reverse('users:settings'))
    form = forms.AvatarForm()
    return render(request=request, template_name='registration/settings.html', context={'form': form})


class UserRegistrationView(CreateView):
    template_name = 'registration/register.html'
    model = User
    form_class = RegistrationForm

    def get_success_url(self):
        return reverse('login')
