from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

def jobcard_list(request):
    return render(request, 'jobcard_list.html')

def invoice_list(request):
    return render(request, 'invoice_list.html')
