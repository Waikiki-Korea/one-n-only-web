from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm, OnoUserChangeForm

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('../../')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

def update(request, pk):
    if request.method == "POST":
        form = OnoUserChangeForm(request.POST, instance=request.user)
        print('1234')
        if form.is_valid():
            print('5678')
            form.save()
            return redirect('../../../')
    else:
        form = OnoUserChangeForm(instance=request.user)
    return render(request, 'common/update.html', {'form': form})