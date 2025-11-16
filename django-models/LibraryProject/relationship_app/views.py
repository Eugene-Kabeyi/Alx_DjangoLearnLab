from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.shortcuts import render, redirect

# ----------------------------------------
# FUNCTION-BASED VIEW: List All Books
# ----------------------------------------
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# ----------------------------------------
# CLASS-BASED VIEW: Library Detail
# ----------------------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    # Optionally customize context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# ----------------------------------------
# USER REGISTRATION VIEW
# ----------------------------------------
class RegisterView(FormView):
    template_name = "relationship_app/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("list_books")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Auto login
        return super().form_valid(form)

def register(request):
    UserCreationForm()
    return RegisterView.as_view(template_name="relationship_app/register.html")(request)
# ----------------------------------------
# LOGIN VIEW
# ----------------------------------------
class LoginView(FormView):
    template_name = "relationship_app/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("list_books")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

# ----------------------------------------
# LOGOUT VIEW
# ----------------------------------------
class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, "relationship_app/logout.html")