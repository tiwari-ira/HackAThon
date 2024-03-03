import os
import joblib
import numpy as np
import pandas as pd
from django.shortcuts import render
from .forms import SuccessPredictionForm
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from io import BytesIO
import PyPDF2
import urllib
from datetime import *
import string 
import random 
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from PyPDF2 import PdfFileReader,PdfFileWriter
from django.contrib.auth.decorators import login_required
import os
import json
from django.core.files.storage import FileSystemStorage
import zipfile
import os
import calc.models
from dotenv import load_dotenv
load_dotenv()
import logging
import math
from PIL import Image 
from django.contrib import messages
from datetime import datetime
from calc.models import PDFU,USE
from django.conf import settings
from django.contrib.auth import login 
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate,logout
from sklearn import preprocessing
import smtplib
@csrf_exempt
def log(request):
    global random_filename,a
    res = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k = 16)) 
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        if len(password)>64:
            password=password[:len(password)-16]
        else:
            password=password
        d=request.POST['inp']
        context2={}
        user=authenticate(username=username,password=password)
        try:
            c=str(random_filename[:len(random_filename)-4])
            if user != None:
                if c==d:
                    if user.is_active:
                        request.session.set_expiry(int(os.getenv('Time_Limit')))
                        login(request,user)
                        return redirect('/home/')
                else: 
                        path=os.getenv('m')
                        random_filename = random.choice([
                            x for x in os.listdir(path)
                            if os.path.isfile(os.path.join(path, x))])
                        a="media/"+random_filename
                        context2['ran2']=a
                        context2['error1']='Entered Captha value correctly.'
                        return render(request, "main.html",context2)
            else:
                path=os.getenv('m')
                random_filename = random.choice([
                    x for x in os.listdir(path)
                    if os.path.isfile(os.path.join(path, x))])
                a="media/"+random_filename
                context2['ran2']=a
                context2['error2']='Enter the Username and password Correctly.'
            return render(request, "main.html",context2)
        except OSError:
            context2['error2']='Enter the Username and password Correctly.'
            return render(request, "main.html",context2)
    path=os.getenv('m')
    random_filename = random.choice([
        x for x in os.listdir(path)
        if os.path.isfile(os.path.join(path, x))])
    context={}
    a="media/"+random_filename
    context['ran']=str(res)
    context['ran2']=a
    return render  (request,'main.html',context)

def predict_price(request):
    if request.method == 'POST':
        form = SuccessPredictionForm(request.POST)
        if form.is_valid():
            # Load the trained linear regression model
            model_path = os.path.join(os.path.dirname(__file__), 'models', 'model.pkl')
            model = joblib.load(model_path)
            new_data = list(form.cleaned_data.values())
            #new_data = np.array(list(form.cleaned_data.values())).reshape(1, -1)
            # Extract input data from the form
    #         new_data = np.array(list(form.cleaned_data.values())).reshape(1, -1)
    #         # Convert data into DataFrame
            input_data = pd.DataFrame(new_data[[0]])

    # # Ensure the order of columns matches the training data
    # # You might need to adjust this based on the features used during model training
            expected_columns = ['APPLICATION_TYPE', 'AFFILIATION', 'CLASSIFICATION', 'USE_CASE', 
                         'ORGANIZATION', 'STATUS', 'INCOME_AMT', 'SPECIAL_CONSIDERATIONS', 'ASK_AMT']
            input_data = input_data.reindex(columns=expected_columns)
            le = preprocessing.OrdinalEncoder()
            new_data_1=le.fit_transform(input_data)
            print(new_data_1)
    #         # Perform prediction
            predicted_price = model.predict(new_data_1)[0]

            # Prepare the response
            context = {
                'form': form,
                'predicted_price': predicted_price,
            }
            s = smtplib.SMTP('smtp.gmail.com', 587)
            # start TLS for security
            s.starttls()
            emails = pd.read_csv("media\html sheet - form data.csv")
            es=list(emails['your-email'])
            s.login("email_id", "password")
            message = str(new_data)
            #for i in range(len(emails)):
            #     s.sendmail("ysikhi99@gmail.com", str(emails['your-email']), message)
            print(es)
            s.sendmail("email_id", es, message)
            s.quit()
            return render(request, 'charity.html', context)
    else:
        form = SuccessPredictionForm()

    context = {'form': form}
    return render(request, 'charity.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def change(request):
    res = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k = 16)) 
    if request.method=="POST":
        usern=request.POST["username"]
        psw1 = request.POST["password"]
        psw1=psw1[:len(psw1)-16]
        psw2 = request.POST["password1"]
        psw2=psw2[:len(psw2)-16]
        psw3 = request.POST["password2"]
        psw3=psw3[:len(psw3)-16]
        user=authenticate(username=usern,password=psw1)
        if user != None:
            if psw2==psw3:
                c1 = PDFU.objects.get(username=usern)
                c1.set_password(psw2)
                c1.save()
                return redirect('/home/')
    context={}
    context['ran']=str(res)
    return render(request,'change.html',context)

