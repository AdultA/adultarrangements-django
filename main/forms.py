# main/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import LifestyleProfile, DiscreetMessage, ExclusiveExperience
from datetime import date

# ===== REGISTRATION FORM =====
class CustomRegistrationForm(UserCreationForm):
    """Custom registration form with email"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        })
    )
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize fields
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        
        # Update placeholders
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create a password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})
    
    def clean_email(self):
        """Validate email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A portfolio with this email already exists.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# ===== PORTFOLIO FORM =====
class PortfolioForm(forms.ModelForm):
    """Form for editing lifestyle portfolio"""
    
    class Meta:
        model = LifestyleProfile
        fields = [
            'preferred_name',
            'gender',
            'gender_preference',
            'date_of_birth',
            'primary_location',
            'portfolio_image',
            'personal_statement',
            'lifestyle_preference',
            'current_engagement',
            'physique',
            'family_considerations',
            'lifestyle_habits',
            'stature',
            'financial_capacity',
            'personal_philosophy',
            'seeking_qualities',
        ]
        widgets = {
            'personal_statement': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'personal_philosophy': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'seeking_qualities': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'preferred_name': forms.TextInput(attrs={'class': 'form-control'}),
            'primary_location': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'gender_preference': forms.Select(attrs={'class': 'form-control'}),
            'lifestyle_preference': forms.Select(attrs={'class': 'form-control'}),
            'current_engagement': forms.Select(attrs={'class': 'form-control'}),
            'physique': forms.Select(attrs={'class': 'form-control'}),
            'family_considerations': forms.Select(attrs={'class': 'form-control'}),
            'lifestyle_habits': forms.Select(attrs={'class': 'form-control'}),
            'stature': forms.Select(attrs={'class': 'form-control'}),
            'financial_capacity': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_date_of_birth(self):
        """Validate age requirement (must be 18+)"""
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise ValidationError("You must be at least 18 years old.")
            if age > 100:
                raise ValidationError("Please enter a valid date of birth.")
        return dob

# ===== MESSAGE FORM =====
class DiscreetMessageForm(forms.ModelForm):
    """Form for sending discreet messages"""
    
    class Meta:
        model = DiscreetMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Compose your discreet message...',
                'class': 'form-control message-input'
            })
        }
    
    def clean_content(self):
        """Validate message content"""
        content = self.cleaned_data.get('content')
        if content:
            content = content.strip()
            if len(content) < 5:
                raise ValidationError("Message is too short (minimum 5 characters).")
            if len(content) > 2000:
                raise ValidationError("Message is too long (maximum 2000 characters).")
        return content

# ===== EXPERIENCE FORM =====
class ExclusiveExperienceForm(forms.ModelForm):
    """Form for hosting exclusive experiences"""
    
    class Meta:
        model = ExclusiveExperience
        fields = [
            'experience_title',
            'venue',
            'experience_date',
            'commencement',
            'conclusion',
            'experience_description',
            'consideration',
            'consideration_type',
        ]
        widgets = {
            'experience_title': forms.TextInput(attrs={'class': 'form-control'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'commencement': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'conclusion': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'experience_description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'consideration': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'consideration_type': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        """Validate experience dates and times"""
        cleaned_data = super().clean()
        experience_date = cleaned_data.get('experience_date')
        commencement = cleaned_data.get('commencement')
        conclusion = cleaned_data.get('conclusion')
        
        if experience_date and experience_date < date.today():
            self.add_error('experience_date', "Experience date cannot be in the past.")
        
        if commencement and conclusion:
            if commencement >= conclusion:
                self.add_error('conclusion', "End time must be after start time.")
        
        return cleaned_data

# ===== SEARCH FILTER FORM =====
class FilterForm(forms.Form):
    """Form for portfolio search filters"""
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter location...',
            'class': 'form-control'
        })
    )
    
    engagement_tier = forms.ChoiceField(
        choices=[
            ('', 'Any Tier'),
            ('standard', 'Standard'),
            ('premium', 'Premium'),
            ('exclusive', 'Exclusive'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    lifestyle_preference = forms.ChoiceField(
        choices=[
            ('', 'Any Preference'),
            ('curated_connections', 'Curated Connections'),
            ('luxury_experiences', 'Luxury Experiences'),
            ('mutual_benefit', 'Mutual Benefit'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    sort_by = forms.ChoiceField(
        choices=[
            ('last_active', 'Recently Active'),
            ('newest', 'Newest Portfolios'),
            ('most_viewed', 'Most Viewed'),
        ],
        required=False,
        initial='last_active',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

# ===== GALLERY FORM =====
class GalleryAccessForm(forms.Form):
    """Form for requesting gallery access"""
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Optional message to the gallery owner...',
            'class': 'form-control'
        }),
        required=False,
        max_length=500
    )

# ===== CONTACT FORM =====
class ContactForm(forms.Form):
    """Contact form for members"""
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'class': 'form-control'
        })
    )
