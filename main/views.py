# main/views.py - CLEAN VERSION (NO CIRCULAR IMPORTS)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import LifestyleProfile
from .forms import CustomRegistrationForm, PortfolioForm

# ===== PUBLIC VIEWS =====
def register_view(request):
    """Registration view for new users"""
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Automatically create a lifestyle profile for the new user
            LifestyleProfile.objects.create(user=user)
            
            messages.success(request, 'Portfolio created successfully! Please login.')
            return redirect('login')
    else:
        form = CustomRegistrationForm()
    
    return render(request, 'register.html', {
        'form': form,
        'title': 'Join Elite Lifestyle Connections',
        'description': 'Create your account to discover sophisticated lifestyle connections.',
    })

# ===== MEMBER VIEWS =====
@login_required
def lifestyle_dashboard(request):
    """Member dashboard - main homepage after login - SHOWS OTHER PROFILES IN GRID"""
    # Get or create user profile
    profile, created = LifestyleProfile.objects.get_or_create(user=request.user)
    
    if created:
        messages.info(request, 'Welcome! Please complete your portfolio for better matches.')
    
    # Get all approved portfolios (exclude current user)
    portfolios_list = LifestyleProfile.objects.filter(
        curator_approved=True,
        public_portfolio=True,
        portfolio_suspended=False
    ).exclude(user=request.user).order_by('-last_active')
    
    # Pagination - 12 per page (like screenshot shows)
    paginator = Paginator(portfolios_list, 12)
    page_number = request.GET.get('page', 1)
    portfolios = paginator.get_page(page_number)
    
    context = {
        'title': 'Lifestyle Portfolio Dashboard | Elite Connections',
        'description': 'Your exclusive lifestyle connections dashboard',
        'portfolios': portfolios,
        'user_profile': profile,
    }
    return render(request, 'main/lifestyle_dashboard.html', context)

@login_required
def edit_portfolio(request):
    """Edit or create lifestyle portfolio - SEPARATE PAGE, NOT DEFAULT"""
    try:
        profile = request.user.lifestyle_profile
    except LifestyleProfile.DoesNotExist:
        profile = LifestyleProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.under_review = True
            portfolio.curator_approved = False
            portfolio.save()
            messages.success(request, 'Portfolio submitted for curator review!')
            return redirect('lifestyle_dashboard')
    else:
        form = PortfolioForm(instance=profile)
    
    context = {
        'title': 'Refine Your Lifestyle Portfolio',
        'description': 'Update your personal portfolio to attract compatible connections.',
        'form': form,
        'profile': profile,
    }
    return render(request, 'main/edit_portfolio.html', context)

def view_portfolio(request, username):
    """View individual portfolio"""
    user = get_object_or_404(User, username=username)
    profile = user.lifestyle_profile
    
    # Check if profile is approved and public
    if not profile.curator_approved or not profile.public_portfolio:
        messages.error(request, 'This portfolio is not available.')
        return redirect('lifestyle_dashboard')
    
    # Increment view count
    profile.view_count += 1
    profile.save()
    
    context = {
        'title': f'{profile.preferred_name or user.username} | Lifestyle Portfolio',
        'description': f'View {profile.preferred_name or user.username}\'s lifestyle portfolio.',
        'portfolio': profile,
        'portfolio_user': user,
    }
    return render(request, 'main/view_portfolio.html', context)

@login_required
def curated_search(request):
    """Search for compatible portfolios with filters"""
    portfolios_list = LifestyleProfile.objects.filter(
        curator_approved=True,
        public_portfolio=True,
        portfolio_suspended=False
    ).exclude(user=request.user)
    
    # Apply filters
    location = request.GET.get('location', '')
    status = request.GET.get('status', '')
    
    if location:
        portfolios_list = portfolios_list.filter(primary_location__icontains=location)
    
    if status == 'premium':
        portfolios_list = portfolios_list.filter(engagement_tier='premium')
    elif status == 'exclusive':
        portfolios_list = portfolios_list.filter(engagement_tier='exclusive')
    
    portfolios_list = portfolios_list.order_by('-last_active')
    
    # Pagination
    paginator = Paginator(portfolios_list, 12)
    page_number = request.GET.get('page', 1)
    portfolios = paginator.get_page(page_number)
    
    context = {
        'title': 'Curated Search | Find Compatible Lifestyles',
        'description': 'Search for sophisticated individuals based on lifestyle compatibility.',
        'portfolios': portfolios,
        'location': location,
        'status': status,
    }
    return render(request, 'main/curated_search.html', context)

