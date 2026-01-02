from django.test import TestCase

from cookbook.forms import (
    RecipeForm,
    CommentForm,
    RecipeSearchForm
)
from cookbook.models import Category


class FormTests(TestCase):
    def test_comment_form_rating_choices(self):
        form = CommentForm()
        choices = list(form.fields["rating"].widget.choices)
        expected = [(i, i) for i in range(1, 6)]
        self.assertEqual(choices, expected)

    def test_recipe_search_form_categories(self):
        Category.objects.create(name="Breakfast")
        form = RecipeSearchForm()
        self.assertTrue(
            form.fields["category"]
            .queryset.filter(name="Breakfast")
            .exists()
        )

    def test_recipe_form_cooking_time_validation(self):
        data = {"title": "T", "cooking_time": 0}
        form = RecipeForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("cooking_time", form.errors)
