from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from .models import Notification, ContactMessage, Post, Comment
from vegetables_prices.models import Vegetable
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
import imghdr
from django.http import HttpResponseForbidden


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, 'Akun berhasil dibuat! Silakan login.')
            return redirect('login')  # Redirect to login page or wherever you need
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
            message = form.cleaned_data['message']
            if len(message) > 1000:
                messages.error(request, 'Pesan terlalu panjang! Maksimal 1000 karakter.')
            else:
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
    users = user_model.objects.all()
    contact_messages = ContactForm.Meta.model.objects.all()
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


class NotificationListView(ListView):
    model = Notification
    template_name = 'users/notification_list.html'
    context_object_name = 'notifications'


@login_required
def vegetable_guide(request):
    vegetables = Vegetable.objects.all()
    return render(request, 'vegetables_prices/vegetable_guide.html', {'vegetables': vegetables})


class ContactMessageCreateView(CreateView):
    model = ContactMessage
    template_name = 'users/contact_admin.html'
    fields = ['message']
    success_url = reverse_lazy('contact_admin')


class UserDetailView(DetailView):
    model = User
    template_name = 'users/profile.html'


@login_required
def community_feed(request):
    posts = Post.objects.select_related('user').prefetch_related('likes', 'comments').order_by('-created_at')
    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'community/feed.html', {'page_obj': page_obj})

@login_required
def upload_post(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption', '').strip()
        if image:
            # Validasi tipe file
            if imghdr.what(image) not in ['jpeg', 'png', 'gif']:
                messages.error(request, 'File harus berupa gambar (JPEG, PNG, GIF).')
                return redirect('upload_post')

            # Validasi ukuran file
            if image.size > 5 * 1024 * 1024:  # Maksimal 5MB
                messages.error(request, 'Ukuran file terlalu besar! Maksimal 5MB.')
                return redirect('upload_post')

            Post.objects.create(user=request.user, image=image, caption=caption)
            messages.success(request, 'Postingan berhasil diunggah!')
            return redirect('community_feed')
    return render(request, 'community/upload.html')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.user:
        post.delete()
        messages.success(request, "Postingan berhasil dihapus.")
        return redirect('community_feed')
    else:
        return HttpResponseForbidden("Anda tidak memiliki izin untuk menghapus postingan ini.")

@require_POST
@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        # Misalkan Anda memiliki metode untuk menangani likes
        post.likes.add(request.user)  # Tambahkan pengguna ke dalam likes
        post.save()
        return JsonResponse({'likes_count': post.likes.count()})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content', '').strip()
    if content:
        if len(content) > 500:
            messages.error(request, 'Komentar terlalu panjang! Maksimal 500 karakter.')
        else:
            Comment.objects.create(user=request.user, post=post, content=content)
            messages.success(request, 'Komentar berhasil ditambahkan!')
    else:
        messages.error(request, 'Komentar tidak boleh kosong.')
    return redirect('community_feed')