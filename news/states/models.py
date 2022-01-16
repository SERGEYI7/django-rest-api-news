from django.db import models
import datetime


class Author(models.Model):
    first_name = models.CharField(max_length=50, unique=True)
    last_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.title}'


class Tag(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.title}'


class State(models.Model):
    title = models.CharField(max_length=100, blank=True)
    summary = models.CharField(max_length=300)
    content = models.TextField()
    author = models.ForeignKey(Author,
                               on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    date_ = str(datetime.datetime.today())
    date = models.DateTimeField(default=date_, blank=True, null=True)