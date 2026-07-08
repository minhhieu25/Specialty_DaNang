from django.urls import path
from .views import ContactView, LoginView, RegisterView, LogoutView, ProfileView, ChangePasswordView, MyOrdersView

urlpatterns = [
    path('lien-he/', ContactView.as_view(), name='contact'),
    path('dang-nhap/', LoginView.as_view(), name='login'),
    path('dang-ky/', RegisterView.as_view(), name='register'),
    path('dang-xuat/', LogoutView.as_view(), name='logout'),
    path('ho-so/', ProfileView.as_view(), name='profile'),
    path('doi-mat-khau/', ChangePasswordView.as_view(), name='change_password'),
    path('don-hang/', MyOrdersView.as_view(), name='my_orders'),
]
