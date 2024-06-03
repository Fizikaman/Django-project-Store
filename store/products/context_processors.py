from products.models import Basket

def basket(request):
    user = request.user
    return {'baskets': Basket.objects.select_related('user', 'product').filter(user=user) if user.is_authenticated else []}