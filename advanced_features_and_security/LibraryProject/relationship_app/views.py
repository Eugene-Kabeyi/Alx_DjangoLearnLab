from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book, Author

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
    template_name = "relationship_app/logout.html"  # <-- Add this

    def get(self, request):
        logout(request)
        return render(request, self.template_name)

    
# ----------------------------------------
# HELPER FUNCTIONS FOR ROLE CHECKING
# ----------------------------------------

def is_admin(user):
    return user.is_authenticated and user.profile.role == "Admin"

def is_librarian(user):
    return user.is_authenticated and user.profile.role == "Librarian"

def is_member(user):
    return user.is_authenticated and user.profile.role == "Member"


# ----------------------------------------
# ROLE-SPECIFIC VIEWS
# ----------------------------------------

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")

# ----------------------------------------
# ADD BOOK VIEW (Requires can_add_book)
# ----------------------------------------
@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author_id = request.POST.get("author")
        author = Author.objects.get(id=author_id)

        Book.objects.create(title=title, author=author)
        return redirect("list_books")

    authors = Author.objects.all()
    return render(request, "relationship_app/add_book.html", {"authors": authors})


# ----------------------------------------
# EDIT BOOK VIEW (Requires can_change_book)
# ----------------------------------------
@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.title = request.POST.get("title")
        author_id = request.POST.get("author")
        book.author = Author.objects.get(id=author_id)
        book.save()
        return redirect("list_books")

    authors = Author.objects.all()
    return render(request, "relationship_app/edit_book.html", {"book": book, "authors": authors})


# ----------------------------------------
# DELETE BOOK VIEW (Requires can_delete_book)
# ----------------------------------------
@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect("list_books")