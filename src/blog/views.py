from django.contrib import messages
from django.utils.text import slugify
from .forms import BlogForm, BlogPostForm   
from .models import Blog, BlogPost
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


@method_decorator(login_required(login_url="login"), name='dispatch')
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            if Blog.objects.filter(owner=self.request.user).exists():
                blog = Blog.objects.get(owner=self.request.user)
                context['hasBlog'] = True
                context['blog'] = Blog.objects.get(owner=self.request.user)
                context['blogPosts'] = BlogPost.objects.filter(blog=blog)
        return context

class NewBlogPostView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog_post.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewBlogPostView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        blog_post_obj = form.save(commit=False)
        blog_post_obj.blog = Blog.objects.get(owner=self.request.user)
        blog_post_obj.is_published = True
        blog_post_obj.slug = slugify(blog_post_obj.title)
        blog_post_obj.save()
        return HttpResponseRedirect(reverse_lazy('home'))

class UpdateBlogPostView(UpdateView):
    form_class = BlogPostForm
    model = BlogPost
    success_url = reverse_lazy('home')
    template_name = 'blog_post.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateBlogPostView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(UpdateBlogPostView, self).get_queryset()
        return queryset.filter(blog__owner = self.request.user)

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_post_detail.html'

class UpdateBlogView(UpdateView):
    form_class = BlogForm
    model = Blog
    template_name = 'blog_settings.html'
    success_url = reverse_lazy('home')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateBlogView, self).dispatch(request, *args, **kwargs)


class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'user_registration.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)    


class LoginUserView(LoginView):
    template_name = 'login.html'
    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)    

class LogoutUserView(LogoutView):
    template_name = 'logout_page.html'

@method_decorator(login_required(login_url='login'), name='dispatch')
class NewBlogView(CreateView):
    form_class = BlogForm
    template_name = 'blog_settings.html'

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.owner = self.request.user
        blog_obj.slug = slugify(blog_obj.title)

        blog_obj.save()
        return HttpResponseRedirect(reverse('home'))

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if Blog.objects.filter(owner=user).exists():
            return HttpResponseForbidden("You can not create more than one blogs per account!")
        else:
            return super(NewBlogView, self).dispatch(request, *args, **kwargs)
        

class ShareBlogPostView(TemplateView):
    template_name = 'share_blog_post.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ShareBlogPostView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, pk, **kwargs):
        context = super(ShareBlogPostView, self).get_context_data(pk, **kwargs)
        blog_post = BlogPost.objects.get(id=pk)
        currently_shared_with = blog_post.shared_to.all()
        currently_shared_with_ids = map(lambda x: x.pk, currently_shared_with)
        exclude_from_can_share_list = [blog_post.blog.pk] + list(currently_shared_with_ids)
        can_be_shared_with = Blog.objects.exclude(pk__in = exclude_from_can_share_list)
        context['post'] = blog_post
        context['is_shared_with'] = currently_shared_with
        context['can_be_shared_with'] = can_be_shared_with
        return context