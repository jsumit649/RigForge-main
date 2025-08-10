from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .forms import MyUserCreationForm, PCBuildForm, AddressForm, ProfileEditForm
from .models import PCBuild, Address



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


def profile(request):
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
def editprofile(request):
    user = request.user
    addresses = user.addresses.all()
    profile_form = ProfileEditForm(instance=user)
    address_form = AddressForm()
    password_form = PasswordChangeForm(user=user)

    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            profile_form = ProfileEditForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated.")
                return redirect('profile')
        elif 'address_submit' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = user
                address.save()
                messages.success(request, "Address added.")
                return redirect('profile')
        elif 'password_submit' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully.")
                return redirect('profile')

    context = {
        'profile_form': profile_form,
        'address_form': address_form,
        'addresses': addresses,
        'password_form': password_form,
    }
    return render(request, 'core/profile.html', context)

@login_required(login_url='login')
def delete_address(request, address_id):
    address = Address.objects.get(id=address_id, user=request.user)
    address.delete()
    messages.success(request, "Address deleted.")
    return redirect('profile')


def cart(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, 'Log in to view your cart')
        return redirect('login')
    
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
    # Check if user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, 'Log in to create a build')
        return redirect('login')
    
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

from django.contrib.auth.decorators import login_required
from .models import Address
from .forms import AddressForm
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required(login_url='login')
def checkout(request):
    user = request.user
    addresses = user.addresses.all()
    address_form = AddressForm()

    # Calculate cart total for the user (same as in your cart view)
    builds = user.pc_builds.all()
    cart = getattr(user, 'cart', None)
    cart_items = cart.items.all() if cart else []

    items_total = 0
    for build in builds:
        items_total += getattr(build, 'Total_Price', 0)
    for item in cart_items:
        items_total += getattr(item.content_object, 'price', 0)

    if request.method == 'POST':
        if 'add_address' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = user
                address.save()
                messages.success(request, "Address added.")
                return redirect('checkout')
        elif 'place_order' in request.POST:
            address_id = request.POST.get('address_id')
            payment_method = request.POST.get('payment_method')
            # Here you would handle order creation, payment, etc.
            messages.success(request, "Order placed successfully!")
            return redirect('home')

    context = {
        'addresses': addresses,
        'address_form': address_form,
        'items_total': items_total,
    }
    return render(request, 'core/checkout.html', context)