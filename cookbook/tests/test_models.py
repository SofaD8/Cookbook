from django.test import TestCase
from django.contrib.auth import get_user_model

from cookbook.models import (
    Recipe,
    Category,
    Tag,
    Comment
)


User = get_user_model()


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="chef",
            password="password123"
        )
        self.category = Category.objects.create(name="Main Course")
        self.tag = Tag.objects.create(name="Vegan", slug="vegan")
        self.recipe = Recipe.objects.create(
            title="Pasta",
            description="Good pasta",
            ingredients="Water, Flour",
            instructions="Cook it",
            cooking_time=20,
            author=self.user,
            category=self.category
        )

    def test_recipe_average_rating(self):
        Comment.objects.create(
            recipe=self.recipe,
            author=self.user,
            content="Nice",
            rating=5
        )
        Comment.objects.create(
            recipe=self.recipe,
            author=self.user,
            content="Ok",
            rating=3
        )
        self.assertEqual(self.recipe.average_rating, 4.0)

    def test_category_absolute_url(self):
        self.assertEqual(
            self.category.get_absolute_url(),
            f"/category/{self.category.pk}/"
        )
