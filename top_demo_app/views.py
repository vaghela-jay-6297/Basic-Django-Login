from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import contact, User
from django.conf import settings
from django.core.mail import send_mail
import random

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact_us(request):
    if request.method == 'POST':
        contact.objects.create(email=request.POST['email'],
                                name=request.POST['name'],
                                message=request.POST['message'])
        success_mes = "Your Message Successfully Send..."
        return render(request, 'contact-us.html', {'success_mes': success_mes})
    else:
        return render(request, 'contact-us.html')


def sign_up(request):
    if request.method=="POST":  # check form request is post or not?
        try:             # here check email is registered or not!
            reg_mail = User.objects.get(email=request.POST['email'])
            warning_mes = "Email is Already Registered!"
            return render(request, 'sign-up.html', {'warning_mes': warning_mes})
        except:         # execute this block when user is not registered!
            if request.POST['password']==request.POST['cpassword']:     # check password & cpassword is match or not?
                User.objects.create(email=request.POST['email'],    # create user in DB
                                fname=request.POST['fname'],
                                lname=request.POST['lname'],
                                address=request.POST['address'],
                                password=request.POST['password'],)
                success_mes = "User Successfully Registered!"
                return render(request, 'login.html', {'success_mes': success_mes})
            else:
                warning_mes = "Password & Confirm Password Does not Matched!"
                return render(request, 'sign-up.html', {'warning_mes': warning_mes})
    else:
        return render(request, 'sign-up.html')

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user_mail = User.objects.get(email=email)   # Check email is registered or not? get method return single object.
        if user_mail.password == password:        # here check registered user DB password & enter password!
            request.session['email'] = user_mail.email    # create session variable with registered email
            request.session['fname'] = user_mail.fname  # create session variable(fname) with user registered fname from DB.
            return render(request, 'index.html')
        else:
            warning_mes = "Invalid Password"
            return render(request, 'login.html', {'warning_mes': warning_mes})
    else:
        return render(request, 'login.html')
    
def logout(request):
    # automatically session is destroy within 5min if you not press any key or mouse pad so that's why we use try and except block.
    try:     # when session is activate. if session is not activate then execute except block.
        del request.session['email']    # delete session
        del request.session['fname']    # delete session
        return render(request, 'login.html')
    except:
        success_mes = "User Logged out Successfully!"
        return render(request, 'login.html', {'success_mes':success_mes}) 
    
def forgot_password(request):
    if request.method=="POST":
        try:
            # if user's email is register then execute this block.
            user_mail = User.objects.get(email=request.POST['email'])
            otp = random.randint(100000, 999999)        # Generate 6 digit random OTP.
            subject = 'Forgot Password OTP'     # subject of sending email
            message = f'Hi {user_mail.fname}, Your OTP is'+ ' ' + str(otp)  # body of email
            email_from = settings.EMAIL_HOST_USER   # fetch given host email from seeting.py file.
            recipient_list = [user_mail.email, ]       # list of recipient emails
            send_mail( subject, message, email_from, recipient_list )   # send_mail to send mail to registered user email.
            success_mes = "OTP Successfully Send on your registered Email."
            return render(request, 'otp.html', {'success_mes':success_mes, 'otp': otp, 'email': user_mail.email})
        except:
            # if user's email is not register then execute this block.
            warning_mes = "This Email is not Registered. Please Check Email!"
            return render(request, 'forgot-password.html', {'warning_mes':warning_mes})
    else:
        return render(request, 'forgot-password.html')
    
def verify_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = int(request.POST['otp'])
        cotp = int(request.POST['cotp'])
        if cotp == otp:
            return render(request, 'new-password.html', {'email': email})
        else:
            warning_mes = "Your Entered OTP is Invalid. Please Try again!"
            return render(request, 'otp.html',{'warning_mes':warning_mes, 'otp': otp, 'email': email})
    else:
        return render(request, 'otp.html')

def new_password(request):
    if request.method=='POST':
        email = request.POST['email']
        np = request.POST['new_password']
        cnp = request.POST['new_cpassword']
        if np == cnp:
            user_mail = User.objects.get(email=email)
            user_mail.password = np
            user_mail.save()
            success_mes = "Password Successfully Updated!"
            return render(request, 'login.html', {'success_mes':success_mes})
        else:
            warning_mes = "Password & Confirm Password Does not Matched!"
            return render(request, 'new-password.html', {'warning_mes':warning_mes})
    else:
        return render(request, 'new-password.html')
    
def change_password(request):
    if request.method == 'POST':
        email = request.session['email']
        new_password = request.POST['new_password']
        cnew_password = request.POST['cnew_password']
        user = User.objects.get(email=email)
        if request.POST['old_password'] == user.password:
            if new_password == cnew_password:
                user.password = new_password
                user.save()
                return redirect('logout')
            else:
                warning_mes = "New Password & Confirm New Password Does not Matched!"
                return render(request, 'change-password.html', {'warning_mes':warning_mes})
        else:
            warning_mes = "Invalid Old Password"
            return render(request, 'change-password.html', {'warning_mes':warning_mes})
    else:
        return render(request, 'change-password.html')