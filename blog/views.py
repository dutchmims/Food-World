from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Tag
from .forms import CommentForm, PostForm, PostUpdateForm


class PostLike(View):
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        response_data = {
            'liked': liked,
            'like_count': post.likes.count(),
        }

        return JsonResponse(response_data)



class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = post.likes.filter(id=request.user.id).exists() if request.user.is_authenticated else False
        tags = post.tags.all()

        comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": comment_form,
                "tags": tags,
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = post.likes.filter(id=request.user.id).exists() if request.user.is_authenticated else False

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            messages.success(request, 'Your comment has been submitted successfully!')
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
        else:
            messages.error(request, 'There was an error with your comment submission. Please try again.')
            return render(
                request,
                "post_detail.html",
                {
                    "post": post,
                    "comments": comments,
                    "commented": True,
                    "comment_form": comment_form,
                    "liked": liked
                },
            )

class CommentCreate(View):
    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            messages.success(request, 'Your comment has been submitted successfully!')
        else:
            messages.error(request, 'There was an error with your comment submission. Please try again.')

        return redirect('post_detail', slug=slug)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

class PostLike(View):
    def post(self, request, slug, *args, **kwargs):
        try:
            post = get_object_or_404(Post, slug=slug)
            liked = False

            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
                liked = True

            response_data = {
                'success': True,
                'liked': liked,
                'like_count': post.likes.count(),
            }

            return JsonResponse(response_data, status=200)

        except Exception as e:
            response_data = {
                'success': False,
                'error_message': str(e),
            }

            return JsonResponse(response_data, status=400)


class TagPosts(ListView): 
    model = Post
    template_name = "tag_posts.html"
    paginate_by = 6

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, name=tag_name)
        return tag.posts.filter(status=1).order_by("-created_on")


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('home')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'post_update.html'

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.slug])


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    template_name = 'post_confirm_delete.html'


class PostList(ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6
