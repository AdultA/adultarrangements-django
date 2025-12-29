# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ===== PUBLIC AUTH PAGES (in main app) =====
    path('register/', views.register_view, name='register'),
    path('join/', views.register_view, name='join'),
    
    # ===== MEMBER PAGES =====
    # Core portfolio pages
    path('lifestyle-dashboard/', views.lifestyle_dashboard, name='lifestyle_dashboard'),
    path('curated-search/', views.curated_search, name='curated_search'),
    path('portfolio/<str:username>/', views.view_portfolio, name='view_portfolio'),
    path('refine-portfolio/', views.edit_portfolio, name='edit_portfolio'),
    path('engagement-management/', views.engagement_management, name='engagement_management'),
    
    # Add this alias for 'profile' to fix the error
    path('profile/', views.lifestyle_dashboard, name='profile'),
    
    # Additional pages
    path('portfolio-pending/', views.portfolio_pending, name='portfolio_pending'),
    path('curated-introductions/', views.curated_introductions, name='curated_introductions'),
    path('saved-connections/', views.saved_connections, name='saved_connections'),
    
    # Action URLs
    path('save-connection/<int:user_id>/', views.save_connection, name='save_connection'),
    path('restrict-connection/<int:user_id>/', views.restrict_connection, name='restrict_connection'),
    path('send-message/<int:user_id>/', views.send_message, name='send_message'),
    
    # Additional views
    path('lifestyle-preferences/', views.lifestyle_preferences, name='lifestyle_preferences'),
    path('discretion-settings/', views.discretion_settings, name='discretion_settings'),
    path('gallery-management/', views.gallery_management, name='gallery_management'),
    path('curator-dashboard/', views.curator_dashboard, name='curator_dashboard'),
]
