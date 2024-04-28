from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from user.models import User
from django.contrib.auth.decorators import login_required
from blog.models import Post
# Create your views here.


@login_required
def profile(request, usn):
    user = request.user
    if usn:
        user = User.objects.get(usn=usn)
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
            user.profile_pic = profile_pic
            user.save()
            return redirect('profile', user.usn)

    context = {
        'user': user,
        'posts': Post.objects.filter(author=user),
    }
    return render(request, 'profile.html', context=context)


def user_login(request):
    if request.method == 'POST':
        usn = request.POST['usn']
        password = request.POST['password']
        user = authenticate(usn=usn, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfully!!')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials!!')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        usn = request.POST.get('usn')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        # Check if user with provided username or email already exists
        if User.objects.filter(usn=usn).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "User with this username or email already exists.")
            return render(request, 'register.html')

        # Create user
        try:
            user = User.objects.create_user(usn=usn, name=name, phone_number=phone_number, email=email,
                                            dob=dob, gender=gender, password=password)
            user.save()
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'register.html')

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')

    return render(request, 'register.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successfully!!')
    return redirect('login')
