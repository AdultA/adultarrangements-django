# adultarrangements/urls.py (PROJECT LEVEL)
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from main.views import register_view  # IMPORTANT: This import must exist

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # ===== PUBLIC PAGES =====
    # These templates are in templates/ directory (not main/templates/)
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('safety/', TemplateView.as_view(template_name='safety.html'), name='safety'),
    path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path('terms/', TemplateView.as_view(template_name='terms.html'), name='terms'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    
    # ===== AUTHENTICATION =====
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register_view, name='register'),  # Uses your custom view
    path('join/', register_view, name='join'),  # Alias for register
    
    # ===== PASSWORD RESET URLs (REQUIRED) =====
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # ===== MEMBER AREA =====
    path('', include('main.urls')),  # This includes all your app URLs from main/urls.py
]
