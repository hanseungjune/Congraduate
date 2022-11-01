from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, CustomUserCreationForm 

@require_http_methods(['GET', 'POST'])
def login(request):
  if request.user.is_authenticated:
    return redirect('articles:index')
  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      auth_login(request, form.get_user())
      return redirect('articles:index')
  else:
    form = AuthenticationForm()
  context = {
    'form': form
  }
  return render(request, 'accounts/login.html', context)

@require_POST
def logout(request):
  if request.method == 'POST':
    print(request)
    auth_logout(request)
    return redirect('articles:index')

@require_http_methods(['GET', 'POST'])
def signup(request):
  if request.method == 'POST':
    form = CustomUserCreationForm(data=request.POST)
    if form.is_valid():
      user = form.save()
      # 바로 로그인
      auth_login(request, user)
      return redirect('articles:index')
  else:
    form = CustomUserCreationForm()
  context = {
    'form': form,
  }
  return render(request, 'accounts/signup.html', context)

def delete(request):
    if request.method == 'POST':
      request.user.delete()
      auth_logout(request)
    return redirect('articles:index')

@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
      form = CustomUserChangeForm(request.POST, instance=request.user)
      if form.is_valid():
        form.save()
        return redirect('articles:index')
    else:
      form = CustomUserChangeForm(instance=request.user)
    context = {
      'form':form,
    }
    return render(request, 'accounts/update.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
      form = PasswordChangeForm(request.user, data=request.POST)
      if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        return redirect('articles:index')
    else:
      form = PasswordChangeForm(request.user)
    context = {
      'form':form
    }
    return render(request, 'accounts/change_password.html', context)