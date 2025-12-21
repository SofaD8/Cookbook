from django.urls import path

from . import views


app_name = "cookbook"

urlpatterns = [
    # Homepage
    path("", views.index, name="index"),

    # Recipe URLs
    path(
        "recipes/",
        views.RecipeListView.as_view(),
        name="recipe-list"
    ),
    path(
        "recipe/<int:pk>/",
        views.RecipeDetailView.as_view(),
        name="recipe-detail"
    ),
    path(
        "recipe/create/",
        views.RecipeCreateView.as_view(),
        name="recipe-create"
    ),
    path(
        "recipe/<int:pk>/update/",
        views.RecipeUpdateView.as_view(),
        name="recipe-update"
    ),
    path(
        "recipe/<int:pk>/delete/",
        views.RecipeDeleteView.as_view(),
        name="recipe-delete"
    ),

    # Comment URLs
    path(
        "recipe/<int:pk>/comment/",
        views.add_comment,
        name="add-comment"
    ),

    # Favorite URLs
    path(
        "recipe/<int:pk>/favorite/",
        views.toggle_favorite,
        name="toggle-favorite"
    ),

    # Category URLs
    path(
        "categories/",
        views.CategoryListView.as_view(),
        name="category-list"
    ),
    path(
        "category/<int:pk>/",
        views.CategoryDetailView.as_view(),
        name="category-detail"
    ),

    # Tag URLs
    path(
        "tags/",
        views.TagListView.as_view(),
        name="tag-list"
    ),
    path(
        "tag/<int:pk>/",
        views.TagDetailView.as_view(),
        name="tag-detail"
    ),

    # User Profile URLs
    path(
        "user/<int:pk>/",
        views.UserDetailView.as_view(),
        name="user-detail"
    ),
]
