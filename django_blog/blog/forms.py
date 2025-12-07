from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Comment, Post

# -----------------------
# Registration form
# -----------------------
# We extend the built-in UserCreationForm to add an email field.
class RegistrationForm (UserCreationForm):
    email = forms.EmailField(required =True) # Make email required  
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    # Override the save method to save the email field
    def save(self, commit =True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    

# -----------------------
# Profile edit form
# -----------------------
class UserUpdateForm(forms.ModelForm):
    
    # Form to update username and email
    class Meta:
        model = User
        fields = ['username', 'email']
        # Add some Bootstrap classes to the form fields
        widgets= {
            'username': forms.TextInput(attrs={'class': 'form-control'}), # Add Bootstrap class
            'email': forms.EmailInput(attrs={'class': 'form-control'}), # Add Bootstrap class
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']
        widgets= {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), # Add Bootstrap class
        }
        
# -----------------------
# Comment form  
# -----------------------
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a comment...'}),
        }
        
# Simple Post form using ModelForm (beginner-friendly)
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # We omit author because we will set it automatically in the view
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your post here...', 'class': 'form-control', 'rows': 8}),
        }