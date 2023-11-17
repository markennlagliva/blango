from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post
from blog.forms import CommentForm

# Loggers
import logging
logger = logging.getLogger(__name__)

# View Caching
from django.views.decorators.cache import cache_page

# Cooking - Varying On Headers
from django.views.decorators.vary import vary_on_headers, vary_on_cookie

# Create your views here.
# 300 seconds == 5 minutes
# @cache_page(300)
# @vary_on_cookie
# def index(request):
#   from django.http import HttpResponse
#   logger.debug('Index function is called!')
#   return HttpResponse(str(request.user).encode("ascii"))
#   posts = Post.objects.filter(published_at__lte=timezone.now())
#   logger.debug("Got %d posts", len(posts))
#   return render(request, 'blog/index.html', {'posts': posts})

def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now())
    logger.debug("Got %d posts", len(posts))
    return render(request, "blog/index.html", {"posts": posts})

def post_detail(request, slug):
  post = get_object_or_404(Post, slug=slug)

  if request.user.is_active:
    if request.method == "POST":
      comment_form = CommentForm(request.POST)

      if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.content_object = post
        comment.creator = request.user
        logger.info(
          "Created comment on Post %d for user %s", post.pk, request.user 
        )
        comment.save()
        return redirect(request.path_info) # redirect back to the Current Post
    else:
      comment_form = CommentForm()
  else:
    comment_form = None


  return render(
    request, "blog/post-detail.html", {"post": post, "comment_form": comment_form}
  )