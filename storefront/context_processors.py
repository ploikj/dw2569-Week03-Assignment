from .models import Cart

def cart_context(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    cart = Cart.objects.filter(session_key=session_key).first()
    cart_count = 0
    if cart:
        cart_count = sum(item.quantity for item in cart.items.all())
    return {'cart_count': cart_count}
