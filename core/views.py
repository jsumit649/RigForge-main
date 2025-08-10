from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView

from .forms import MyUserCreationForm, PCBuildForm
from .models import PCBuild



from django.contrib.auth import get_user_model
User = get_user_model()



def home(request):
    return render(request, 'core/home.html')






def loginPage(request):

    page = 'login';

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username").lower()
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

    
    context= {'page': page}
        
        
    return render(request, "core/login_register.html", context)


# Handles user logout functionality
def logoutUser(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'core/login_register.html', {'form': form})


def editprofile(request):
    user = request.user
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = MyUserCreationForm(instance=user)
    return render(request, 'core/profile.html', {'form': form})







@login_required(login_url='login')
def cart(request):
    user = request.user
    builds = user.pc_builds.all()
    cart = getattr(user, 'cart', None)
    cart_items = cart.items.all() if cart else []

    # Calculate total
    total = 0
    for build in builds:
        total += getattr(build, 'Total_Price', 0)
    for item in cart_items:
        total += getattr(item.content_object, 'price', 0)

    context = {
        'builds': builds,
        'cart_items': cart_items,
        'total': total,  # Pass total to template
        }
    return render(request, 'core/cart.html', context)




def componentspage(request):
    return render(request, 'core/components.html')


def PCBuildpage(request):
    user = request.user
    if request.method == 'POST':
        form = PCBuildForm(request.POST)
        if form.is_valid():
            pc_build = form.save(commit=False)
            pc_build.user = user
            pc_build.save()
            messages.success(request, 'Build created successfully!')
            return redirect('build')
    else:
        form = PCBuildForm()
    builds = user.pc_builds.all()
    context = {
        'form': form,
        'builds': builds,
        'edit_mode': False,
    }
    return render(request, 'core/build.html', context)

@login_required(login_url='login')
def remove_build(request, build_id):
    user = request.user
    try:
        build = user.pc_builds.get(id=build_id)
        build.delete()
        messages.success(request, 'Build deleted successfully!')
    except PCBuild.DoesNotExist:
        messages.error(request, 'Build not found.')
    return redirect('cart')

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    user = request.user
    cart = getattr(user, 'cart', None)
    if not cart:
        messages.error(request, 'Cart not found.')
        return redirect('cart')
    try:
        cart_item = cart.items.get(id=item_id)
        cart_item.delete()
        messages.success(request, 'Item removed from cart successfully!')
    except Exception as e:
        messages.error(request, f'Error removing item: {str(e)}')
    return redirect('cart')

@login_required(login_url='login')
def edit_build(request, build_id):
    user = request.user
    try:
        build = user.pc_builds.get(id=build_id)
    except PCBuild.DoesNotExist:
        messages.error(request, 'Build not found.')
        return redirect('build')
    if request.method == 'POST':
        form = PCBuildForm(request.POST, instance=build)
        if form.is_valid():
            form.save()
            messages.success(request, 'Build updated successfully!')
            return redirect('build')
    else:
        form = PCBuildForm(instance=build)
    # Show all user's builds for context
    builds = user.pc_builds.all()
    context = {'form': form, 'edit_mode': True, 'builds': builds, 'edit_build_id': build.id}
    return render(request, 'core/build.html', context)