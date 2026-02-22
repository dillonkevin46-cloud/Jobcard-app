from django.db import models
from django.conf import settings
from clients.models import ClientProfile
from django.utils import timezone

class JobcardTemplate(models.Model):
    name = models.CharField(max_length=255)
    layout_schema = models.JSONField(help_text="Form.io JSON schema")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Jobcard(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PENDING_REVIEW', 'Pending Manager Review'),
        ('PENDING_INVOICING', 'Pending Invoicing'),
        ('ARCHIVED', 'Archived'),
    ]

    jobcard_id = models.CharField(max_length=20, unique=True, editable=False)
    template = models.ForeignKey(JobcardTemplate, on_delete=models.CASCADE)
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_jobcards')
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='jobcards')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    technician_signature = models.ImageField(upload_to='signatures/tech/', null=True, blank=True)
    client_signature = models.ImageField(upload_to='signatures/client/', null=True, blank=True)

    manager_notes = models.TextField(blank=True)
    manager_signature = models.ImageField(upload_to='signatures/manager/', null=True, blank=True)

    invoice_pdf = models.FileField(upload_to='invoices/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.jobcard_id:
            now = timezone.now()
            year = now.year
            # Find the last jobcard created this year
            last_jobcard = Jobcard.objects.filter(jobcard_id__startswith=f"JC-{year}").order_by('jobcard_id').last()
            if last_jobcard:
                last_id = int(last_jobcard.jobcard_id.split('-')[-1])
                new_id = last_id + 1
            else:
                new_id = 1
            self.jobcard_id = f"JC-{year}-{new_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.jobcard_id} - {self.client.name}"

class LineItem(models.Model):
    jobcard = models.ForeignKey(Jobcard, on_delete=models.CASCADE, related_name='line_items')
    who_helped = models.CharField(max_length=255)
    hardware_used = models.CharField(max_length=255, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.who_helped} - {self.quantity}"
