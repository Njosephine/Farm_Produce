from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

# Product list view
def product_list(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'product_list.html', {'products': products})

# Add new product
def add_product(request):
    if request.method == 'POST':
        # Handle product creation
        name = request.POST['name']
        price = request.POST['price']
        product = Product(name=name, price=price)
        product.save()
        return redirect('product_list')
    return render(request, 'add_product.html')

# Edit product
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.save()
        return redirect('product_list')
    return render(request, 'edit_product.html', {'product': product})

# Delete product
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_list')
