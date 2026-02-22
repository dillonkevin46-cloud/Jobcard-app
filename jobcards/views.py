from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import JobcardTemplate
import json

def dashboard(request):
    return render(request, 'dashboard.html')

def jobcard_list(request):
    return render(request, 'jobcard_list.html')

def invoice_list(request):
    return render(request, 'invoice_list.html')

@login_required
def template_builder(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        layout_schema = request.POST.get('layout_schema')

        if name and layout_schema:
            try:
                schema_json = json.loads(layout_schema)
                JobcardTemplate.objects.create(name=name, layout_schema=schema_json)
                return redirect('dashboard')
            except json.JSONDecodeError:
                # Handle error
                pass

    return render(request, 'template_builder.html')
