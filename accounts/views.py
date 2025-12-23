from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy

from cookbook.models import Recipe
from .forms import SignUpForm, UserUpdateForm


class SignUpView(generic.CreateView):
    """User registration view"""
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        messages.success(
            self.request, 
            "Обліковий запис успішно створено! "
            "Please log in."
        )
        return super().form_valid(form) # noqa


@login_required
def profile_view(request):
    """Current user"s profile view"""
    user_recipes = Recipe.objects.filter(author=request.user)
    favorite_recipes = request.user.favorite_recipes.all()

    context = {
        "profile_user": request.user,
        "user_recipes": user_recipes,
        "favorite_recipes": favorite_recipes,
        "total_recipes": user_recipes.count(),
        "total_comments": request.user.comments.count(),
    }
    return render(
        request, 
        "registration/profile.html", 
        context
    )


@login_required
def profile_update(request):
    """Update user profile view"""
    if request.method == "POST":
        form = UserUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                "Профіль успішно оновлено!"
            )
            return redirect("cookbook:user-detail", pk=request.user.pk)
    else:
        form = UserUpdateForm(instance=request.user)

    return render(
        request, 
        "cookbook/profile_update.html", 
        {"form": form}
    )
