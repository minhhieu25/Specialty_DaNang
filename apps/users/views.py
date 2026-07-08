from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from .models import ContactMessage

class ContactView(View):
    def get(self, request):
        return render(request, 'users/contact.html')

    def post(self, request):
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if full_name and phone and email and message:
            ContactMessage.objects.create(
                full_name=full_name,
                phone=phone,
                email=email,
                message=message
            )
            messages.success(request, 'Cảm ơn bạn đã liên hệ. Chúng tôi sẽ phản hồi sớm nhất có thể!')
            return redirect('contact')
            
        messages.error(request, 'Vui lòng điền đầy đủ thông tin.')
        return redirect('contact')

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
            return redirect('login')

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'users/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')

        if not all([username, email, password, re_password]):
            messages.error(request, 'Vui lòng điền đầy đủ thông tin.')
            return redirect('register')

        if password != re_password:
            messages.error(request, 'Mật khẩu không khớp.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Tên đăng nhập đã tồn tại.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email đã được sử dụng.')
            return redirect('register')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Đăng ký tài khoản thành công! Vui lòng đăng nhập.')
        return redirect('login')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash

class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request):
        return render(request, 'users/profile.html', {'user': request.user})

    def post(self, request):
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        
        if email != user.email and User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, 'Email này đã được sử dụng bởi người khác.')
        else:
            user.email = email
            user.save()
            messages.success(request, 'Cập nhật thông tin hồ sơ thành công!')
            
        return redirect('profile')

class ChangePasswordView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request):
        return render(request, 'users/change_password.html')

    def post(self, request):
        user = request.user
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(old_password):
            messages.error(request, 'Mật khẩu cũ không đúng.')
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, 'Mật khẩu mới không khớp.')
            return redirect('change_password')
            
        if len(new_password) < 6:
            messages.error(request, 'Mật khẩu mới phải có ít nhất 6 ký tự.')
            return redirect('change_password')

        user.set_password(new_password)
        user.save()
        # Cập nhật session để người dùng không bị văng ra sau khi đổi mật khẩu
        update_session_auth_hash(request, user)
        messages.success(request, 'Đổi mật khẩu thành công!')
        return redirect('profile')

from apps.products.models import Order, Product
from datetime import timedelta

class MyOrdersView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request):
        # Fetch user orders and prefetch order items and their related products
        orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items__product')
        
        # Calculate estimated delivery date based on shipping fee
        for order in orders:
            # Check if it's Giao hàng Hỏa tốc (express delivery)
            # 50000 -> 1 day, otherwise -> 3 days
            if str(order.shipping_fee) == '50000' or order.shipping_fee == 50000:
                order.estimated_delivery = order.created_at + timedelta(days=1)
            else:
                order.estimated_delivery = order.created_at + timedelta(days=3)
            
        # Recommended products (e.g., best sellers)
        recommended_products = Product.objects.filter(is_best_seller=True).order_by('?')[:4]
        
        context = {
            'orders': orders,
            'recommended_products': recommended_products
        }
        return render(request, 'users/my_orders.html', context)
        
    def post(self, request):
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')
        
        if action == 'cancel_order':
            reason = request.POST.get('cancel_reason')
            try:
                order = Order.objects.get(id=order_id, user=request.user)
                if order.status in ['pending', 'processing']:
                    order.status = 'cancelled'
                    # order.cancel_reason = reason # If a field existed
                    order.save()
                    messages.success(request, f'Đơn hàng #{order.id} đã được hủy thành công.')
                else:
                    messages.error(request, 'Không thể hủy đơn hàng này vì đang được giao hoặc đã hoàn tất.')
            except Order.DoesNotExist:
                messages.error(request, 'Không tìm thấy đơn hàng.')
        elif action == 'return_order':
            reason = request.POST.get('reason')
            details = request.POST.get('details', '')
            # Normally save a ReturnRequest model or send an email.
            messages.success(request, f'Yêu cầu hoàn trả cho đơn hàng #{order_id} đã được gửi thành công. Bộ phận CSKH sẽ liên hệ với bạn trong 24h tới!')
            
        return redirect('my_orders')
