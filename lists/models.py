from django.db import models


class List(models.Model):
    pass


class ListItem(models.Model):
    list = models.ForeignKey(List, on_delete=models.PROTECT, default=None)
    text = models.TextField()
