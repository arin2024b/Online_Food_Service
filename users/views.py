from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm, AddressForm
from .models import Address
from django.contrib.auth import get_user_model
from orders.models import Order

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    addresses = user.addresses.all()
    orders = Order.objects.filter(user=user).order_by('-timestamp')
    return render(request, 'users/profile.html', {'form': form, 'addresses': addresses, 'orders': orders})

@login_required
def add_address_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added!')
            return redirect('profile')
    else:
        form = AddressForm()
    return render(request, 'users/address_form.html', {'form': form})

@login_required
def edit_address_view(request, pk):
    address = Address.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated!')
            return redirect('profile')
    else:
        form = AddressForm(instance=address)
    return render(request, 'users/address_form.html', {'form': form})

@login_required
def delete_address_view(request, pk):
    address = Address.objects.get(pk=pk, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted!')
    return redirect('profile')
