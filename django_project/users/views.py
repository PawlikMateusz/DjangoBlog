from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
# Create your views here.


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'
    success_message = "Now you are registered, try to log in!"

# Profile view - hard way
# class UserDetailView(LoginRequiredMixin, ListView):
#     login_url = "login"
#     template_name = 'users/user_detail.html'

#     def get_queryset(self):
#         queryset = [User.objects.filter(pk=self.request.user.pk).first()]
#         return queryset


class UserDetailView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = 'users/user_detail.html'
