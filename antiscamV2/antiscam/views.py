from django.shortcuts import render, get_object_or_404
from .models import Scammer

def home(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def scammerlist(request):
    scammers = Scammer.objects.all()  # Fetch locations from the database
    context = {'scammers': scammers}

    return render(request,"scammers/index.html", context)

def viewscammer(request, scammer_id):
    scammer = get_object_or_404(Scammer, id=scammer_id)
    return render(request, "scammers/view.html", {'scammer': scammer})