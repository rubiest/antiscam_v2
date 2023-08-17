from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Scammer, Location, Category
from django.contrib import messages

@login_required(login_url='/signin/')
def dashboard(request):
    return render(request,"dashboard.html")

@login_required(login_url='/signin/')
def profile(request):
    return render(request,"profile.html")

@login_required(login_url='/signin/')
def newscammer(request):
    locations = Location.objects.all()  # Fetch locations from the database
    categories = Category.objects.all()  # Fetch locations from the database
    context = {'locations': locations, 'categories': categories}
    
    if request.method == "POST":
        name = request.POST['name']
        brief = request.POST['brief']
        modus = request.POST['modus']
        phone = request.POST['phone']
        date_reported = request.POST['date_reported']
        last_date_reported = timezone.now().date()
        location_id = request.POST['location']
        location = Location.objects.get(id=location_id)
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)

        # Get the currently logged-in user
        reported_by = request.user
        if not phone.isdigit():
            messages.error(request, "Phone Number must be a number!")
        else:
            scammer = Scammer.objects.create(
                name=name,
                reported_by=reported_by,
                brief_intro=brief,
                modus_operandi=modus,
                date_reported=date_reported,
                last_date_reported=last_date_reported,
                phone = phone,
                location = location,
                category = category
            )
            scammer.save()
        
        # Redirect to a success page or another view
        return redirect('/scammer-lists/')

    return render(request,"scammers/new.html", context)