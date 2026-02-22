from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ClientProfile
from .forms import ClientProfileForm

def is_manager_or_admin(user):
    return user.is_superuser or user.groups.filter(name__in=['Admin', 'Manager', 'SuperAdmin']).exists()

@login_required
def client_list(request):
    clients = ClientProfile.objects.all().order_by('-created_at')
    return render(request, 'client_list.html', {'clients': clients})

@login_required
@user_passes_test(is_manager_or_admin)
def client_create(request):
    if request.method == 'POST':
        form = ClientProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientProfileForm()
    return render(request, 'client_form.html', {'form': form, 'title': 'Add New Client'})

@login_required
@user_passes_test(is_manager_or_admin)
def client_edit(request, pk):
    client = get_object_or_404(ClientProfile, pk=pk)
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientProfileForm(instance=client)
    return render(request, 'client_form.html', {'form': form, 'title': 'Edit Client'})

@login_required
@user_passes_test(is_manager_or_admin)
def client_delete(request, pk):
    client = get_object_or_404(ClientProfile, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return redirect('client_list')
