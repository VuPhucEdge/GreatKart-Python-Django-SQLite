from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

from .models import Product

from carts.models import CartItem
from carts.views import _cart_id

from category.models import Category


def store(request, category_slug=None):
    categories = None
    products = None

    # filter by category
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories,
            is_available=True,
        )
        paginator = Paginator(products, 6)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available=True).order_by("id")
        paginator = Paginator(products, 6)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)

    context = {
        "products": paged_products,
    }

    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    # get single product
    try:
        single_product = Product.objects.get(
            category__slug=category_slug,
            slug=product_slug,
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request),
            product=single_product,
        ).exists()
    except Exception as e:
        raise e

    context = {
        "single_product": single_product,
        "in_cart": in_cart,
    }

    return render(request, "store/product_detail.html", context)


def search(request):
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]

        if keyword:
            products = Product.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword)
                or Q(product_name__icontains=keyword)
                or Q(category__icontains=keyword)
            )

    context = {
        "products": products,
    }

    return render(request, "store/store.html", context)
