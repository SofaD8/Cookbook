from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy

from cookbook.models import Recipe, User
from .forms import SignUpForm, UserUpdateForm


class SignUpView(generic.CreateView):
    """User registration view"""
    form_class = SignUpForm
    success_url = reverse_lazy("accounts:login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        messages.success(
            self.request,
            "Account created successfully! "
            "Please log in."
        )
        return super().form_valid(form) # noqa


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    """Current user's profile view"""
    template_name = "registration/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_recipes = Recipe.objects.filter(author=user)

        context.update({
            "profile_user": user,
            "user_recipes": user_recipes,
            "favorite_recipes": user.favorite_recipes.all(),
            "total_recipes": user_recipes.count(),
            "total_comments": user.comments.count(),
        })
        return context


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Update user profile view"""
    model = User
    form_class = UserUpdateForm
    template_name = "cookbook/profile_update.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(
            self.request,
            "Profile updated successfully!")
        return reverse_lazy(
            "cookbook:user-detail",
            kwargs={"pk": self.request.user.pk})
