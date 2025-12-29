# main/models.py - CORRECTED VERSION
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import json

# ===== GLOBAL CHOICES =====
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

GENDER_INTEREST_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Both', 'Both'),
]

# Lifestyle Preferences
LIFESTYLE_PREFERENCE_CHOICES = [
    ('curated_connections', 'Curated Connections'),
    ('luxury_experiences', 'Luxury Experiences'),
    ('mutual_benefit', 'Mutual Benefit'),
]

# Engagement Type
ENGAGEMENT_TYPE_CHOICES = [
    ('standard', 'Standard'),
    ('premium', 'Premium'),
    ('exclusive', 'Exclusive'),
]

# Relationship Status
RELATIONSHIP_CHOICES = [
    ('discreetly_available', 'Discreetly Available'),
    ('selectively_engaged', 'Selectively Engaged'),
    ('unattached', 'Unattached'),
    ('complicated_elegance', 'Complicated Elegance'),
]

# Body Type
BODY_TYPE_CHOICES = [
    ('Slim', 'Slim'),
    ('Average', 'Average'),
    ('Athletic', 'Athletic'),
    ('Large', 'Large'),
    ('Curvy', 'Curvy'),
]

# Children
CHILDREN_CHOICES = [
    ('No', 'No'),
    ('Yes', 'Yes'),
    ('Yes, at home', 'Yes, at home'),
    ('Yes, not at home', 'Yes, not at home'),
]

# Smoker
SMOKER_CHOICES = [
    ('No', 'No'),
    ('Yes', 'Yes'),
    ('Socially', 'Socially'),
]

# Height (simplified)
HEIGHT_CHOICES = [
    ('Select from list', 'Select from list'),
    ("5'0\"", "5'0\""),
    ("5'5\"", "5'5\""),
    ("5'10\"", "5'10\""),
    ("6'0\"", "6'0\""),
    ("6'5\"", "6'5\""),
]

# Net Worth
NET_WORTH_CHOICES = [
    ('Under $100k', 'Under $100k'),
    ('$100k - $250k', '$100k - $250k'),
    ('$250k - $500k', '$250k - $500k'),
    ('$500k - $1M', '$500k - $1M'),
    ('$1M - $5M', '$1M - $5M'),
    ('Over $5M', 'Over $5M'),
]

# Period choices
PERIOD_CHOICES = [
    ('per week', 'per week'),
    ('per month', 'per month'),
    ('per meet', 'per meet'),
]