@csrf_exempt
def reg(request):
    global random_filename,a
    if request.method == "POST":

        usern=request.POST.get("username")
        psw1 = request.POST.get("password")
        print(psw1)
        psw2 = request.POST.get("psw2")
        print(psw2)
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        context2={}
        if email.endswith(os.getenv('e')) or email.endswith(os.getenv('f')):
            if psw1 != psw2:
                messages.warning(request, 'password mismatch')
                context = {
                    'username':usern,
                    'fname' : fname,
                    'lname' : lname,
                    'email':email
                }
                return render(request,"register.html",context)
            else:
                try:
                    c=str(random_filename[:len(random_filename)-4])
                    d=request.POST['inp']
                    if c==d:
                        try:
                            teacher = PDFU()
                            teacher.first_name = fname
                            teacher.last_name = lname
                            teacher.email = email
                            teacher.set_password(psw1)
                            teacher.username = usern
                            teacher.date_joined = datetime.today()
                            teacher.save()
                            messages.add_message(request, messages.INFO, 'Account Created successfully.')
                            return redirect('/',)
                        except:
                            path=os.getenv('m')
                            random_filename = random.choice([
                                x for x in os.listdir(path)
                                if os.path.isfile(os.path.join(path, x))])
                            a=random_filename
                            context2['ran1']=a
                            context2['error']='The username you entered has already been taken. Please try another username.'
                            return render(request, 'register.html',context2)
                    else: 
                        path=os.getenv('m')
                        random_filename = random.choice([
                            x for x in os.listdir(path)
                            if os.path.isfile(os.path.join(path, x))])
                        a=random_filename
                        context2['ran1']=a
                        context2['error1']='Entered Captha value correctly.'
                        return render(request, "register.html",context2)
                except OSError:
                    path=os.getenv('m')
                    random_filename = random.choice([
                        x for x in os.listdir(path)
                        if os.path.isfile(os.path.join(path, x))])
                    a=random_filename
                    context2['ran1']=a
                    context2['error']='The username you entered has already been taken. Please try another username.'
                    return render(request, 'register.html',context2)
        else: 
            context2['error1']='Entered Captha value correctly.'
            return render(request, "register.html",context2)
    path=os.getenv('m')
    random_filename = random.choice([
        x for x in os.listdir(path)
        if os.path.isfile(os.path.join(path, x))])
    a=random_filename
    context1={}
    context1['ran1']=a
    return render(request, "register.html",context1)

@csrf_exempt
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return HttpResponseRedirect('/')
@csrf_exempt
def userid(request):
    now = datetime.now()
    s=str(now.strftime(os.getenv('d')))
    current_user =str(request.user)
    m=current_user+s
    return m
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def home(request):
    return render(request,'home.html')
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def DonorHomePage(request):
    return render(request,'donorHomePage.html')
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def About(request):
    return render(request,'about.html')
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def Charity(request):
    return render(request,'charity.html')
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def DonorLogin(request):
    return render(request,'donorLogin.html')
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def Contact(request):
    return render(request,'Contact.html')
