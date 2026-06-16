from django.shortcuts import render

def dashboard(request):
    return render(request, 'transportation/dashboard.html')
