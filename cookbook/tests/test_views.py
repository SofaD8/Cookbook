from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from cookbook.models import Recipe, Category


User = get_user_model()


class CookbookViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="chef",
            password="password123"
        )
        self.category = Category.objects.create(name="Desserts")
        self.recipe = Recipe.objects.create(
            title="Test Cake",
            author=self.user,
            category=self.category,
            cooking_time=30,
            servings=4,
            description="English test description",
            ingredients="Flour, Sugar",
            instructions="Mix and bake"
        )

    def test_index_view_exists(self):
        response = self.client.get(reverse("cookbook:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "cookbook/index.html"
        )

    def test_add_comment_post_only(self):
        self.client.login(
            username="chef",
            password="password123"
        )
        url = reverse(
            "cookbook:add-comment",
            kwargs={"pk": self.recipe.pk}
        )
        response = self.client.post(url, {
            "content": "Nice logic!",
            "rating": 5
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.recipe.comments.count(), 1)

    def test_favorite_toggle_post(self):
        self.client.login(
            username="chef",
            password="password123"
        )
        url = reverse(
            "cookbook:toggle-favorite",
            kwargs={"pk": self.recipe.pk}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self.user.favorite_recipes
            .filter(pk=self.recipe.pk)
            .exists()
        )
