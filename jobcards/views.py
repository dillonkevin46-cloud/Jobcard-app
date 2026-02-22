from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobcardTemplate
import json

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def jobcard_list(request):
    return render(request, 'jobcard_list.html')

@login_required
def invoice_list(request):
    return render(request, 'invoice_list.html')

@login_required
def template_list(request):
    templates = JobcardTemplate.objects.all().order_by('-created_at')
    return render(request, 'template_list.html', {'templates': templates})

@login_required
def template_builder(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        layout_schema = request.POST.get('layout_schema')

        if name and layout_schema:
            try:
                schema_json = json.loads(layout_schema)
                JobcardTemplate.objects.create(name=name, layout_schema=schema_json)
                messages.success(request, 'Template saved successfully!')
                return redirect('template_list')
            except json.JSONDecodeError:
                messages.error(request, 'Invalid template schema.')
        else:
            messages.error(request, 'Please provide both a name and a layout.')

    # Use empty schema for new template
    schema_json = "{}"
    return render(request, 'template_builder.html', {'schema_json': schema_json})

@login_required
def template_edit(request, pk):
    template = get_object_or_404(JobcardTemplate, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        layout_schema = request.POST.get('layout_schema')

        if name and layout_schema:
            try:
                schema_json = json.loads(layout_schema)
                template.name = name
                template.layout_schema = schema_json
                template.save()
                messages.success(request, 'Template updated successfully!')
                return redirect('template_list')
            except json.JSONDecodeError:
                messages.error(request, 'Invalid template schema.')
        else:
            messages.error(request, 'Please provide both a name and a layout.')

    # Convert existing layout schema to JSON string for the frontend
    schema_json = json.dumps(template.layout_schema)
    return render(request, 'template_builder.html', {'template': template, 'schema_json': schema_json})

@login_required
def template_delete(request, pk):
    template = get_object_or_404(JobcardTemplate, pk=pk)
    if request.method == 'POST':
        template.delete()
        messages.success(request, 'Template deleted successfully!')
        return redirect('template_list')
    return redirect('template_list')
