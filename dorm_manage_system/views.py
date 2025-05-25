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