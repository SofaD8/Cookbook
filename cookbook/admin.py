from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    User,
    Category,
    Tag,
    Recipe,
    Comment
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin panel"""
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff"
    ]
    list_filter = [
        "is_staff",
        "is_superuser",
        "date_joined"
    ]
    search_fields = [
        "username",
        "email",
        "first_name",
        "last_name"
    ]

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                "bio",
                "profile_image",
                "favorite_recipes"
            )
        }),
    )

    filter_horizontal = [
        "favorite_recipes",
        "groups",
        "user_permissions"
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin panel"""
    list_display = ["name", "recipe_count"]
    search_fields = ["name"]

    def recipe_count(self, obj):
        return obj.recipes.count()

    recipe_count.short_description = "Number of Recipes"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin panel"""
    list_display = [
        "name",
        "slug",
        "recipe_count"
    ]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}

    def recipe_count(self, obj):
        return obj.recipes.count()

    recipe_count.short_description = "Number of Recipes"


class CommentInline(admin.TabularInline):
    """Inline comments for Recipe admin"""
    model = Comment
    extra = 0
    fields = [
        "author",
        "content",
        "rating",
        "created_at"
    ]
    readonly_fields = ["created_at"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Recipe admin panel"""
    list_display = [
        "title",
        "author",
        "category",
        "cooking_time",
        "servings",
        "created_at",
        "average_rating"
    ]
    list_filter = [
        "category",
        "tags",
        "created_at",
        "author"
    ]
    search_fields = [
        "title",
        "description",
        "author__username"
    ]
    filter_horizontal = ["tags"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "average_rating"
    ]
    date_hierarchy = "created_at"

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "title",
                "author",
                "category",
                "description"
            )
        }),
        ("Recipe Details", {
            "fields": (
                "ingredients",
                "instructions",
                "cooking_time",
                "servings"
            )
        }),
        ("Media & Tags", {
            "fields": ("image", "tags")
        }),
        ("Metadata", {
            "fields": (
                "created_at",
                "updated_at",
                "average_rating"
            ),
            "classes": ("collapse",)
        }),
    )

    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin panel"""
    list_display = [
        "author",
        "recipe",
        "rating",
        "created_at",
        "short_content"
    ]
    list_filter = [
        "rating",
        "created_at",
        "author"
    ]
    search_fields = [
        "content",
        "author__username",
        "recipe__title"
    ]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"

    def short_content(self, obj):
        return obj.content[:50] + "..." \
            if len(obj.content) > 50 \
            else obj.content

    short_content.short_description = "Content Preview"
