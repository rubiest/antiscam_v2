from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/signin/')
def dashboard(request):
    return render(request,"dashboard.html")