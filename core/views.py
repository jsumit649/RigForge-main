from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm

from .forms import MyUserCreationForm, PCBuildForm, AddressForm, ProfileEditForm
from .models import PCBuild, Address

User = get_user_model()

class HomeView(TemplateView):
    template_name = 'core/home.html'


class LoginPageView(FormView):
    template_name = 'core/login_register.html'
    form_class = MyUserCreationForm  # Not actually used for login, but for template context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return self.form_invalid(self.get_form())
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return self.form_invalid(self.get_form())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'login'
        return context


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect("home")


class RegisterPageView(FormView):
    template_name = 'core/login_register.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(self.request, user)
        messages.success(self.request, 'Account created successfully!')
        return redirect('login')

    def form_invalid(self, form):
        messages.error(self.request, 'An error occurred during registration')
        return super().form_invalid(form)


class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        user = request.user
        form = MyUserCreationForm(instance=user)
        return render(request, 'core/profile.html', {'form': form})

    def post(self, request):
        user = request.user
        form = MyUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        return render(request, 'core/profile.html', {'form': form})


class EditProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        user = request.user
        addresses = user.addresses.all()
        profile_form = ProfileEditForm(instance=user)
        address_form = AddressForm()
        password_form = PasswordChangeForm(user=user)
        context = {
            'profile_form': profile_form,
            'address_form': address_form,
            'addresses': addresses,
            'password_form': password_form,
        }
        return render(request, 'core/profile.html', context)

    def post(self, request):
        user = request.user
        addresses = user.addresses.all()
        profile_form = ProfileEditForm(instance=user)
        address_form = AddressForm()
        password_form = PasswordChangeForm(user=user)

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


class DeleteAddressView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, address_id):
        address = get_object_or_404(Address, id=address_id, user=request.user)
        address.delete()
        messages.success(request, "Address deleted.")
        return redirect('profile')


class CartView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        user = request.user
        builds = user.pc_builds.all()
        cart = getattr(user, 'cart', None)
        cart_items = cart.items.all() if cart else []
        total = sum(getattr(build, 'Total_Price', 0) for build in builds)
        total += sum(getattr(item.content_object, 'price', 0) for item in cart_items)
        context = {
            'builds': builds,
            'cart_items': cart_items,
            'total': total,
        }
        return render(request, 'core/cart.html', context)


class ComponentsPageView(TemplateView):
    template_name = 'core/components.html'


class PCBuildPageView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        user = request.user
        form = PCBuildForm()
        builds = user.pc_builds.all()
        context = {
            'form': form,
            'builds': builds,
            'edit_mode': False,
        }
        return render(request, 'core/build.html', context)

    def post(self, request):
        form = PCBuildForm(request.POST)
        if form.is_valid():
            build = form.save(commit=False)
            build.user = request.user
            issues = build.check_compatibility()
            if issues:
                # Do NOT save, show issues
                builds = PCBuild.objects.filter(user=request.user)
                return render(request, 'core/build.html', {
                    'form': form,
                    'builds': builds,
                    'compatibility_issues': issues,
                    'edit_mode': False,
                })
            build.save()
            return redirect('build')  # or your builds page
        builds = request.user.pc_builds.all()
        context = {
            'form': form,
            'builds': builds,
            'edit_mode': False,
        }
        return render(request, 'core/build.html', context)


class RemoveBuildView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, build_id):
        user = request.user
        try:
            build = user.pc_builds.get(id=build_id)
            build.delete()
            messages.success(request, 'Build deleted successfully!')
        except PCBuild.DoesNotExist:
            messages.error(request, 'Build not found.')
        return redirect('cart')


class RemoveFromCartView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, item_id):
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


class EditBuildView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, build_id):
        user = request.user
        try:
            build = user.pc_builds.get(id=build_id)
        except PCBuild.DoesNotExist:
            messages.error(request, 'Build not found.')
            return redirect('build')
        form = PCBuildForm(instance=build)
        builds = user.pc_builds.all()
        context = {'form': form, 'edit_mode': True, 'builds': builds, 'edit_build_id': build.id}
        return render(request, 'core/build.html', context)

    def post(self, request, build_id):
        user = request.user
        try:
            build = user.pc_builds.get(id=build_id)
        except PCBuild.DoesNotExist:
            messages.error(request, 'Build not found.')
            return redirect('build')
        form = PCBuildForm(request.POST, instance=build)
        if form.is_valid():
            form.save()
            messages.success(request, 'Build updated successfully!')
            return redirect('build')
        builds = user.pc_builds.all()
        context = {'form': form, 'edit_mode': True, 'builds': builds, 'edit_build_id': build.id}
        return render(request, 'core/build.html', context)


class CheckoutView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        user = request.user
        addresses = user.addresses.all()
        address_form = AddressForm()
        builds = user.pc_builds.all()
        cart = getattr(user, 'cart', None)
        cart_items = cart.items.all() if cart else []
        # Redirect if both builds and cart_items are empty
        if not builds and not cart_items:
            messages.info(request, "Your cart is empty.")
            return redirect('home')
        items_total = sum(getattr(build, 'Total_Price', 0) for build in builds)
        items_total += sum(getattr(item.content_object, 'price', 0) for item in cart_items)
        context = {
            'addresses': addresses,
            'address_form': address_form,
            'items_total': items_total,
        }
        return render(request, 'core/checkout.html', context)

    def post(self, request):
        user = request.user
        addresses = user.addresses.all()
        address_form = AddressForm()
        builds = user.pc_builds.all()
        cart = getattr(user, 'cart', None)
        cart_items = cart.items.all() if cart else []
        # Redirect if both builds and cart_items are empty
        if not builds and not cart_items:
            messages.info(request, "Your cart is empty.")
            return redirect('home')
        items_total = sum(getattr(build, 'Total_Price', 0) for build in builds)
        items_total += sum(getattr(item.content_object, 'price', 0) for item in cart_items)

        if 'add_address' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = user
                address.save()
                messages.success(request, "Address added.")
                return redirect('checkout')
        elif 'place_order' in request.POST:
            # You would handle order creation, payment, etc.
            messages.success(request, "Order placed successfully!")
            return redirect('home')

        context = {
            'addresses': addresses,
            'address_form': address_form,
            'items_total': items_total,
        }
        return render(request, 'core/checkout.html', context)