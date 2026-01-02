import cloudinary
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.db.models import Avg
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)


class User(AbstractUser):
    """Custom User model extending AbstractUser"""
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text="Tell us about yourself"
    )
    profile_image = CloudinaryField(
        "profile image",
        folder="profiles/",
        blank=True,
        null=True,
        help_text="Upload your profile picture"
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
        help_text="Category name"
    )
    description = models.TextField(
        blank=True,
        help_text="Category description"
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
        help_text="Tag name"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        help_text="URL-friendly version of the name"
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
        help_text="Receipe title"
    )
    description = models.TextField(
        help_text="Short description of the dish"
    )
    ingredients = models.TextField(
        help_text="List of ingredients (one per line)"
    )
    instructions = models.TextField(
        help_text="Step-by-step cooking instructions"
    )
    cooking_time = models.PositiveIntegerField(
        help_text="Cooking time in minutes",
        validators=[MinValueValidator(1)]
    )
    servings = models.PositiveIntegerField(
        default=1,
        help_text="Number of servings",
        validators=[MinValueValidator(1)]
    )
    image = CloudinaryField(
        "image",
        folder="test_folder",
        blank=True,
        null=True,
        help_text="Upload a photo of your dish"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        help_text="Recipe author"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="recipes",
        help_text="Recipe category"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
        blank=True,
        help_text="Recipe tags"
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
        avg = self.comments.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else None


class Comment(models.Model):
    """Comments on recipes"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="Recipe name"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="Comment author"
    )
    content = models.TextField(
        help_text="Enter your comment here"
    )
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate this recipe (1-5 stars)"
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


@receiver(post_delete, sender=Recipe)
def photo_delete(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)


@receiver(pre_save, sender=Recipe)
def photo_delete_on_change(sender, instance, **kwargs):
    """Deletes old image from Cloudinary when a new one is uploaded"""
    if not instance.pk:
        return False

    try:
        old_file = Recipe.objects.get(pk=instance.pk).image
    except Recipe.DoesNotExist:
        return False

    new_file = instance.image
    if old_file and old_file != new_file:
        cloudinary.uploader.destroy(old_file.public_id)
