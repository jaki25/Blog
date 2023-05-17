from . import views
from django.urls import path

urlpatterns= [
path("", views.Starting_pageView.as_view(), name="starting-page"),
path("posts", views.PostView.as_view(), name="posts-page"),
path("posts/<slug:slug>", views.Single_postView.as_view(), name="post-detail"), #posts/my-first-page
path("read-latar", views.ReadLaterPost.as_view(), name="read-later"),
path("<int:i>", views.Erorr),
path("<str:i>", views.Erorr),
]