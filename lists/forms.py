from django import forms
from django.core.exceptions import ValidationError
from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this item in your list"


class ItemForm(forms.models.ModelForm):
    """
    Create form for items to be loaded and validated.
    """
    
    class Meta:
        """
        Specifiy meta information about the form.
        
        Note: required class for ModelForm.
        """
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(
                attrs={
                    'placeholder': 'Enter a to-do item',
                    'class': 'form-control input-lg',
                }
            ),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }
    
    def save(self, for_list):
        """
        Save item from form to database.
        """
        self.instance.list = for_list
        return super().save()


class ExistingListItemForm(ItemForm):
    """
    Create form for items to be submitted to an existing list.
    """

    def __init__(self, for_list, *args, **kwargs):
        """
        Initiate form with the correct list.
        """
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        """
        Overwrite valdiation to except for error, in which case add to errors list
        """
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    def save(self):
        """
        Saves item to database.
        
        Note: Override inherited save from Item form to use the original save.
        """
        return forms.models.ModelForm.save(self)
