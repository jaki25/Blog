from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator
# Create your models here.

class Tag(models.Model):
    caption=models.CharField(max_length=10)

    def __str__(self):
        return self.caption

class Author(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField()

    def fully_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.fully_name()

class Post(models.Model):
    title=models.CharField(max_length=150)
    excerpt=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images", null=True)
    date=models.DateField(auto_now=True)
    slug=models.SlugField(unique=True, db_index=True)
    contnet=models.TextField(validators=[MinLengthValidator(10)])
    author=models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name="posts")
    tag=models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.title}_::({self.author})"

class Comment(models.Model):
    user_name=models.CharField(max_length=50, null=False)
    email=models.EmailField(max_length=254, null=False)
    text=models.TextField()
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")


