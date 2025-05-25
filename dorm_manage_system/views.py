from django.shortcuts import render, redirect
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

def home(request):
    """View function for the home page."""
    return render(request, 'home.html')

def accessibility(request):
    """View function for the accessibility statement page."""
    return render(request, 'accessibility.html')

def accessibility_contact(request):
    """View function for handling accessibility contact form submissions."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        # Here you would typically send an email or save to database
        # For now, we'll just show a success message
        messages.success(request, 'תודה על פנייתך. נחזור אליך בהקדם.')
        
        # Log the accessibility contact for monitoring
        logger.info(f'Accessibility contact received from {name} ({email})')
        
        return redirect('accessibility')
    
    return redirect('accessibility')

def legal_assistance(request):
    """View function for the legal assistance page."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        issue = request.POST.get('issue')
        documents = request.FILES.getlist('documents')
        
        # Here you would typically:
        # 1. Save the request to the database
        # 2. Send notification emails
        # 3. Process uploaded documents
        
        # For now, we'll just show a success message
        messages.success(request, 'תודה על פנייתך. צוות המשפטי שלנו יצור איתך קשר תוך יומיים עסקיים.')
        
        # Log the legal assistance request
        logger.info(f'Legal assistance request received from {name} ({email})')
        
        return redirect('legal_assistance')
    
    return render(request, 'legal_assistance.html')

def connect_us(request):
    """View function for the contact us page."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically:
        # 1. Save the contact request to the database
        # 2. Send notification emails
        # 3. Process any attachments
        
        # For now, we'll just show a success message
        messages.success(request, '{% trans "Thank you for contacting us. We will get back to you as soon as possible." %}')
        
        # Log the contact request
        logger.info(f'Contact request received from {name} ({email}) - Subject: {subject}')
        
        return redirect('connect_us')
    
    return render(request, 'connect_us.html') 