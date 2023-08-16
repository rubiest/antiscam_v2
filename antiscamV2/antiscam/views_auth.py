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
from .tokens import generate_token
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        phone = request.POST['phone']
        location = request.POST['location']

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
        elif len(username) > 20:
            messages.error(request, "Username must be under 20 chars!")
        elif password != confirmpassword:
            messages.error(request, "Password didn't match!")
        elif not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
        elif not phone.isdigit():
            messages.error(request, "Phone Number must be a number!")
        else:
            myuser = CustomUser.objects.create_user(username, email, password)
            myuser.first_name = request.POST['fname']
            myuser.last_name = request.POST['lname']
            myuser.phone = phone
            myuser.location = location
            myuser.is_active = False
            myuser.token = generate_token.make_token(myuser)
            myuser.save()
            
        # Send Welcome email
        subject = "Welcome to Antiscam Application"
        message = f"Hello, {myuser.username}!\nWelcome to Antiscam Application! Thank you for registering on our website. You will receive another email to confirm your email address before logging in.\n\nThank you"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [myuser.email], fail_silently=True)

        # Send Confirmation email
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ Antiscam Application"
        message2 = render_to_string('email_confirmation.html', {
            'username': myuser.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': myuser.token
        })
        email = EmailMessage(email_subject, message2, settings.EMAIL_HOST_USER, [myuser.email])
        email.fail_silently = True
        email.send()

        messages.success(request, "Your account has been successfully created. We have sent you a confirmation email! Please check your email.")
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

@login_required(login_url='/signin/')
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        new_first_name  = request.POST['fname']
        new_last_name = request.POST['lname']
        new_phone = request.POST['phone']
        new_location = request.POST['location']
        new_username = request.POST['username']
        new_email = request.POST['email']

        if new_username != user.username and CustomUser.objects.filter(username=new_username).exists():
            messages.error(request, "Username already exists!")
        elif new_email != user.email and CustomUser.objects.filter(email=new_email).exists():
            messages.error(request, "Email already exists!")
        elif len(new_username) > 20:
            messages.error(request, "Username must be under 20 chars!")
        elif not new_username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
        elif not new_phone.isdigit():
            messages.error(request, "Phone Number must be a number!")
        else:
            if (new_first_name and new_first_name != user.first_name) or \
               (new_last_name and new_last_name != user.last_name) or \
               (new_phone and new_phone != user.phone) or \
               (new_location and new_location != user.location) or \
               (new_username and new_username != user.username) or \
               (new_email and new_email != user.email):
                # Check if username or email changed
                if new_username != user.username or new_email != user.email:
                    # Send email notification
                    send_email_notification(user, new_username, new_email)

                # Update user profile
                user.first_name = new_first_name
                user.last_name = new_last_name
                user.phone = new_phone
                user.location = new_location
                user.username = new_username
                user.email = new_email
                user.save()
                messages.success(request, "Profile updated successfully.")
            else:
                messages.info(request, "No changes were made to the profile.")

        return redirect('profile')
    
    return render(request, "edit_profile.html")

def send_email_notification(user, new_username, new_email):
    subject = "Profile Information Update"
    message = f"Dear {user.username},\n\nYour profile information has been updated.\n\n"
    if new_username != user.username:
        message += f"New Username: {new_username}\n"
    if new_email != user.email:
        message += f"New Email: {new_email}\n"
    message += "\nThank you for using our platform!"
    from_email = settings.EMAIL_HOST_USER
    to_list = [user.email]
    send_mail(subject, message, from_email, to_list, fail_silently=True)