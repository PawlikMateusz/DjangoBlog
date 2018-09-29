from django.shortcuts import render
from blog.models import Post, Comment
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, TemplateView, CreateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
# Create your views here.


class PostView(ListView):
    model = Post
    ordering = ['-date_posted']


class AboutTemplateView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = 'blog/about.html'


class CreateNewPostView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = "login"
    model = Post
    fields = ['title', 'content']
    success_message = "Post was created successfully"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm(
            initial={'post': self.object, 'author': self.request.user})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if self.request.user:
            form.save()
            messages.add_message(self.request, messages.INFO,
                                 'Comment is added succesfully')
            return super(PostDetailView, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('blog:nopermission'))


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    model = Comment

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             'The comment is deleted successfuly')
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == request.user:
            self.object.delete()
            success_url = self.get_success_url()
            messages.add_message(self.request, messages.INFO,
                                 'The comment is deleted successfuly')
            return HttpResponseRedirect(success_url)
        else:
            return HttpResponseRedirect(reverse_lazy('blog:nopermission'))


class CommentEditView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    model = Comment
    template_name = 'blog/comment_update_form.html'
    fields = ['text']

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             'The comment is edited succesfully')
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})


class DeletePostView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    model = Post
    success_url = reverse_lazy('blog:homePage')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == request.user:
            self.object.delete()
            success_url = self.get_success_url()
            messages.add_message(self.request, messages.INFO,
                                 'The post is deleted successfuly')
            return HttpResponseRedirect(success_url)
        else:
            return HttpResponseRedirect(reverse_lazy('blog:nopermission'))


class UpdatePostView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "login"
    model = Post
    template_name = 'blog/post_update_form.html'
    fields = ['title', 'content']
    success_message = "Post was updated successfully"

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class NoPermisionTemplateView(TemplateView):
    template_name = 'blog/nopermission.html'


class UserPostsListView(ListView):
    model = Post
    template_name = 'blog/userposts.html'
    ordering = ['-date_posted']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['pk'])
        queryset = user.post_set.all().order_by('-date_posted')
        return queryset
