from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from django.contrib import messages

def get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def index(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    categories = Category.objects.all()
    products = Product.objects.all().order_by('-sold')
    
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    if category_id:
        products = products.filter(category_id=category_id)
        
    context = {
        'categories': categories,
        'products': products[:20],
        'current_category': int(category_id) if category_id else None,
        'query': query
    }
    return render(request, 'storefront/index.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'storefront/detail.html', context)

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        session_key = get_session_key(request)
        
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
            
        messages.success(request, f'เพิ่ม "{product.name}" ลงในรถเข็นแล้ว')
        return redirect('cart_view')
        
    return redirect('storefront_index')

def cart_view(request):
    session_key = get_session_key(request)
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    context = {
        'cart': cart
    }
    return render(request, 'storefront/cart.html', context)

def checkout(request):
    session_key = get_session_key(request)
    cart = Cart.objects.filter(session_key=session_key).first()
    
    if not cart or cart.items.count() == 0:
        messages.error(request, 'ตะกร้าสินค้าว่างเปล่า')
        return redirect('storefront_index')
        
    if request.method == 'POST':
        # Create Order
        order = Order.objects.create(
            session_key=session_key,
            total_amount=cart.total_price()
        )
        
        # Move items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            # Update stock and sold
            item.product.stock -= item.quantity
            item.product.sold += item.quantity
            item.product.save()
            
        # Clear cart
        cart.delete()
        messages.success(request, 'สั่งซื้อสำเร็จ! ขอบคุณที่ใช้บริการ')
        return redirect('storefront_index')
        
    return redirect('cart_view')
