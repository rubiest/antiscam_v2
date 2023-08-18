from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Scammer, Comment, Category, Location, Case
from django.db.models import Q
from .forms import CommentForm
from django.utils import timezone

def home(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def scammerlist(request):
    category_id = request.GET.get('category')
    location_id = request.GET.get('location')
    search_query = request.GET.get('search')

    scammers = Scammer.objects.all()

    if category_id:
        scammers = scammers.filter(category_id=category_id)

    if location_id:
        scammers = scammers.filter(location_id=location_id)

    if search_query:
        scammers = scammers.filter(Q(name__icontains=search_query) | Q(phone__icontains=search_query))

    categories = Category.objects.all()
    locations = Location.objects.all()

    context = {
        'scammers': scammers,
        'categories': categories,
        'locations': locations,
        'selected_category_id': int(category_id) if category_id else None,
        'selected_location_id': int(location_id) if location_id else None,
        'search_query': search_query,
    }

    return render(request,"scammers/index.html", context)

def viewscammer(request, scammer_id):
    scammer = get_object_or_404(Scammer, id=scammer_id)
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_text = comment_form.cleaned_data['comment']
            comment = Comment(user=request.user, scammer=scammer, comment=comment_text)
            comment.save()

    comments = Comment.objects.filter(scammer=scammer)
    cases = Case.objects.filter(scammer=scammer)
    total_votes = scammer.voters.count()
    total_comments = comments.count()
    total_cases = cases.count()
    voters = scammer.voters.all()

    context = {'scammer': scammer, 'comment_form': comment_form, 'comments': comments, 'total_votes': total_votes, 'total_comments': total_comments, 'voters': voters, 'cases': cases, 'total_cases': total_cases}
    return render(request, "scammers/view.html", context)

@login_required(login_url='/signin/')
def vote_unvote_scammer(request, scammer_id):
    scammer = get_object_or_404(Scammer, id=scammer_id)

    if request.user == scammer.reported_by:
        messages.error(request, "You cannot vote for your own scammer entry.")
    else:
        if request.user in scammer.voters.all():
            scammer.votes -= 1
            scammer.voters.remove(request.user)
        else:
            scammer.votes += 1
            scammer.voters.add(request.user)

        scammer.save()
        messages.success(request, "Your vote has been recorded.")

    return redirect('viewscammer', scammer_id=scammer_id)

@login_required(login_url='/signin/')
def newcase(request, scammer_id):
    scammer = get_object_or_404(Scammer, id=scammer_id)
    categories = Category.objects.all()
    context = {'categories': categories, 'scammer': scammer}

    if request.method == "POST":
        account_name = request.POST['account_name']
        account_number = request.POST['account_number']
        bank_name = request.POST['bank_name']
        case_details = request.POST['case_details']
        date_reported = request.POST['date_reported']
        police_report = request.POST.get('police_report') == 'yes'
        reported_by = request.user
        last_date_reported = timezone.now().date()
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)

        case = Case.objects.create(
            account_name=account_name,
            account_number=account_number,
            bank_name=bank_name,
            scammer=scammer,
            case_details=case_details,
            reported_by=reported_by,
            police_report=police_report,
            date_reported=date_reported,
            last_date_reported=last_date_reported,
            category = category
        )
        case.save()

        return redirect('viewscammer', scammer_id=scammer_id)

    return render(request, 'cases/new.html', context)