from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q, Count, Avg
from django.http import HttpResponseRedirect

from .models import (
    User,
    Recipe,
    Category,
    Tag,
    Comment
)
from .forms import (
    RecipeForm,
    CommentForm,
    RecipeSearchForm
)


def index(request):
    """Homepage with featured recipes"""
    recent_recipes = Recipe.objects.select_related(
        "author", "category"
    ).prefetch_related("tags").order_by("-created_at")[:6]

    popular_recipes = Recipe.objects.annotate(
        comment_count=Count("comments")
    ).order_by("-comment_count")[:3]

    context = {
        "recent_recipes": recent_recipes,
        "popular_recipes": popular_recipes,
        "total_recipes": Recipe.objects.count(),
        "total_users": User.objects.count(),
    }
    return render(
        request,
        "cookbook/index.html",
        context
    )


class RecipeListView(generic.ListView):
    """List all recipes with search and filter"""
    model = Recipe
    template_name = "cookbook/recipe_list.html"
    context_object_name = "recipes"
    paginate_by = 12

    def get_queryset(self):
        queryset = Recipe.objects.select_related(
            "author", "category"
        ).prefetch_related("tags").order_by("-created_at")

        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(ingredients__icontains=query)
            )

        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        tag_id = self.request.GET.get("tag")
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        sort = self.request.GET.get("sort")
        if sort == "oldest":
            queryset = queryset.order_by("created_at")
        elif sort == "popular":
            queryset = (queryset.annotate(
                num_comments=Count("comments"))
                        .order_by("-num_comments")
                        )
        elif sort == "rating":
            queryset = (queryset.annotate(
                avg_rate=Avg("comments__rating"))
                        .order_by("-avg_rate")
                        )
        else:
            queryset = queryset.order_by("-created_at")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = RecipeSearchForm(self.request.GET)
        context["categories"] = Category.objects.all()
        context["tags"] = Tag.objects.all()
        context["current_query"] = self.request.GET.get("query", "")
        context["current_category"] = self.request.GET.get("category", "")
        context["current_tag"] = self.request.GET.get("tag", "")
        context["current_sort"] = self.request.GET.get("sort", "")
        return context


class RecipeDetailView(generic.DetailView):
    """Recipe detail page with comments"""
    model = Recipe
    template_name = "cookbook/recipe_detail.html"
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()

        context["comments"] = (recipe.comments
                               .select_related("author")
                               .all()
                               )

        if self.request.user.is_authenticated:
            context["comment_form"] = CommentForm()
            context["is_favorite"] = (
                self.request.user.favorite_recipes
                .filter(pk=recipe.pk).exists()
            )

        context["is_author"] = (
                self.request.user.is_authenticated and
                self.request.user == recipe.author
        )

        context["related_recipes"] = Recipe.objects.filter(
            category=recipe.category
        ).exclude(pk=recipe.pk).select_related("author")[:3]

        return context


class RecipeCreateView(LoginRequiredMixin, generic.CreateView):
    """Create new recipe"""
    model = Recipe
    form_class = RecipeForm
    template_name = "cookbook/recipe_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request,
            "Recipt created successfully!"
        )
        return super().form_valid(form) # noqa


class RecipeUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView):
    """Update existing recipe (only author can edit)"""
    model = Recipe
    form_class = RecipeForm
    template_name = "cookbook/recipe_form.html"

    def test_func(self):
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        messages.success(
            self.request,
            "Recipt updated successfully!"
        )
        return super().form_valid(form) # noqa


class RecipeDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    """Delete recipe (only author can delete)"""
    model = Recipe
    template_name = "cookbook/recipe_confirm_delete.html"
    success_url = reverse_lazy("cookbook:recipe-list")

    def test_func(self):
        return self.request.user == self.get_object().author

    def delete(self, request, *args, **kwargs):
        messages.success(
            request,
            "Recipt deleted successfully!")
        return super().delete(
            request,
            *args,
            **kwargs
        )


@login_required
def add_comment(request, pk):
    """Add comment to recipe"""
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.author = request.user
            comment.save()
            messages.success(
                request,
                "Your comment has been added successfully!"
            )
        else:
            messages.error(
                request,
                "Error adding comment. Please check your data and try again."
            )

    return redirect("cookbook:recipe-detail", pk=pk)


@login_required
def toggle_favorite(request, pk):
    """Add or remove recipe from favorites"""
    recipe = get_object_or_404(Recipe, pk=pk)
    user = request.user

    if user.favorite_recipes.filter(pk=recipe.pk).exists():
        user.favorite_recipes.remove(recipe)
        messages.info(request, "Removed from favorites.")
    else:
        user.favorite_recipes.add(recipe)
        messages.success(request, "Added to favorites!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class CategoryListView(generic.ListView):
    """List all categories"""
    model = Category
    template_name = "cookbook/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.annotate(
            recipe_count=Count("recipes")
        ).order_by("name")


class CategoryDetailView(generic.DetailView):
    """Category detail with recipes"""
    model = Category
    template_name = "cookbook/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipes"] = (self.get_object().recipes
                              .select_related("author")
                              .all()
                              )
        return context


class TagListView(generic.ListView):
    """List all tags"""
    model = Tag
    template_name = "cookbook/tag_list.html"
    context_object_name = "tags"

    def get_queryset(self):
        return Tag.objects.annotate(
            recipe_count=Count("recipes")
        ).order_by("name")


class TagDetailView(generic.DetailView):
    """Tag detail with recipes"""
    model = Tag
    template_name = "cookbook/tag_detail.html"
    context_object_name = "tag"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.get_object()
        context["recipes"] = (tag.recipes
                              .select_related("author")
                              .all()
                              )
        return context


class UserDetailView(generic.DetailView):
    """User profile page"""
    model = User
    template_name = "cookbook/user_detail.html"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context.update({
            "user_recipes": user.recipes.all(),
            "total_recipes": user.recipes.count(),
            "favorite_recipes": user.favorite_recipes.all(),
            "total_comments": Comment.objects.filter(author=user).count(),
        })
        return context
