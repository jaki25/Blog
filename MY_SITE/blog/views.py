from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.template.loader import render_to_string
from datetime import date
from django.http import HttpResponseNotFound, HttpResponseRedirect
#temperary posts

from .models import Post, Author, Tag, Comment
from django.views.generic import ListView, DetailView
from .forms import CommentForm
from django.views import View
import time

# Create your views here.

class Starting_pageView(ListView):
    template_name="blog/index.html"
    model=Post
    oredring=["-date"]
    context_object_name="posts"

    def get_queryset(self):
        
        query= super().get_queryset()
        data=query.order_by("-id")

        return data[:3]
    
#rendering template without class based views
"""def starting_page(request):
    
    latest_post= Post.objects.all().order_by('date')[:3]
    try:

        return render(request, "blog/index.html", {
            "posts":latest_post
        })
    except:
        response= render_to_string("404.html")
        return HttpResponseNotFound(response)
"""
class PostView(ListView):
    template_name="blog/all-posts.html"
    model=Post
    context_object_name="all_posts"

#rendering template without class based views
"""def posts(request):

    try:
        all_posts=Post.objects.all()
        return render(request, "blog/all-posts.html", {
            "all_posts":all_posts
        })
    except:
        response= render_to_string("404.html")
        return HttpResponseNotFound(response)
    """

class Single_postView(View):
    
    def is_stored_post(self,request, post_id):
        stored_post=request.session.get("stored_post")
        if stored_post is not None:
            is_saved_for_later= post_id in stored_post
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self,request, slug):
        post=Post.objects.get(slug=slug)
        context={
        "post":post,
        "post_tag":post.tag.all(),
        "form":CommentForm(),
        "comments":post.comments.all().order_by("-id"),
        "is_stored": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form=CommentForm(request.POST)
        post=Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment=comment_form.save(commit=False) #this create an instance and not touching the data base
            comment.post=post
            comment.save()
            return HttpResponseRedirect("/posts/"+ slug)
        
        
        context={
        "post":post,
        "post_tag":post.tag.all(),
        "form":comment_form,
        "comments":post.comments.all(),
        "is_stored":self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    

 #rendering template without class based views   
"""
def single_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)

    

        return render(request, "blog/post-detail.html", {
            "post":post, "post_tag":post.tag.all()
        })
    except:
        response= render_to_string("404.html")
        return HttpResponseNotFound(response)"""


class ReadLaterPost(View):
    def get(self, request):
        stored_posts=request.session.get("stored_posts")
        context={}
        if stored_posts is None or len(stored_posts) == 0:
            
            context["post"] = []
            context["has_post"] = False
        else:
            posts=Post.objects.filter(id__in=stored_posts)
            context["posts"]=posts
            context["has_post"] = True
        
        return render(request, "blog/read_later.html", context)

    def post(self, request):
        stored_posts=request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts=[]
        
        post_id=int(request.POST["post_id"])

        if post_id not in stored_posts:

            stored_posts.append(post_id)
            
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"]=stored_posts
        return HttpResponseRedirect("/")




def Erorr(request,i):
    response= render_to_string("404.html")
    return HttpResponseNotFound(response) 