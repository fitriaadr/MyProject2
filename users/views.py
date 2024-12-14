from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from .models import Notification
from vegetables_prices.models import Vegetable

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun berhasil dibuat! Silakan login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Username atau password salah!')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def contact_admin(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, 'Pesan berhasil dikirim!')
            return redirect('user_dashboard')
    else:
        form = ContactForm()
    return render(request, 'users/contact_admin.html', {'form': form})

@staff_member_required
def admin_dashboard(request):
    user_model = get_user_model()
    users = user_model.objects.all()  # Mengambil semua data pengguna
    contact_messages = ContactForm.Meta.model.objects.all()  # Mengambil semua pesan kontak (jika ContactMessage digunakan)
    return render(request, 'users/admin_dashboard.html', {
        'users': users,
        'contact_messages': contact_messages
    })

def home(request):
    return render(request, 'users/home.html')

@login_required
def user_dashboard(request):
    notifications = Notification.objects.filter(user=request.user)
    vegetables = Vegetable.objects.all()
    form = ContactForm()
    return render(request, 'users/user_dashboard.html', {
        'notifications': notifications,
        'vegetables': vegetables,
        'form': form
    })

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil berhasil diperbarui!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/user_profile.html', {'form': form})

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/notification_list.html', {'notifications': notifications})

@login_required
def vegetable_guide(request):
    vegetables = Vegetable.objects.all()
    return render(request, 'vegetables_prices/vegetable_guide.html', {'vegetables': vegetables})

