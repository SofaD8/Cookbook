from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Recipe, Comment


class RecipeForm(forms.ModelForm):
    """Recipe creation and update form"""


    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'category',
            'ingredients',
            'instructions',
            'cooking_time',
            'servings',
            'image',
            'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter recipe title...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of your dish...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder':
                    'List ingredients (one per line):\n'
                    '- 2 cups flour\n- 1 egg\n- ...'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder':
                    '1. First step...\n2. Second step...\n...'
            }),
            'cooking_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minutes',
                'min': 1
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of servings',
                'min': 1
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'tags': forms.CheckboxSelectMultiple(),
        }
        help_texts = {
            'cooking_time': 'Total cooking time in minutes',
            'servings': 'How many people does this recipe serve?',
            'tags': 'Select all that apply',
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['image'].required = False


class CommentForm(forms.ModelForm):
    """Comment form for recipes"""


    class Meta:
        model = Comment
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your thoughts about this recipe...'
            }),
            'rating': forms.RadioSelect(
                choices=[(i, f'{i} ⭐') for i in range(1, 6)]
            ),
        }
        labels = {
            'content': 'Your Comment',
            'rating': 'Rate this Recipe (optional)',
        }


class RecipeSearchForm(forms.Form):
    """Search form for recipes"""
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search recipes...',
            'aria-label': 'Search'
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        from .models import Category

        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
