from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Task(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owner")
    categories = models.ManyToManyField(
        Category, related_name="tasks")
    done = models.BooleanField(default=False)
    responsible = models.ForeignKey(
            settings.AUTH_USER_MODEL, 
            related_name="responsible",
            blank=True,
            null=True,
    )

    def __str__(self):
        return self.name
