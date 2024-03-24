# views.py
import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import ContactForm

def generate_otp():
    # Generate a 6-digit OTP
    return ''.join(random.choices('0123456789', k=6))

def send_otp_email(email, otp):
    subject = 'One-Time Password (OTP) Verification'
    message = f'Your OTP is: {otp}'
    from_email = 'petsget.online@gmail.com'  # Update this with your email address
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)






def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Generate OTP
            otp = generate_otp()
            
            # Send OTP via email
            send_otp_email(email, otp)
            
            # Redirect to OTP verification page
            request.session['otp'] = otp
            request.session['name'] = name
            request.session['email'] = email
            request.session['message'] = message
            return redirect('verify_contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
            
'''send_mail(
                subject='Contact Form Submission',
                message=f'Name: {name}\nEmail: {email}\nMessage: {message}',
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            
            
            
            
            
            return render(request, 'success.html', {'name': name})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})'''

def verify_contact(request):
    form_data = request.session.get('form_data')
    if not form_data:
        return redirect('contact')
    if request.method == 'POST':
        # Process the form data and do necessary actions
        # Once done, clear the session data
        del request.session['form_data']
        return render(request, 'success.html', {'name': form_data['name']})
    return render(request, 'verify_contact.html', {'form_data': form_data})

