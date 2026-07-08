from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from .models import Product, Category, Review

class DashboardView(ListView):
    model = Product
    template_name = 'dashboard.html'
    context_object_name = 'products'

    def get_queryset(self):
        sort = self.request.GET.get('sort', 'popular')
        qs = Product.objects.all()
        
        if sort == 'newest':
            qs = qs.order_by('-created_at')
        elif sort == 'price_asc':
            qs = qs.order_by('price')
        elif sort == 'price_desc':
            qs = qs.order_by('-price')
        elif sort == 'bestseller':
            qs = qs.filter(is_best_seller=True)
        else:
            # popular (default): mix of best sellers and others or just default ordering
            qs = qs.order_by('-is_best_seller', '-created_at')
            
        return qs[:12]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.blog.models import Article
        context['latest_articles'] = Article.objects.filter(is_featured=True).order_by('-created_at')[:3]
        if not context['latest_articles']:
            context['latest_articles'] = Article.objects.all().order_by('-created_at')[:3]
        
        context['testimonials'] = Review.objects.filter(rating__gte=4).order_by('-created_at')[:3]
        return context

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 9 # Adjust based on how many you want per page

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)
        else:
            self.category = None
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.category
        return context

from django.views.decorators.http import require_POST
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Check if quantity and update flags are provided
    quantity = int(request.POST.get('quantity', 1))
    update_qty = request.POST.get('update', 'False') == 'True'
    
    cart.add(product=product, quantity=quantity, override_quantity=update_qty)
    
    # Only show success message if not just updating quantity
    if not update_qty:
        messages.success(request, f'Đã thêm {product.name} vào giỏ hàng.')
        
    return redirect('cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'Đã xóa {product.name} khỏi giỏ hàng.')
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'products/cart.html', {'cart': cart})

class AboutView(View):
    def get(self, request):
        return render(request, 'products/about.html')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

class SubmitReviewView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        rating = request.POST.get('rating', 5)
        content = request.POST.get('content', '')
        # Simple default name if not logged in
        customer_name = request.user.username if request.user.is_authenticated else "Khách hàng ẩn danh"
        
        Review.objects.create(
            product=product,
            customer_name=customer_name,
            rating=rating,
            content=content
        )
        messages.success(request, 'Cảm ơn bạn đã gửi đánh giá!')
        return redirect('product_detail', slug=product.slug)

from .models import Order, OrderItem

class CheckoutView(View):
    def get(self, request):
        cart = Cart(request)
        if len(cart) == 0:
            return redirect('cart_detail')
        return render(request, 'products/checkout.html', {'cart': cart})

    def post(self, request):
        cart = Cart(request)
        if len(cart) == 0:
            return redirect('cart_detail')

        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        note = request.POST.get('note', '')
        payment_method = request.POST.get('payment_method', 'cod')
        shipping_fee = int(request.POST.get('shipping_fee', 0))

        total_price = cart.get_total_price() + shipping_fee

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone=phone,
            email=email,
            address=address,
            note=note,
            payment_method=payment_method,
            shipping_fee=shipping_fee,
            total_price=total_price,
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        # Clear the cart
        cart.clear()

        return redirect('order_success', order_id=order.id)

class OrderSuccessView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'products/order_success.html', {'order': order})
