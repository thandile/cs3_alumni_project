from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from alumni.models import Profile
from django.http import HttpResponseRedirect
from django import forms



# Create your views here.

class UserForm(forms.Form):
        username = forms.CharField(max_length=50)
        email = forms.EmailField(max_length=50)
        password = forms.CharField(max_length=32, widget=forms.PasswordInput)
        first_name = forms.CharField(max_length=50, label = "first name")
        last_name = forms.CharField(max_length=50, label = "last name")


class ProfileForm(forms.Form):
        degree = forms.CharField(max_length=50)
        grad_year = forms.IntegerField(label= "graduation year")
        city = forms.CharField(max_length=50)
        country = forms.CharField(max_length=50)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

'''
from forms import UserForm

def lexusadduser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(new_user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('main.html')
    else:
        form = UserForm() 

    return render(request, 'adduser.html', {'form': form}) 
'''


def create(request):
    form = UserForm()
    if request.method == "POST":
		# then they are sending data, create a new user
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, "../templates/alumni/toProfile.html", {'userid' : new_user.id, 'username' : new_user.first_name})
    else:
        # they are requesting the page, give
        form = UserForm()
    return render(request, '../templates/alumni/create.html', {'form': form})


def index(request):
    return HttpResponse("Hello, world. You're at the alumni index.")


def logout_view(request):
    logout(request)


def create_profile(request):  #create profile
    user = User.objects.latest('pk')
    prof_form = ProfileForm()
    if request.method == "POST":

        prof_form = ProfileForm(request.POST)
        profile = Profile(city = request.POST.get("city"), country = request.POST.get("country"),
                    degree = request.POST.get("degree"), grad_year = request.POST.get("grad_year"),
                          user_id = user.id )
        profile.save()
        user_info = Profile.objects.get(user_id=user.id)
        name = user.first_name
        surname = user.last_name
        email = user.email
        city = user_info.city
        country = user_info.country
        degree = user_info.degree
        grad_year = user_info.grad_year
        return render(request, '../templates/alumni/profile.html', {'name' : name, 'surname' : surname, 'email' : email, 'city': city, "country": country, "degree" : degree, "grad_year": grad_year} )
    else:
        prof_form = ProfileForm()
        return render(request, '../templates/alumni/createProfile.html', {'form': prof_form})

def profile(request):   #view profile info
    if request.method =="POST":
        pass
    else:
        user = request.user
        user_info = Profile.objects.get(user_id =user.id)
        name = user.first_name
        surname = user.last_name
        email = user.email
        city = user_info.city
        country = user_info.country
        degree = user_info.degree
        grad_year = user_info.grad_year
        return render(request, '../templates/alumni/profile.html', {'name' : name, 'surname' : surname, 'email' : email, 'city': city, "country": country, "degree" : degree, "grad_year": grad_year} )


def view_profile(request):
#view profile info
    if request.method =="POST":
        pass
    else:
        form = ProfileForm()
        user = request.user
        user_info = Profile.objects.get(user_id =user.id)
        form.name = user.first_name
        form.surname = user.last_name
        form.email = user.email
        form.city = user_info.city
        form.country = user_info.country
        form.degree = user_info.degree
        form.grad_year = user_info.grad_year
        return render(request, '../templates/alumni/createProfile.html', {'form': form})

        #return render(request, '../templates/alumni/profile.html', {'name' : name, 'surname' : surname, 'email' : email, 'city': city, "country": country, "degree" : degree, "grad_year": grad_year} )

    if request.method == 'POST':
           degree = forms.CharField(required = True)
           city = forms.CharField(required = True)
           grad_year = forms.DateTimeField(required = True)
           country = forms.CharField(required = True)
           profile = Profile(city = request.POST.get("city"), country = request.POST.get("country"), \
           degree = request.POST.get("degree"), grad_year = request.POST.get("grad_year"), user_id =2)#,\
                        #photo = request.FILES['photo']) #link profile to user
           profile.save()
           return HttpResponse("Your profile has been Edited")




def log_in(request):
    log_in = LoginForm()
    if request.method == "POST":
        log_in = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return render(request,'../templates/alumni/homepage.html', {'username' : username})
    else:
        log_in = LoginForm()
        return render(request, '../templates/alumni/login.html', {'form':log_in})


def home(request):
    return render(request, '../templates/alumni/homepage.html')