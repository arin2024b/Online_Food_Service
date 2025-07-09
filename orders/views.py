from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from restaurants.models import MenuItem, Restaurant
from .models import Order, OrderItem, PromoCode, Review
from users.models import Address
from decimal import Decimal

def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

def cart_view(request):
    cart = get_cart(request)
    items = []
    total = Decimal('0.00')
    for item_id, item_data in cart.items():
        menu_item = get_object_or_404(MenuItem, pk=item_id)
        quantity = item_data['quantity']
        item_total = menu_item.price * quantity
        total += item_total
        items.append({'item': menu_item, 'quantity': quantity, 'item_total': item_total})
    promo_code = request.session.get('promo_code')
    discount = Decimal('0.00')
    promo_obj = None
    if promo_code:
        try:
            promo_obj = PromoCode.objects.get(code=promo_code)
            if promo_obj.is_percentage:
                discount = total * (promo_obj.discount / 100)
            else:
                discount = promo_obj.discount
        except PromoCode.DoesNotExist:
            pass
    grand_total = max(total - discount, Decimal('0.00'))
    return render(request, 'orders/cart.html', {
        'items': items,
        'total': total,
        'discount': discount,
        'grand_total': grand_total,
        'promo_code': promo_code,
    })

def add_to_cart_view(request, item_id):
    cart = get_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += quantity
    else:
        cart[str(item_id)] = {'quantity': quantity}
    save_cart(request, cart)
    messages.success(request, 'Item added to cart!')
    return redirect('cart')

def remove_from_cart_view(request, item_id):
    cart = get_cart(request)
    if str(item_id) in cart:
        del cart[str(item_id)]
        save_cart(request, cart)
        messages.success(request, 'Item removed from cart!')
    return redirect('cart')

def update_cart_view(request, item_id):
    cart = get_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] = quantity
        save_cart(request, cart)
        messages.success(request, 'Cart updated!')
    return redirect('cart')

def apply_promo_code_view(request):
    code = request.POST.get('promo_code', '').strip()
    try:
        promo = PromoCode.objects.get(code=code)
        request.session['promo_code'] = code
        messages.success(request, 'Promo code applied!')
    except PromoCode.DoesNotExist:
        messages.error(request, 'Invalid promo code!')
    return redirect('cart')

@login_required
def checkout_view(request):
    cart = get_cart(request)
    if not cart:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')
    items = []
    total = Decimal('0.00')
    restaurant = None
    for item_id, item_data in cart.items():
        menu_item = get_object_or_404(MenuItem, pk=item_id)
        if not restaurant:
            restaurant = menu_item.category.restaurant
        quantity = item_data['quantity']
        item_total = menu_item.price * quantity
        total += item_total
        items.append({'item': menu_item, 'quantity': quantity, 'item_total': item_total})
    promo_code = request.session.get('promo_code')
    discount = Decimal('0.00')
    promo_obj = None
    if promo_code:
        try:
            promo_obj = PromoCode.objects.get(code=promo_code)
            if promo_obj.is_percentage:
                discount = total * (promo_obj.discount / 100)
            else:
                discount = promo_obj.discount
        except PromoCode.DoesNotExist:
            pass
    grand_total = max(total - discount, Decimal('0.00'))
    addresses = request.user.addresses.all()
    if request.method == 'POST':
        address_id = request.POST.get('address')
        address = get_object_or_404(Address, pk=address_id, user=request.user)
        order = Order.objects.create(
            user=request.user,
            restaurant=restaurant,
            total=grand_total,
            delivery_address=address,
            status='placed',
            promo_code=promo_obj if promo_obj else None,
        )
        for entry in items:
            OrderItem.objects.create(
                order=order,
                menu_item=entry['item'],
                quantity=entry['quantity'],
                price=entry['item'].price,
            )
        request.session['cart'] = {}
        request.session['promo_code'] = ''
        messages.success(request, 'Order placed successfully!')
        return redirect('order_success', order_id=order.pk)
    return render(request, 'orders/checkout.html', {
        'items': items,
        'total': total,
        'discount': discount,
        'grand_total': grand_total,
        'addresses': addresses,
    })

@login_required
def order_success_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    can_review = order.status == 'delivered' and not Review.objects.filter(user=request.user, restaurant=order.restaurant, menu_item=None).exists()
    return render(request, 'orders/order_detail.html', {'order': order, 'can_review': can_review})

@login_required
def submit_review_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    if order.status != 'delivered':
        messages.error(request, 'You can only review delivered orders.')
        return redirect('order_detail', order_id=order.pk)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')
        Review.objects.create(user=request.user, restaurant=order.restaurant, rating=rating, comment=comment)
        messages.success(request, 'Thank you for your review!')
        return redirect('order_detail', order_id=order.pk)
    return render(request, 'orders/submit_review.html', {'order': order})
