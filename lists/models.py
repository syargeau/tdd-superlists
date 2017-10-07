from django.db import models

class Item(models.Model):
    """
    Handles storing to-do list items
    """
    text = models.TextField(default='')
    pass
