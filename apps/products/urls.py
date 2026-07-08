from django.urls import path
from .views import DashboardView, ProductListView, ProductDetailView, SubmitReviewView, cart_add, cart_remove, cart_detail, AboutView, CheckoutView, OrderSuccessView

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('gioi-thieu/', AboutView.as_view(), name='about'),
    path('san-pham/', ProductListView.as_view(), name='product_list'),
    path('san-pham/danh-muc/<slug:category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
    path('san-pham/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('san-pham/<int:product_id>/add-review/', SubmitReviewView.as_view(), name='add_review'),
    path('gio-hang/', cart_detail, name='cart_detail'),
    path('gio-hang/add/<int:product_id>/', cart_add, name='cart_add'),
    path('gio-hang/remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('thanh-toan/', CheckoutView.as_view(), name='checkout'),
    path('thanh-toan/thanh-cong/<int:order_id>/', OrderSuccessView.as_view(), name='order_success'),
]
