from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse_lazy # for redirecting after registration
from .forms import RegistrationForm, UserUpdateForm, ProfileForm  #Create your views here.

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