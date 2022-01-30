from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from .models import Profile
from django.http import HttpResponse
# Create your views here.

from django import forms
class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
        

def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            skill = request.POST.get("skill")
            print(skill)
            
            # Save user
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            # create user_profile
            profile = Profile(user=user, skill=skill)
            profile.save()
            msg = f'{username} account Created successfully'
            return render(request, 'connect/signup.html', {"form": form, 'msg': msg})
    return render(request, 'connect/signup.html', {"form": form})

class SignInForm(forms.Form):
    username_or_email = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)

from django.db.models import Q
from django.contrib.auth import login, logout

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

def sign_in(request):
    form = SignInForm()
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username_or_email")
            password = form.cleaned_data.get("password")
            
            user = User.objects.filter(Q(username=username) | Q(email=username)).first()
            
            if user:
                if user.check_password(password):
                    login(request, user)
                    # Return user to index page
                    return HttpResponseRedirect(reverse('index', args=[]))
                else: 
                    msg ='Wrong password'
                    return render(request, 'connect/signin.html', {
                        'form': form, 'msg': msg
                    })
            msg ='Wrong username or password'
            return render(request, 'connect/signin.html', {
                        'form': form, 'msg': msg
                    })
            
                    
            
    return render(request, 'connect/signin.html', {
        'form': form
    })
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_img', 'status', 'skill']
    
def index(request):
    if request.user.is_active:
        active='profile'
        form = ProfileForm()
        if request.method == 'POST':
            form = ProfileForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                print(form.cleaned_data)
                img = form.cleaned_data.get('profile_img')
                status = form.cleaned_data.get('status')
                skill = form.cleaned_data.get("skill")
                
                user_profile = Profile.objects.filter(user=request.user).first()            
                user_profile.profile_img = img
                user_profile.status = status
                user_profile.skill = skill
                
                user_profile.save()
            
        return render(request, 'connect/profile.html', {'active': active, 'form': form})
    else:
        return HttpResponseRedirect(reverse('sign_in', args=[]))        



class SearchForm(forms.Form):
    name = forms.CharField(max_length=150)
    
def search(request):
    if request.user.is_active:
        form = SearchForm()
        if request.method == 'POST':
            form = SearchForm(data= request.POST)
            if form.is_valid():
                name = form.cleaned_data.get("name")
                
                # Search users with username like name
                results = User.objects.filter(username__icontains=name).exclude(username=request.user.username).all()
                
                print(results)
                return render(request, 'connect/search.html', {"form": form, 'active': 'search', 'results': results})
                
                
        return render(request, 'connect/search.html', {"form": form, 'active': 'search'})

    return HttpResponseRedirect


def sign_out(request):
    if request.user.is_active:
        logout(request)
    return HttpResponseRedirect(reverse('sign_in', args=[]))


def add_friend(request, id):
    if request.user.is_active:
        user = User.objects.filter(id=id).first()
        if user:
            user_profile = Profile.objects.filter(user=request.user).first()
            if user in user_profile.friends.all():
                return HttpResponse(f'{user} is already a friend')
            else:
                user_profile.friends.add(user)
                user_profile.save()
                return HttpResponse(f'{user} added successfully')
    else:
        return HttpResponseRedirect(reverse('sign_in', args=[]))


class SkillForm(forms.Form):
    skill = forms.CharField(max_length=40, label='Search Skill')
    
def find_skill(request):
    if request.user.is_active:
        form = SkillForm()
        
        if request.method == 'POST':
            form = SkillForm(data=request.POST)
            if form.is_valid():
                skill = form.cleaned_data["skill"]
                
                # Search skill
                search = search_skill(request, skill)
                return render(request, 'connect/find_skill.html', {'form': form, 'active': 'find_skill', 'search': search, 'skill': skill})
                
        return render(request, 'connect/find_skill.html', {'form': form, 'active': 'find_skill'})
    else:
        return HttpResponseRedirect(reverse('sign_in', args=[]))

from collections import deque
def search_skill(request, skill):
    frontier = deque([request.user])
    searched = []
    
    while frontier:
        explore = frontier.popleft()
        explore_profile = explore.profile
        if explore_profile.skill.lower() == skill.lower():
            return explore
        else:
            for friend in explore_profile.friends.all():
                if friend not in searched:
                    frontier.append(friend)
            searched.append(explore)
    
    return 'None'


def friends(request):
    if request.user.is_active:
        friends = request.user.profile.friends.all()
        return render(request, 'connect/friends.html', {"results": friends, 'active': 'friends'})