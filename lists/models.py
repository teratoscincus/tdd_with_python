from django.db import models


class ListItem(models.Model):
    text = models.TextField()
