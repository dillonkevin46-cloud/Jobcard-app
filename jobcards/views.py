from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .models import JobcardTemplate, Jobcard, LineItem
from clients.models import ClientProfile
from .utils import generate_pdf
import json
import base64
from django.core.files.base import ContentFile

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def jobcard_list(request):
    jobcards = Jobcard.objects.all().order_by('-created_at')
    return render(request, 'jobcard_list.html', {'jobcards': jobcards})

@login_required
def invoice_list(request):
    # Filter for jobcards that are 'ARCHIVED' or 'PENDING_INVOICING' - assuming these have invoices
    invoices = Jobcard.objects.exclude(invoice_pdf='').order_by('-created_at')
    return render(request, 'invoice_list.html', {'invoices': invoices})

@login_required
def jobcard_create(request):
    if request.method == 'POST':
        client_id = request.POST.get('client')
        template_id = request.POST.get('template')
        if client_id and template_id:
            return redirect('jobcard_fill', template_id=template_id, client_id=client_id)
        else:
            messages.error(request, 'Please select both a client and a template.')

    clients = ClientProfile.objects.all()
    templates = JobcardTemplate.objects.all()
    return render(request, 'jobcard_create_step1.html', {'clients': clients, 'templates': templates})

@login_required
def jobcard_fill(request, template_id, client_id):
    template = get_object_or_404(JobcardTemplate, pk=template_id)
    client = get_object_or_404(ClientProfile, pk=client_id)

    if request.method == 'POST':
        submission_data = request.POST.get('submission_data')
        if submission_data:
            try:
                data = json.loads(submission_data)

                # Create Jobcard
                jobcard = Jobcard.objects.create(
                    template=template,
                    technician=request.user,
                    client=client,
                    status='PENDING_REVIEW',
                    start_time=data.get('startTime'),
                    end_time=data.get('endTime')
                )

                # Create Line Items
                work_items = data.get('workItems', [])
                for item in work_items:
                    LineItem.objects.create(
                        jobcard=jobcard,
                        who_helped=item.get('whoHelped', ''),
                        hardware_used=item.get('hardware', ''),
                        quantity=int(item.get('qty', 1))
                    )

                # Handle Signatures (Base64)
                if data.get('clientSignature'):
                    try:
                        format, imgstr = data.get('clientSignature').split(';base64,')
                        ext = format.split('/')[-1]
                        data_img = ContentFile(base64.b64decode(imgstr), name=f'client_sig.{ext}')
                        jobcard.client_signature = data_img
                    except ValueError:
                        pass

                if data.get('techSignature'):
                    try:
                        format, imgstr = data.get('techSignature').split(';base64,')
                        ext = format.split('/')[-1]
                        data_img = ContentFile(base64.b64decode(imgstr), name=f'tech_sig.{ext}')
                        jobcard.technician_signature = data_img
                    except ValueError:
                        pass

                jobcard.save()

                # Generate PDF
                pdf_content = generate_pdf(jobcard, data)
                filename = f'{jobcard.jobcard_id}.pdf'
                jobcard.invoice_pdf.save(filename, ContentFile(pdf_content))
                jobcard.save()

                # Send Email
                try:
                    email = EmailMessage(
                        subject=f'Jobcard Completed: {jobcard.jobcard_id}',
                        body=f'Dear {client.contact_person},\n\nPlease find attached the jobcard for the recent service.\n\nRegards,\nServiceForge Team',
                        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@serviceforge.com',
                        to=[client.email],
                    )
                    email.attach(filename, pdf_content, 'application/pdf')
                    email.send(fail_silently=True)
                    messages.success(request, f'Jobcard created and emailed to {client.email}.')
                except Exception as e:
                    messages.warning(request, f'Jobcard created, but failed to send email: {e}')

                return redirect('dashboard')

            except json.JSONDecodeError:
                messages.error(request, 'Invalid submission data.')
            except Exception as e:
                messages.error(request, f'Error creating jobcard: {e}')

    return render(request, 'jobcard_fill.html', {'template': template, 'client': client, 'schema_json': json.dumps(template.layout_schema)})

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

    schema_json = "{}"
    return render(request, 'template_builder.html', {'schema_json': schema_json})

@login_required
def template_list(request):
    templates = JobcardTemplate.objects.all().order_by('-created_at')
    return render(request, 'template_list.html', {'templates': templates})

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
