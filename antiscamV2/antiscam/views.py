from django.shortcuts import redirect, render
# from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from antiscamV2 import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

@login_required(login_url='/signin/')
def dashboard(request):
    return render(request,"dashboard.html")

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if CustomUser.objects.filter(username=username):
            messages.error(request, "Username already exists!")
            return redirect('home')

        if CustomUser.objects.filter(email=email):
            messages.error(request, "Email already exists!")
            return redirect('home')

        if len(username)>20:
            messages.error(request, "Username must be under 20 chars!")
            return redirect('home')

        if password != confirmpassword:
            messages.error(request, "Password didn't match!")

        if not username.isalnum():
            messages.error(request, "Username must be Alphanumeric!")

        myuser = CustomUser.objects.create_user(username,email,password)
        # myuser.first_name = fname
        # myuser.last_name = lname
        myuser.is_active = False
        myuser.token = generate_token.make_token(myuser)
        myuser.save()

        messages.success(request, "Your account has been successfully created. We have sent you a confirmation email! Please check your email.")

        # Welcome email
        subject = "Welcome to Antiscam Application"
        message = "Hello, " + myuser.username + "! \n" + "Welcome to Antiscam Application! \nThank you for register at our website.\nYou will receive another email to confirm your email. Please to do so before log in to the website! \n\nThank you"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email, to_list, fail_silently=True)

        # Confirmation email
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ Antiscam Application"
        message2 = render_to_string('email_confirmation.html',{
            'username': myuser.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            # 'token': generate_token.make_token(myuser),
            'token': myuser.token
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "antiscam/register.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            username = user.username
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials")
            return redirect('home')

    return render(request, "antiscam/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "You has been successfully logged out from the system")
    return redirect('home')
    
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        myuser = None

    if myuser is not None:
        if myuser.is_active:
            # Check if the user is already activated
            return render(request, "antiscam/activation_failed.html", {'error_message': "Your account is already activated."})
        
        if generate_token.check_token(myuser, token):
            myuser.is_active = True
            myuser.save()
            # Revoke the token by setting it to None
            myuser.token = None
            myuser.save()
            messages.success(request, "Your account has been successfully activated. Please login")
            return redirect('signin')
    
    # If user doesn't exist or token is invalid
    return render(request, "antiscam/activation_failed.html")
