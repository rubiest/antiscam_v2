from django.shortcuts import render
from .models import Scammer

def home(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def scammerlist(request):
    scammers = Scammer.objects.all()  # Fetch locations from the database
    context = {'scammers': scammers}

    return render(request,"scammers/index.html", context)