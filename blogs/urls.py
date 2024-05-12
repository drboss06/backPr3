from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf.urls import handler404
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    AddCommentView,
    SignupView,
    PostByCategoryListView,
    PostByTagListView,
)

handler404 = 'blogs.views.custom_404_view'

urlpatterns = [
    path("new/", BlogCreateView.as_view(), name="post_new"),
    # path("<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path('<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='post_detail'),
    path("<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"),
    path("<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),
    path("", BlogListView.as_view(), name="post_list"),
    path('post/<int:post_id>/add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', SignupView.as_view(), name='signup'),
    path('home/', TemplateView.as_view(template_name='post/post_new.html'), name='home'),
    path('category/<slug:category_slug>/', PostByCategoryListView.as_view(), name='post_list_by_category'),
    path('tag/<slug:tag_slug>/', PostByTagListView.as_view(), name='post_list_by_tag'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
