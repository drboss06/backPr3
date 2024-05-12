from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template import RequestContext
from django.db.models import Q

from .models import Post, Comment, Category, Tag
from .forms import PostSearchForm


class BlogListView(ListView):
    model = Post
    paginate_by = 3
    template_name = "post/post_list.html"
    
    context_object_name = 'posts'
    form_class = PostSearchForm

    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')
        category = self.request.GET.get('category')

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

        if category:
            queryset = queryset.filter(category=category)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        
        return context

class BlogDetailView(DetailView):
    model = Post
    template_name = "post/post_detail.html"
    slug_url_kwarg = 'slug'
    

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(self.get_queryset(), slug=slug)


class BlogCreateView(SuccessMessageMixin, CreateView):
    model = Post
    template_name = "post/post_new.html"
    fields = ["name", "description", "featured_image", "category", "tags"]
    success_message = "%(name)s успешно создан"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "post/post_edit.html"
    fields = ["name", "description", "featured_image", "category", "tags"]
    success_message = "%(name)s успешно обновлен"
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "post/post_delete.html"
    context_object_name = 'post'
    success_url = reverse_lazy("post_list")
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class AddCommentView(View):
    # def post(self, request, post_id):
    #     post = Post.objects.get(pk=post_id)
    #     comment_content = request.POST.get('content')

    #     # Create a new Comment instance and associate it with the Post
    #     new_comment = Comment(post=post, content=comment_content)
    #     new_comment.save()

    #     return redirect('post_detail', pk=post_id)  # Redirect to the post detail page after adding the comment
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        comment_content = request.POST.get('content')

        new_comment = Comment(content=comment_content)
        new_comment.save()

        post.comment.add(new_comment)

        return redirect('post_detail', pk=post_id)



class PostByCategoryListView(ListView):
    model = Post
    template_name = "post/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Post.objects.filter(category=category)


class PostByTagListView(ListView):
    model = Post
    template_name = "post/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Post.objects.filter(tags=tag)


def custom_404_view(request, exception):
    return render(request, '404.html', {'message': 'К сожалению, страница не существует'}, status=404)