@login_required
def engagement_management(request):
    """Account and engagement settings"""
    try:
        profile = request.user.lifestyle_profile
    except LifestyleProfile.DoesNotExist:
        messages.error(request, 'Please create your portfolio first.')
        return redirect('edit_portfolio')
    
    context = {
        'title': 'Engagement Management | Your Profile',
        'description': 'Manage your engagement tier and account settings.',
        'profile': profile,
    }
    return render(request, 'main/engagement_management.html', context)

# ===== ADDITIONAL VIEWS =====
@login_required
def portfolio_pending(request):
    """Portfolio pending approval page"""
    try:
        profile = request.user.lifestyle_profile
    except LifestyleProfile.DoesNotExist:
        return redirect('edit_portfolio')
    
    return render(request, 'main/portfolio_pending.html', {
        'title': 'Portfolio Under Review | Elite Lifestyle Connections',
        'description': 'Your portfolio is currently under review by our curation team.',
        'profile': profile,
    })

@login_required
def curated_introductions(request):
    """Messages/inbox"""
    return render(request, 'main/curated_introductions.html', {
        'title': 'Curated Introductions | Discreet Exchanges',
        'description': 'Manage your discreet exchanges with compatible individuals.',
    })

@login_required
def saved_connections(request):
    """Favorites/saved connections"""
    try:
        profile = request.user.lifestyle_profile
        # Get saved user IDs from JSONField
        saved_ids = profile.saved_connections or []
        saved_users = User.objects.filter(id__in=saved_ids)
    except:
        saved_users = []
    
    return render(request, 'main/saved_connections.html', {
        'title': 'Saved Connections | Your Network',
        'description': 'Manage your saved connections and view expressions of interest.',
        'saved_users': saved_users,
    })

@login_required
def save_connection(request, user_id):
    """Save a user to connections"""
    try:
        user_to_save = User.objects.get(id=user_id)
        profile = request.user.lifestyle_profile
        
        # Initialize saved_connections if empty
        if profile.saved_connections is None:
            profile.saved_connections = []
        
        # Add to saved connections if not already saved
        if user_id not in profile.saved_connections:
            profile.saved_connections.append(user_id)
            profile.save()
            messages.success(request, f'Added {user_to_save.username} to saved connections.')
        else:
            messages.info(request, f'{user_to_save.username} is already in your saved connections.')
    
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
    
    return redirect('lifestyle_dashboard')

@login_required
def restrict_connection(request, user_id):
    """Restrict/block a connection"""
    try:
        user_to_restrict = User.objects.get(id=user_id)
        profile = request.user.lifestyle_profile
        
        # Initialize restricted_connections if empty
        if profile.restricted_connections is None:
            profile.restricted_connections = []
        
        # Add to restricted connections
        if user_id not in profile.restricted_connections:
            profile.restricted_connections.append(user_id)
            profile.save()
            messages.success(request, f'Restricted connection with {user_to_restrict.username}.')
        else:
            messages.info(request, f'Connection with {user_to_restrict.username} is already restricted.')
    
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
    
    return redirect('lifestyle_dashboard')

@login_required
def send_message(request, user_id):
    """Send a message to another user"""
    try:
        user_to_message = User.objects.get(id=user_id)
        messages.info(request, f'Messaging feature coming soon! Would message {user_to_message.username}.')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
    
    return redirect('lifestyle_dashboard')

# ===== SIMPLIFIED ADDITIONAL VIEWS =====
@login_required
def lifestyle_preferences(request):
    """Lifestyle preferences settings"""
    return render(request, 'main/lifestyle_preferences.html', {
        'title': 'Lifestyle Preferences | Your Settings',
        'description': 'Configure your lifestyle preferences and interests.',
    })

@login_required
def discretion_settings(request):
    """Privacy and discretion settings"""
    return render(request, 'main/discretion_settings.html', {
        'title': 'Discretion Settings | Privacy',
        'description': 'Manage your privacy and discretion preferences.',
    })

@login_required
def gallery_management(request):
    """Photo gallery management"""
    return render(request, 'main/gallery_management.html', {
        'title': 'Gallery Management | Your Photos',
        'description': 'Manage your portfolio and private gallery images.',
    })

@login_required
def curator_dashboard(request):
    """Admin/curator dashboard - only for staff users"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('lifestyle_dashboard')
    
    # Get pending portfolios for review
    pending_portfolios = LifestyleProfile.objects.filter(
        under_review=True,
        curator_approved=False
    )
    
    return render(request, 'main/curator_dashboard.html', {
        'title': 'Curator Dashboard | Portfolio Management',
        'description': 'Review and manage member portfolios.',
        'pending_portfolios': pending_portfolios,
    })
