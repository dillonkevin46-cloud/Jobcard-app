from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'user_list.html', {'users': users})

@login_required
@user_passes_test(is_superuser)
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_form.html', {'form': form, 'title': 'Add New User'})

@login_required
@user_passes_test(is_superuser)
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'user_form.html', {'form': form, 'title': 'Edit User'})
