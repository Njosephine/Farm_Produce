from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib import messages
from .forms import ProductForm  # Ensure this form is created
import datetime
from .models import Product, Transaction
from .forms import PurchaseForm


# Product list view
def product_list(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'product_list.html', {'products': products})


# Add new product
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Ensure this name is correct
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

# Edit product
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Fetch product or return 404
    
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect after saving
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})

# Delete product
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_list')

#displays only seasonal products based on the current season
def seasonal_product_list(request):
    current_month = datetime.datetime.now().month
    # Define which months belong to which seasons (e.g., Summer, Winter)
    if 3 <= current_month <= 5:
        season = 'Summer'
    elif 6 <= current_month <= 8:
        season = 'Fall'
    elif 9 <= current_month <= 11:
        season = 'Winter'
    else:
        season = 'Spring'
    
    seasonal_products = Product.objects.filter(seasonal=True, season=season)
    return render(request, 'seasonal_product_list.html', {'products': seasonal_products})


def record_purchase(request):
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity_purchased = form.cleaned_data['quantity_purchased']
            total_cost = form.cleaned_data['total_cost']

            # Record the transaction
            transaction = Transaction.objects.create(
                product=product,
                quantity_purchased=quantity_purchased,
                total_cost=total_cost
            )

            # Update the product's stock
            product.quantity_kg += quantity_purchased
            product.save()

            return redirect('product_list')  # Redirect to a product list page or wherever suitable
    else:
        form = PurchaseForm()
    
    return render(request, 'record_purchase.html', {'form': form})

# Add drying functionality
def reduce_drying_loss(request, product_id, weight_loss_percentage):
    product = Product.objects.get(id=product_id)
    dried_weight = product.quantity_kg * (1 - weight_loss_percentage / 100)
    product.quantity_kg = dried_weight
    product.save()
    return redirect('product_list')


# View to add a new product
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

# View to handle purchasing
#from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # For showing error messages
#from .models import Product

def purchase_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        purchased_kg = request.POST.get('purchased_kg')
        
        try:
            purchased_kg = float(purchased_kg)
            if purchased_kg <= 0:
                messages.error(request, "Quantity must be positive")
            else:
                # Update product stock
                product.quantity_kg += purchased_kg
                product.save()
                
                # Record transaction
                Transaction.objects.create(
                    product=product,
                    quantity_purchased=purchased_kg,
                    total_cost=purchased_kg * product.price_per_kg
                )
                messages.success(request, f"Added {purchased_kg}kg to {product.name}")
                return redirect('product_list')
                
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid number")

    return render(request, 'purchase_product.html', {
        'product': product,
        'current_stock': product.quantity_kg,
        'price_per_kg': product.price_per_kg
    })
