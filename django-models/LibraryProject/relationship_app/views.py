from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library

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
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after register
            return redirect("list_books")  # Redirect anywhere you prefer
    else:
        form = UserCreationForm()

    return render(request, "relationship_app/register.html", {"form": form})


# ----------------------------------------
# LOGIN VIEW
# ----------------------------------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("list_books")
    else:
        form = AuthenticationForm()

    return render(request, "relationship_app/login.html", {"form": form})


# ----------------------------------------
# LOGOUT VIEW
# ----------------------------------------
def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")
