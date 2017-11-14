from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class List(models.Model):
    """
    Handles storing the different lists
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    
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

    class Meta:
        """
        Provide meta information for this model so that duplicate items can't be in the same list.
        """
        ordering = ('id',)
        unique_together = ('list', 'text')

    def __str__(self):
        """
        Convert Item objects to their string text representations.
        """
        return self.text
