from django.db import models
from django.core.urlresolvers import reverse


class List(models.Model):
    """
    Handles storing the different lists
    """
    
    def get_absolute_url(self):
        """
        Returns the URL used by the view
        """
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    """
    Handles storing to-do list items
    """
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
    pass
