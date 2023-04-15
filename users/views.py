from faker import Faker
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
import block0.models

app_name = "users"


def user_page(request, user_id):
    requested_user = get_object_or_404(User, pk=user_id)
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
