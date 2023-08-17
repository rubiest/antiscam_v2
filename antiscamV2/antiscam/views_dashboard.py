from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Scammer, Location, Category
from django.contrib import messages
from .forms import SearchCreateScammerForm

@login_required(login_url='/signin/')
def dashboard(request):
    return render(request,"dashboard.html")

@login_required(login_url='/signin/')
def profile(request):
    user = request.user
    reported_scammers = Scammer.objects.filter(reported_by=user)
    voted_scammer_ids = user.voted_scammers.values_list('id', flat=True)
    voted_scammers = Scammer.objects.filter(id__in=voted_scammer_ids)

    context = {'reported_scammers': reported_scammers, 'voted_scammers': voted_scammers}

    return render(request,"profile.html", context)

@login_required(login_url='/signin/')
def newscammer(request):
    locations = Location.objects.all()  # Fetch locations from the database
    categories = Category.objects.all()  # Fetch locations from the database
    context = {'locations': locations, 'categories': categories}
    
    # Check if the pre-filled phone number is stored in the session
    pre_filled_phone = request.session.get('pre_filled_phone', '')
    
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
        if Scammer.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists!")
        elif not phone.isdigit():
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
        return redirect('scammerlist')

    context['pre_filled_phone'] = pre_filled_phone
    return render(request,"scammers/new.html", context)

@login_required(login_url='/signin/')
def search_create_scammer(request):
    if request.method == 'POST':
        form = SearchCreateScammerForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            # Check if a scammer with the provided phone number exists
            existing_scammer = Scammer.objects.filter(phone=phone).first()
            if existing_scammer:
                # Scammer with the given phone number already exists
                return redirect('viewscammer', scammer_id=existing_scammer.id)
            else:
                # Store the pre-filled phone number in the session
                request.session['pre_filled_phone'] = phone
                return redirect('newscammer')
    else:
        form = SearchCreateScammerForm()

    return render(request, 'search_create_scammer.html', {'form': form})