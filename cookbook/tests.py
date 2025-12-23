from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Recipe, Category, Comment


User = get_user_model()


class CookbookViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='chef', password='password123')
        self.category = Category.objects.create(name='Десерти')
        self.recipe = Recipe.objects.create(
            title='Тестовий торт',
            author=self.user,
            category=self.category,
            cooking_time=30,
            servings=4
        )

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('cookbook:recipe-detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recipe.title)

    def test_add_comment_authenticated_user(self):
        self.client.login(username='chef', password='password123')

        response = self.client.post(reverse('cookbook:add-comment', kwargs={'pk': self.recipe.pk}), {
            'content': 'Дуже смачно!',
            'rating': 5
        })
        self.assertRedirects(response, reverse('cookbook:recipe-detail', kwargs={'pk': self.recipe.pk}))

        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'Дуже смачно!')
        self.assertEqual(comment.rating, 5)
