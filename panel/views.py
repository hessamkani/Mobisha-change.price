
from django.http import JsonResponse
from panel.models import Product
from panel.models import ProductPriceChange
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def get_product(request):
    name = request.POST.get('name')
    category = request.POST.get('category')
    price = request.POST.get('price')

    errors = []

    if name is None:
        errors.append("name field is required.")
    if category is None:
        errors.append("category field is required.")
    if price is None:
        errors.append("price field is required.")
    if errors:
        return JsonResponse({
            'ok': False,
            'errors': errors,
        }, status=400)

    product = Product.objects.create(name=name, category=category, price=price)
    ProductPriceChange.objects.create(price=price, product=product)

    return JsonResponse({
        'ok': True,
        'product_id': product.pk
    })


@api_view(['POST'])
def change_price(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    new_price = float(1.2) * float(product.price)

    ProductPriceChange.objects.create(product=product, price=product.price, new_price=new_price)

    product.price = new_price
    product.save()

    return JsonResponse({
        'ok': True,
        'product_id': product.pk,
    })


@api_view(['GET'])
def check_price(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    price_change = ProductPriceChange.objects.filter(product=product).latest('time')
    price_change_dict = {
        'product': price_change.product.name,
        'price': price_change.price,
        'new_price': price_change.new_price,
        'time': price_change.time
    }

    return JsonResponse(price_change_dict)


@api_view(['GET'])
def log(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    all_price_changes = ProductPriceChange.objects.filter(product=product)

    all_price_changes_list = \
        [
            {
                'product': price_change.product.name,
                'price': price_change.price,
                'new_price': price_change.new_price,
                'time': price_change.time
            }
            for price_change in all_price_changes
        ]
    return JsonResponse(all_price_changes_list, safe=False)
