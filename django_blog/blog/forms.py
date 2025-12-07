from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

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