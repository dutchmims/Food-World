from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Post, Tag
from .forms import CommentForm, PostForm, PostUpdateForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse

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


class PostLike(View):
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def tag_posts(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.filter(status=1).order_by("-created_on")
    page_number = request.GET.get('page')
    posts_per_page = 6
    paginator = Paginator(posts, posts_per_page)
    paginated_posts = paginator.get_page(page_number)

    return render(
        request,
        "tag_posts.html",
        {
            "tag": tag,
            "posts": paginated_posts,
        },
    )

class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('home')


class PostUpdate(UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'post_update.html'

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.slug])


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    template_name = 'post_confirm_delete.html'


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6
