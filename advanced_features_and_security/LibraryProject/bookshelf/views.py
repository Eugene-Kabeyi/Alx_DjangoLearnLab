from django.http import HttpResponse
from django.shortcuts import render
from .models import Book
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Document
from .forms import BookSearchForm

# Create your views here.
def book_list(request):
    """View to display a list of books."""
    books = Book.objects.all()
    context = {'book_list':books}

    return render(request, 'bookshelf/book_list.html', context), HttpResponse("Hello, this is the book list view.")

def search_books(request):
    form = BookSearchForm(request.GET or None)
    books = Book.objects.none()
    if form.is_valid():
        q = form.cleaned_data["q"]
        # Use ORM filtering — parameterized and safe
        if q:
            books = Book.objects.select_related("author").filter(title__icontains=q)
    return render(request, "relationship_app/search_results.html", {"form": form, "books": books})


@permission_required('secure_app.can_view', raise_exception=True)
def view_documents(request):
    docs = Document.objects.all()
    return render(request, "secure_app/view_documents.html", {"documents": docs})


@permission_required('secure_app.can_create', raise_exception=True)
def create_document(request):
    if request.method == "POST":
        Document.objects.create(
            title=request.POST["title"],
            content=request.POST["content"]
        )
        return render(request, "secure_app/success.html")
    return render(request, "secure_app/create_document.html")


@permission_required('secure_app.can_edit', raise_exception=True)
def edit_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)

    if request.method == "POST":
        doc.title = request.POST["title"]
        doc.content = request.POST["content"]
        doc.save()
        return render(request, "secure_app/success.html")

    return render(request, "secure_app/edit_document.html", {"doc": doc})


@permission_required('secure_app.can_delete', raise_exception=True)
def delete_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    doc.delete()
    return render(request, "secure_app/success.html")