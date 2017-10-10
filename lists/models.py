from django.db import models


class List(models.Model):
    """
    Handles storing the different lists
    """
    pass


class Item(models.Model):
    """
    Handles storing to-do list items
    """
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
    pass
