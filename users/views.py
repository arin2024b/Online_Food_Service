from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm, AddressForm
from .models import Address
from django.contrib.auth import get_user_model
from orders.models import Order
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password

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

@csrf_protect
def password_reset_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        try:
            user = User.objects.get(username=username, email=email)
            if user.phone == phone:
                request.session['reset_user_id'] = user.id
                return redirect('password_reset_confirm')
            else:
                messages.error(request, 'Invalid credentials. Please check your details.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials. Please check your details.')
    return render(request, 'users/password_reset_request.html')

@csrf_protect
def password_reset_confirm(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, 'Session expired. Please try again.')
        return redirect('password_reset_request')
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password and password == confirm_password:
            user = User.objects.get(id=user_id)
            user.password = make_password(password)
            user.save()
            del request.session['reset_user_id']
            messages.success(request, 'Password reset successful. Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'users/password_reset_confirm.html')
