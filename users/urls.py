from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import NotificationListView, delete_post

urlpatterns = [
    # Home & Authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # User Dashboard & Profile
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile/', views.user_profile, name='user_profile'),

    # Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('contact/', views.contact_admin, name='contact_admin'),

    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notification_list'),

    # Vegetable Guide
    path('vegetable-guide/', views.vegetable_guide, name='vegetable_guide'),

    # Community
    path('community/', views.community_feed, name='community_feed'),
    path('community/upload/', views.upload_post, name='upload_post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('community/like/<int:post_id>/', views.like_post, name='like_post'),
    path('community/comment/<int:post_id>/', views.add_comment, name='add_comment'),
]
