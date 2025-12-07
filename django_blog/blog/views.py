from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse_lazy # for redirecting after registration
from .forms import RegistrationForm, UserUpdateForm, ProfileForm, CommentForm, PostForm  #Create your views here.
# Generic class-based views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Mixins for permission checks
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Tag

from django.db.models import Q
# ----------------------------
# Registration view (custom)
# ----------------------------
def register(request):
    """
   Show registration form and create user.
    Uses RegistrationForm (extends UserCreationForm).
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            login(request, user)  # Log the user in after registration
            messages.success(request, f'Account created for {user.username}!')
            return redirect(reverse_lazy('profile'))  # Redirect to home page after registration
        
        else:
            return render(request, 'blog/register.html', {'form': form})
    else: 
        form = RegistrationForm()
        return render(request, 'blog/register.html', {'form': form})
    
# ----------------------------
# Profile view (view & edit)
# ----------------------------
@login_required
def profile(request):
    """
    Show and edit user profile.
    Uses UserUpdateForm and ProfileForm.
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user) # Bind to current user
        p_form = ProfileForm(request.POST, instance=request.user.profile) # Bind to current user's profile
        
        # Validate and save forms
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')  # Redirect to profile page after update
        else:
            messages.error(request, f'Please correct the error below.')
            
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)
    
    # Prepare context for rendering
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'blog/profile.html', context)

# ----------------------------
# Add comment view  
# ---------------------------
@login_required
def add_comment(request):
    """
    View to add a comment.
    Uses CommentForm.
    """
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Associate comment with logged-in user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('some_view_name')  # Replace with appropriate view name
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CommentForm()
    
    return render(request, 'blog/add_comment.html', {'form': form})

#----------------------------
# Edit comment view
#---------------------------
@login_required
def edit_comment(request, comment_id):
    """
    View to edit an existing comment.
    Uses CommentForm.
    """
    from .models import Comment  # Importing here to avoid circular imports
    comment = Comment.objects.get(id=comment_id, user=request.user)  # Ensure user can only edit their own comments
    
    if comment.author != request.user:
        return redirect('blog/post-detail.html', pk=comment.post.id)  # only author can edit
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been updated!')
            return redirect('blog/post-detail.html', pk=comment.post.id)  # Replace with appropriate view name
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'blog/edit_comment.html', {'form': form})


# ----------------------------
# Delete comment view
# ---------------------------
@login_required
def delete_comment(request, comment_id):
    """
    View to delete an existing comment.
    """
    from .models import Comment  # Importing here to avoid circular imports
    comment = Comment.objects.get(id=comment_id, user=request.user)  # Ensure user can only delete their own comments
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment has been deleted!')
        return redirect('blog/add_comment.html')  # Replace with appropriate view name
    
    return render(request, 'blog/post_detail.html', {'comment': comment})


# -------------------------
# List all posts (public)
# -------------------------
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'   # <app>/<template>.html
    context_object_name = 'posts'
    ordering = ['-published_date']          # newest first
    paginate_by = 5                         # optional: 5 posts per page


# -------------------------
# Single post detail (public)
# -------------------------
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


# -------------------------
# Create a new post (authenticated users only)
# -------------------------
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    # where to go after successful creation
    # reverse_lazy to avoid resolving url at import time
    success_url = reverse_lazy('post-list')

    # set author automatically to current logged-in user
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Post created successfully.")
        return response


# -------------------------
# Update view: only the author may edit
# -------------------------
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

    # UserPassesTestMixin calls this to check permission
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to edit this post.")
        return redirect('post-detail', pk=self.get_object().pk)


# -------------------------
# Delete view: only the author may delete
# -------------------------
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to delete this post.")
        return redirect('post-detail', pk=self.get_object().pk)
 
 #-------------------------
 # Search view (public)
 #------------------------   
class SearchView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context
  
#-------------------------
# List posts by tag (public)   
#------------------------   
class PostListByTagView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        return Post.objects.filter(tags__name=tag_name)
