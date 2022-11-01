from django.urls import path
from .views import (
    HomeView, 
    UserRegistrationView, 
    LoginUserView, 
    LogoutUserView, 
    NewBlogView, 
    UpdateBlogView, 
    NewBlogPostView, 
    UpdateBlogPostView,
    BlogPostDetailView
    )

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout_page/', LogoutUserView.as_view(), name='logout_page'),
    path('blog-settings/', NewBlogView.as_view(), name="blog-settings"),
    path('new/blog-post/', NewBlogPostView.as_view(), name='new-blog-post'),
    path('detail/blog-post/<int:pk>/', BlogPostDetailView.as_view(), name='blog-post-detail'),
    path('update/blog-post/<int:pk>/', UpdateBlogPostView.as_view(), name='update-blog-post'),
    path('update/blog-settings/<int:pk>', UpdateBlogView.as_view(), name='update-blog-settings'),
]