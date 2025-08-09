from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView

from .forms import MyUserCreationForm, PCBuildForm
from .models import CPU, GPU, Motherboard, RAM, PSU,SSDStorage, HDDStorage, Case, CPUCooler



from django.contrib.auth import get_user_model
User = get_user_model()



def home(request):
    return render(request, 'core/home.html')






def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')

    
    context= {}
        
        
    return render(request, "core/login_register.html", context)


# Handles user logout functionality
def logoutUser(request):
    logout(request)
    return redirect("home")

def registerPage(request):
    form = MyUserCreationForm()

    if request.method =='POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render (request, 'base/login_register.html', {'form': form})



@login_required(login_url='login')
def cart(request):
    if request.method == "POST":
        # Handle cart logic here
        messages.success(request, 'Item added to cart successfully!')
        return redirect('cart')

    if request.method == "GET":
        # Handle displaying cart items
        messages.info(request, 'Viewing cart items')
    # Render the cart page
    return render(request, 'core/cart.html')



def PCBuildpage(request):
    if request.method == 'POST':
        form = PCBuildForm(request.POST)
        if form.is_valid():
            pc_build = form.save(commit=False)
            pc_build.user = request.user
            # Call the model's check_compatibility method
            issues = pc_build.check_compatibility()
            if issues:
                for issue in issues:
                    messages.error(request, issue)
                # Do not save if there are compatibility issues
            else:
                pc_build.save()
                messages.success(request, 'PC Build created successfully!')
                return redirect('home')
    else:
        form = PCBuildForm()

    context = {
        'form': form,
    }
    return render(request, 'core/build.html', context)