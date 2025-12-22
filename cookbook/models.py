from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)


class User(AbstractUser):
    """Custom User model extending AbstractUser"""
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text="Про себе"
    )
    profile_image = CloudinaryField(
        "profile image",
        folder="profiles/",
        blank=True,
        null=True,
        help_text="Додайте світлину"
    )
    favorite_recipes = models.ManyToManyField(
        "Recipe",
        related_name="favorited_by",
        blank=True
    )

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse(
            "cookbook:user-detail",
            kwargs={"pk": self.pk}
        )


class Category(models.Model):
    """Recipe categories (Desserts, Main Courses, etc.)"""
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Назва категорії"
    )
    description = models.TextField(
        blank=True,
        help_text="Опис категорії"
    )

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "cookbook:category-detail",
            kwargs={"pk": self.pk}
        )


class Tag(models.Model):
    """Tags for recipes (vegetarian, quick, healthy, etc.)"""
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Назва тегу"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        help_text="URL-friendly версія назви"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "cookbook:tag-detail",
            kwargs={"pk": self.pk}
        )


class Recipe(models.Model):
    """Main Recipe model"""
    title = models.CharField(
        max_length=200,
        help_text="Назва рецепту"
    )
    description = models.TextField(
        help_text="Короткий опис страви"
    )
    ingredients = models.TextField(
        help_text="Список інгрідієнтів (кожен з нової стрічки"
    )
    instructions = models.TextField(
        help_text="Покрокова інструкція приготування"
    )
    cooking_time = models.PositiveIntegerField(
        help_text="Час приготування в хвилинах",
        validators=[MinValueValidator(1)]
    )
    servings = models.PositiveIntegerField(
        default=1,
        help_text="Кількість порцій",
        validators=[MinValueValidator(1)]
    )
    image = CloudinaryField(
        "image",
        folder="recipes/",
        blank=True,
        null=True,
        help_text="Додайте світлину страви"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        help_text="Автор рецепту"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="recipes",
        help_text="Категорія рецепту"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
        blank=True,
        help_text="Тег для рецепту"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "cookbook:recipe-detail",
            kwargs={"pk": self.pk}
        )

    @property
    def average_rating(self):
        """Calculate average rating from comments"""
        ratings = self.comments.exclude(rating__isnull=True).values_list("rating", flat=True)
        if ratings:
            return round(sum(ratings) / len(ratings), 1)
        return None


class Comment(models.Model):
    """Comments on recipes"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="Назва рецепту"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="Автор коментаря"
    )
    content = models.TextField(
        help_text="Ваш коментар"
    )
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Оцініть цей рецепт (1-5 зірок)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.recipe.title}"

    def get_absolute_url(self):
        return reverse(
            "cookbook:recipe-detail",
            kwargs={"pk": self.recipe.pk}
        )
