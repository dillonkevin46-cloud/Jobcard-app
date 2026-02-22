from django.shortcuts import render

def client_list(request):
    return render(request, 'client_list.html')
