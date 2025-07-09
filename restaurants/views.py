from django.shortcuts import render, get_object_or_404
from .models import Restaurant, MenuCategory, MenuItem
from django.db.models import Q

# Create your views here.

def restaurant_list(request):
    query = request.GET.get('q', '')
    cuisine = request.GET.get('cuisine', '')
    min_rating = request.GET.get('rating', '')
    restaurants = Restaurant.objects.filter(is_approved=True)
    if query:
        restaurants = restaurants.filter(Q(name__icontains=query) | Q(address__icontains=query) | Q(cuisine_type__icontains=query))
    if cuisine:
        restaurants = restaurants.filter(cuisine_type__icontains=cuisine)
    if min_rating:
        try:
            min_rating = float(min_rating)
            restaurants = restaurants.filter(rating__gte=min_rating)
        except ValueError:
            pass
    cuisines = Restaurant.objects.values_list('cuisine_type', flat=True).distinct()
    return render(request, 'restaurants/restaurant_list.html', {
        'restaurants': restaurants,
        'cuisines': cuisines,
        'query': query,
        'selected_cuisine': cuisine,
        'selected_rating': min_rating,
    })

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, is_approved=True)
    categories = restaurant.categories.all()
    menu_items = MenuItem.objects.filter(category__restaurant=restaurant, is_available=True)
    return render(request, 'restaurants/restaurant_detail.html', {
        'restaurant': restaurant,
        'categories': categories,
        'menu_items': menu_items,
    })
