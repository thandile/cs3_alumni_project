from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import login
from django.contrib.auth.models import User
from alumni.models import Profile
from django.http import HttpResponseRedirect
from django import forms

import autocomplete_light as AL

# Create your views here.

'''
class UserCreationForm(forms.Form):
# instead of autocomplete light, see the following

# http://stackoverflow.com/questions/11287485/taking-user-input-to-create-users-in-django
user = AL.ModelMultipleChoiceField(autocomplete='UserAutocomplete')
'''

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')#, 'name', 'surname')

class ProfileForm(forms.Form):
        degree = forms.CharField(max_length=50, label= "degree")
        grad_year = forms.IntegerField(label= "graduation year")
        city = forms.CharField(max_length=50)
        country = forms.CharField(max_length=50)
        #photo = forms.ImageField()

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
            #login(new_user)
            return HttpResponse("User successfully created.")
            # redirect, or however you want to get to the main view
            #return HttpResponseRedirect('index.html')
    else:
        # they are requesting the page, give
        form = UserForm()
    return render(request, '../templates/alumni/create.html', {'form': form})
#return HttpResponse("You're looking at question %s." % question_id)


def index(request):
    return HttpResponse("Hello, world. You're at the alumni index.")


def profile(request):
    form = UserForm()
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        #if form.is_valid():
           # return HttpResponse(form.cleaned_data[""])
        profile = Profile(city = request.POST.get("city"), country = request.POST.get("country"), \
                    degree = request.POST.get("degree"), grad_year = request.POST.get("grad_year"), user_id =2)#,\
                    #photo = request.FILES['photo']) #link profile to user
        profile.save()
        return HttpResponse("Your profile has been submitted")
    else:
        form = ProfileForm()
        return render(request, '../templates/alumni/createProfile.html', {'form': form})