class LifestyleProfile(models.Model):
    """Elite Lifestyle Connections Profile"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lifestyle_profile')
    
    # === PERSONAL PORTFOLIO ===
    preferred_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    gender_preference = models.CharField(max_length=10, choices=GENDER_INTEREST_CHOICES, default='Both')
    date_of_birth = models.DateField(null=True, blank=True)
    
    # === LIFESTYLE LOCATION ===
    primary_location = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # === PORTFOLIO PRESENCE ===
    portfolio_image = models.ImageField(upload_to='portfolios/', null=True, blank=True)
    personal_statement = models.TextField(blank=True)
    lifestyle_preference = models.CharField(max_length=50, choices=LIFESTYLE_PREFERENCE_CHOICES, blank=True)
    
    # === PERSONAL ATTRIBUTES ===
    current_engagement = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES, blank=True)
    physique = models.CharField(max_length=50, choices=BODY_TYPE_CHOICES, blank=True)
    family_considerations = models.CharField(max_length=50, choices=CHILDREN_CHOICES, blank=True)
    lifestyle_habits = models.CharField(max_length=50, choices=SMOKER_CHOICES, blank=True)
    stature = models.CharField(max_length=50, choices=HEIGHT_CHOICES, blank=True)
    financial_capacity = models.CharField(max_length=50, choices=NET_WORTH_CHOICES, blank=True)
    
    # === PERSONAL NARRATIVE ===
    personal_philosophy = models.TextField(blank=True)
    seeking_qualities = models.TextField(blank=True)
    
    # === IDEAL ENGAGEMENT ===
    preferred_engagements = models.JSONField(default=list)
    appreciates_qualities = models.JSONField(default=list)
    availability_framework = models.JSONField(default=list)
    
    # Expectations
    expectation_framework = models.CharField(max_length=100, blank=True)
    consideration_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    consideration_period = models.CharField(max_length=50, choices=PERIOD_CHOICES, blank=True)
    
    # === MEMBERSHIP STATUS ===
    engagement_tier = models.CharField(max_length=20, choices=ENGAGEMENT_TYPE_CHOICES, default='standard')
    portfolio_suspended = models.BooleanField(default=False)
    curator_approved = models.BooleanField(default=False)
    public_portfolio = models.BooleanField(default=False)
    under_review = models.BooleanField(default=True)
    enhanced_portfolio = models.BooleanField(default=False)
    curated_content = models.JSONField(null=True, blank=True)
    
    # === VISUAL PORTFOLIO ===
    lifestyle_images = models.JSONField(default=list)
    private_gallery = models.JSONField(default=list)
    gallery_access = models.JSONField(default=dict)
    gallery_requests = models.JSONField(default=dict)
    
    # === CONNECTION METRICS ===
    saved_connections = models.JSONField(default=list)
    restricted_connections = models.JSONField(default=list)
    portfolio_views = models.JSONField(default=dict)
    interest_received = models.JSONField(default=dict)
    last_active = models.DateTimeField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    
    # === DATES ===
    engagement_expiry = models.IntegerField(null=True, blank=True)
    portfolio_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # === METHODS ===
    def get_life_stage(self):
        """Calculate life stage from date_of_birth"""
        if self.date_of_birth:
            today = timezone.now().date()
            years = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
            if years < 25:
                return "Emerging Sophisticate"
            elif years < 35:
                return "Established Professional"
            elif years < 50:
                return "Seasoned Connoisseur"
            else:
                return "Distinguished Elite"
        return None
    
    def has_exclusive_access(self):
        """Check if user has exclusive engagement tier"""
        return self.engagement_tier in ['premium', 'exclusive']
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_active = timezone.now()
        self.save()
    
    def __str__(self):
        return f"{self.preferred_name or self.user.username} - {self.engagement_tier} Lifestyle Portfolio"

class CuratedIntroduction(models.Model):
    """Curated introduction between sophisticated individuals"""
    participants = models.ManyToManyField(User, related_name='curated_introductions')
    last_exchange = models.ForeignKey('DiscreetMessage', on_delete=models.SET_NULL, null=True, related_name='latest_in_introduction')
    introduction_initiated = models.DateTimeField(auto_now_add=True)
    last_interaction = models.DateTimeField(auto_now=True)
    
    def get_other_participant(self, user):
        """Get the other individual in the introduction"""
        return self.participants.exclude(id=user.id).first()
    
    def get_unread_exchanges(self, user):
        """Count unread exchanges for an individual"""
        return self.discreet_messages.filter(is_read=False).exclude(sender=user).count()
    
    class Meta:
        ordering = ['-last_interaction']

class DiscreetMessage(models.Model):
    """Discreet message exchange"""
    introduction = models.ForeignKey(CuratedIntroduction, on_delete=models.CASCADE, related_name='discreet_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_exchanges')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    exchanged_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['exchanged_at']

class ExclusiveExperience(models.Model):
    """Exclusive experience listings"""
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_experiences')
    experience_title = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)
    experience_date = models.DateField()
    commencement = models.TimeField()
    conclusion = models.TimeField()
    experience_description = models.TextField()
    consideration = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    consideration_type = models.CharField(max_length=50, choices=[
        ('hosted_experience', 'Hosted Experience'),
        ('seeking_participant', 'Seeking Participant'),
    ])
    is_active = models.BooleanField(default=True)
    listed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.experience_title} - {self.experience_date}"

class GalleryAccessRequest(models.Model):
    """Private gallery access requests"""
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gallery_requests_sent')
    gallery_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gallery_requests_received')
    access_status = models.CharField(max_length=20, choices=[
        ('pending_review', 'Pending Review'),
        ('access_granted', 'Access Granted'),
        ('access_declined', 'Access Declined'),
    ], default='pending_review')
    requested_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['requester', 'gallery_owner']
