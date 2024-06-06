from django import forms
from django.core.exceptions import ValidationError
from lists.models import Item, List

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You can't have a duplicate item on your list"

class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ("text",)
        widgets = {
            "text": forms.widgets.TextInput(
                attrs={
                    "placeholder": "Enter a to-do item",
                    "class": "form-control form-control-lg",
                }
            ),
        }
        error_messages = {"text": {"required": EMPTY_ITEM_ERROR}}

    # The .instance attribute on a form represents the database object that is being modified or created
    def save(self, for_list):
        self.instance.list = for_list
        return super().save()
    
class ExistingListItemForm(ItemForm): 
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)