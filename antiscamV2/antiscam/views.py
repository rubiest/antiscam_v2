from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Scammer, Comment
from .forms import CommentForm

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
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_text = comment_form.cleaned_data['comment']
            comment = Comment(user=request.user, scammer=scammer, comment=comment_text)
            comment.save()

    comments = Comment.objects.filter(scammer=scammer)
    total_votes = scammer.voters.count()
    total_comments = comments.count()
    voters = scammer.voters.all()

    context = {'scammer': scammer, 'comment_form': comment_form, 'comments': comments, 'total_votes': total_votes, 'total_comments': total_comments, 'voters': voters}
    return render(request, "scammers/view.html", context)

@login_required(login_url='/signin/')
def vote_unvote_scammer(request, scammer_id):
    scammer = get_object_or_404(Scammer, id=scammer_id)

    if request.user in scammer.voters.all():
        scammer.votes -= 1
        scammer.voters.remove(request.user)
    else:
        scammer.votes += 1
        scammer.voters.add(request.user)

    scammer.save()

    return redirect('viewscammer', scammer_id=scammer_id)