from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Recipe, Comment


class RecipeForm(forms.ModelForm):
    """Recipe creation and update form"""


    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "category",
            "ingredients",
            "instructions",
            "cooking_time",
            "servings",
            "image",
            "tags"
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введіть назву рецепта..."
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Короткий опис вашої страви..."
            }),
            "category": forms.Select(attrs={
                "class": "form-select"
            }),
            "ingredients": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder":
                    "Список інгредієнтів (по одному на рядок):\n"
                    "- 2 склянки борошна\n- 1 яйце\n- ..."
            }),
            "instructions": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
                "placeholder":
                    "1. Перший крок...\n2. Другий крок...\n..."
            }),
            "cooking_time": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Хвилини",
                "min": 1
            }),
            "servings": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Кількість порцій",
                "min": 1
            }),
            "image": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*"
            }),
            "tags": forms.CheckboxSelectMultiple(),
        }
        help_texts = {
            "cooking_time": "Загальний час приготування в хвилинах",
            "servings": "На скільки порцій?",
            "tags": "Виберіть усе, що підходить",
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["image"].required = False


class CommentForm(forms.ModelForm):
    """Comment form for recipes"""


    class Meta:
        model = Comment
        fields = ["content", "rating"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Поділіться своєю думкою про рецепт..."
            }),
                "rating": forms.RadioSelect(
                choices=[(i, i) for i in range(1, 6)]),
        }
        labels = {
            "content": "Ваш коментар",
            "rating": "Оцініть цей рецепт (optional)",
        }


class RecipeSearchForm(forms.Form):
    """Search form for recipes"""
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Пошук рецептів...",
            "aria-label": "Search"
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        empty_label="Всі категорії",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    def __init__(self, *args, **kwargs):
        from .models import Category

        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
