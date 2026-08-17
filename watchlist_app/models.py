from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Media(models.Model):
    TYPE_MOVIE = 'MOVIE'
    TYPE_TV = 'TV'
    TYPE_CHOICES = [
        (TYPE_MOVIE, 'Movie'),
        (TYPE_TV, 'TV'),
    ]

    STATUS_UNWATCHED = 'UNWATCHED'
    STATUS_WATCHED = 'WATCHED'
    STATUS_CHOICES = [
        (STATUS_UNWATCHED, 'Unwatched'),
        (STATUS_WATCHED, 'Watched'),
    ]

    title = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_MOVIE)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_UNWATCHED)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['status', 'title']

    def __str__(self):
        return self.title
