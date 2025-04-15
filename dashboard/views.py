from datetime import datetime
from decimal import Decimal
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import LoginForm, Product_Form, Purchase_Form, Sale_Form
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Product, Profile, Purchase, Sale
from .forms import Category_Form, Product_Form
from django_tables2 import RequestConfig
from django.shortcuts import render, redirect, get_object_or_404


from .tables import ProductTable, SaleTable,PurchaseTable
from .filters import ProductFilter, SaleFilter
from .filters import PurchaseFilter
from django.db.models import Q
from django.contrib.auth.models import User


def index_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/dashboard")
            else:
               form.add_error(None, 'Invalid username or password') 
       

    return render(request, "accounts/auth.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("index") 



# def home_view(request):
#     return render(request, "dashboard/home.html")

@login_required
def profile_view(request):
    profile, created =Profile.objects.get_or_create(user=request.user)
    return render(request, "accounts/profile.html", {"profile": profile})

@login_required
def dashboard_view(request):
    total_users = User.objects.count()
    total_categories = Category.objects.count()

    latest_sale = Sale.objects.order_by('-sale_date').first()
    latest_purchase = Purchase.objects.order_by('-purchasedate').first()

    total_expenses = latest_purchase.total_expenses() if latest_purchase else Decimal('0.00')

    # Default values
    profit = Decimal('0.00')
    loss = Decimal('0.00')

    if latest_sale:
        total_selling_price = Decimal('0.00')
        total_cost = Decimal('0.00')

        for detail in latest_sale.details.all():
            total_selling_price += detail.total_selling_price
            total_cost += (
                detail.total_buying_price +
                detail.allocated_buying_expense +
                detail.allocated_drying_expense +
                detail.allocated_selling_expense
            )

        result = total_selling_price - total_cost
        if result >= 0:
            profit = result
        else:
            loss = abs(result)

    context = {
        'total_users': total_users,
        'total_categories': total_categories,
        'latest_sale': latest_sale,
        'latest_purchase': latest_purchase,
        'total_expenses': total_expenses,
        'profit': profit,
        'loss': loss,
    }

    # Optional debug print
    if latest_sale:
        print(f"DEBUG - Sale ID: {latest_sale.id}, Selling Expenses: {latest_sale.selling_expenses}")
        print(f"\n===== SALE #{latest_sale.sale_number} ({latest_sale.quantitySold} units) =====")
        for detail in latest_sale.details.all():
            print(f"DETAIL: Product #{detail.product.product_number} | Qty: {detail.quantity}")
            print(f"  - Buying Cost: {detail.total_buying_price}")
            print(f"  - Buying Expense: {detail.allocated_buying_expense}")
            print(f"  - Drying Expense: {detail.allocated_drying_expense}")
            print(f"  - Selling Expense: {detail.allocated_selling_expense}")
            print(f"  - Total Cost: {detail.total_buying_price + detail.allocated_buying_expense + detail.allocated_drying_expense + detail.allocated_selling_expense}")
            print(f"  - Selling Price: {detail.total_selling_price}")
            print(f"  - Profit/Loss: {detail.profit_or_loss}")

    return render(request, 'dashboard/dashboard.html', context)
    

# # categories view
# def category_view(request):
#     form = Category_Form()
#     categories = Category.objects.all()
#     products = Product.objects.all() 

#     if request.method == 'POST' and 'category_submit' in request.POST:
#         form = Category_Form(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('category')

#     return render(request, "dashboard/category.html", {
#         "form": form,
#         "form_type": "category",
#         "categories": categories,
#         "products": products,
#     })


def category_view(request):
    category_form = Category_Form()
    product_form = Product_Form()

    if request.method == 'POST':
        if 'category_submit' in request.POST:
            category_form = Category_Form(request.POST)
            if category_form.is_valid():
                category_form.save()
                return redirect('category')
        elif 'product_submit' in request.POST:
            product_form = Product_Form(request.POST)
            if product_form.is_valid():
                product_form.save()
                return redirect('category')

    products = Product.objects.all()
    categories = Category.objects.all()

    return render(request, "dashboard/category.html", {
        "category_form": category_form,
        "product_form": product_form,
        "products": products,
        "categories": categories,
    })





def purchases_view(request):
    
    queryset =  Purchase.objects.all()

    search_term = request.GET.get("category_search", "")

    if search_term:
        # Filter categories that match the search term
        categories = Category.objects.filter(categoryName__icontains=search_term)
        
        # Get the ids of the matching categories
        category_ids = categories.values_list('id', flat=True)
        
        # Filter Sale objects by category ids
        queryset = queryset.filter(categoryName__in=category_ids)

         # Apply filter (if any) to the queryset
    purchase_filter = PurchaseFilter(request.GET, queryset=queryset)
       
         # Create the table and paginate the results
    table = PurchaseTable(purchase_filter.qs)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    # Render the template with filter and table data
    return render(request, "dashboard/purchase.html", {
        "filter": purchase_filter,
        "table": table
    })


def edit_purchase(request, id):
    purchase = get_object_or_404(Purchase, id=id)
    if request.method == 'POST':
        form = Purchase_Form(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            return redirect('purchases')  
    else:
        form = Purchase_Form(instance=purchase)
    return render(request, 'dashboard/edit_purchase.html', {'form': form})

# Delete Sale
def delete_purchase(request, id):
    purchase = get_object_or_404(Purchase, id=id)
    purchase.delete()

     # Reorder sale_numbers
    for index, s in enumerate(Purchase.objects.order_by('purchase_number'), start=1):
        s.purchase_number = index
        s.save(update_fields=['purchase_number'])

        
    return redirect('purchases')


def add_purchase_view(request):
    if request.method == 'POST':
        form = Purchase_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchases')  
    else:
        form = Purchase_Form()
    return render(request, 'dashboard/add_purchase.html', {'form': form})

def export_purchase_csv(request):
    # Create an HTTP response with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="purchase.csv"'
    
    # Create the CSV writer object
    writer = csv.writer(response)
    
    # Write the header row
    writer.writerow(['purchase_number','purchasedate','categoryName','supplierName','quantityPurchased','buyingPrice','buying_expenses'])
    
    # Write data rows
    purchases = Purchase.objects.all()
    for purchase in purchases:
        writer.writerow([purchase.purchase_number, purchase.purchasedate, purchase.categoryName, purchase.supplierName, purchase.quantityPurchased, purchase.buyingPrice, purchase.buying_expenses])
    
    return response



def export_purchase_pdf(request):
    # Create an HTTP response with the appropriate PDF MIME type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="purchases.pdf"'
    
    # Create a PDF canvas
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Write the title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 40, "Purchase Data")
    
    # Set up the column headers
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, height - 80, "Purchase Number")
    p.drawString(100, height - 80, "Purchase Date")
    p.drawString(200, height - 80, "Category")
    p.drawString(300, height - 80, "Supplier")#    'bd44-197-239-9-67.ngrok-free.app' 
    p.drawString(400, height - 80, "Quantity Purchased")
    p.drawString(500, height - 80, "Buying Price")
    p.drawString(600, height - 80, "Total Buying Price")
    p.drawString(700, height - 80, "Buying Expenses")
    
    # Write the data rows
    y_position = height - 100
    purchases = Purchase.objects.all()
    for purchase in purchases:
        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, str(purchase.purchase_number))
        p.drawString(100, y_position, str(purchase.purchasedate))
        p.drawString(200, y_position, str(purchase.categoryName))
        p.drawString(300, y_position, str(purchase.supplierName))
        p.drawString(400, y_position, str(purchase.quantityPurchased))
        p.drawString(500, y_position, str(purchase.buyingPrice))
        p.drawString(700, y_position, str(purchase.buying_expenses))
        
        y_position -= 20
        if y_position < 40: 
            p.showPage()
            y_position = height - 40
    
    # Save the PDF
    p.showPage()
    p.save()
    
    return response



def sales_view(request):
    # Initialize queryset for Sale model
    queryset = Sale.objects.all()

    # Check if a search term is provided
    search_term = request.GET.get("category_search", "")
    
    if search_term:
        # Filter categories that match the search term
        categories = Category.objects.filter(categoryName__icontains=search_term)
        
        # Get the ids of the matching categories
        category_ids = categories.values_list('id', flat=True)
        
        # Filter Sale objects by category ids
        queryset = queryset.filter(categoryName__in=category_ids)
    
    # Apply filter (if any) to the queryset
    sale_filter = SaleFilter(request.GET, queryset=queryset)
    
    # Create the table and paginate the results
    table = SaleTable(sale_filter.qs)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    # Render the template with filter and table data
    return render(request, "dashboard/sales.html", {
        "filter": sale_filter,
        "table": table
    })


def add_sale_view(request):
    if request.method == 'POST':
        form = Sale_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales')  
    else:
        form = Sale_Form()
    return render(request, 'dashboard/add_sale.html', {'form': form})


def export_sales_csv(request):
    # Create an HTTP response with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales.csv"'
    
    # Create the CSV writer object
    writer = csv.writer(response)
    
    # Write the header row
    writer.writerow(['ID', 'Sale Date', 'Category', 'Customer', 'Quantity Sold', 'Selling Price', 'Total Selling Price', 'Selling Expenses'])
    
    # Write data rows
    sales = Sale.objects.all()
    for sale in sales:
        writer.writerow([sale.id, sale.sale_date, sale.categoryName, sale.customerName, sale.quantitySold, sale.sellingPrice, sale.selling_expenses])
    
    return response



def export_sales_pdf(request):
    # Create an HTTP response with the appropriate PDF MIME type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales.pdf"'
    
    # Create a PDF canvas
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Write the title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 40, "Sales Data")
    
    # Set up the column headers
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, height - 80, "ID")
    p.drawString(100, height - 80, "Sale Date")
    p.drawString(200, height - 80, "Category")
    p.drawString(300, height - 80, "Customer")
    p.drawString(400, height - 80, "Quantity Sold")
    p.drawString(500, height - 80, "Selling Price")
    p.drawString(600, height - 80, "Total Selling Price")
    p.drawString(700, height - 80, "Selling Expenses")
    
    # Write the data rows
    y_position = height - 100
    sales = Sale.objects.all()
    for sale in sales:
        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, str(sale.id))
        p.drawString(100, y_position, str(sale.sale_date))
        p.drawString(200, y_position, str(sale.categoryName))
        p.drawString(300, y_position, str(sale.customerName))
        p.drawString(400, y_position, str(sale.quantitySold))
        p.drawString(500, y_position, str(sale.sellingPrice))
        p.drawString(700, y_position, str(sale.selling_expenses))
        
        y_position -= 20
        if y_position < 40: 
            p.showPage()
            y_position = height - 40
    
    # Save the PDF
    p.showPage()
    p.save()
    
    return response


def edit_sale(request, id):
    sale = get_object_or_404(Sale, id=id)
    if request.method == 'POST':
        form = Sale_Form(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('sales') 
    else:
        form = Sale_Form(instance=sale)
    return render(request, 'dashboard/edit_sale.html', {'form': form})

# Delete Sale
def delete_sale(request, id):
    sale = get_object_or_404(Sale, id=id)
    sale.delete()

     # Reorder sale_numbers
    for index, s in enumerate(Sale.objects.order_by('sale_number'), start=1):
        s.sale_number = index
        s.save(update_fields=['sale_number'])

        
    return redirect('sales')



def products_view(request):
    # Initialize queryset for Sale model
    queryset = Product.objects.all()

    # Check if a search term is provided
    search_term = request.GET.get("category_search", "")
    
    if search_term:
        # Filter categories that match the search term
        categories = Category.objects.filter(categoryName__icontains=search_term)
        
        # Get the ids of the matching categories
        category_ids = categories.values_list('id', flat=True)
        
        # Filter Sale objects by category ids
        queryset = queryset.filter(categoryName__in=category_ids)
    
    # Apply filter (if any) to the queryset
    product_filter = ProductFilter(request.GET, queryset=queryset)
    
    # Create the table and paginate the results
    table = ProductTable(product_filter.qs)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    # Render the template with filter and table data
    return render(request, "dashboard/products.html", {
        "filter": product_filter,
        "table": table
    })


def add_product_view(request):
    if request.method == 'POST':
        form = Product_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')  
    else:
        form = Product_Form()
    return render(request, 'dashboard/add-product.html', {'form': form})


def export_product_csv(request):
    # Create an HTTP response with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="product.csv"'
    
    # Create the CSV writer object
    writer = csv.writer(response)
    
    # Write the header row
    writer.writerow(['product_number','categoryName', 'driedWeight', 'drying_expenses', 'drying_status', 'drying_start_date', 'drying_end_date', 'quantity_purchased'])
    
    # Write data rows
    product = Product.objects.all()
    for products in product:
        writer.writerow([product.product_number, product.categoryName, product.driedWeight, product.drying_expenses, product.drying_status, product.drying_start_date,product.drying_end_date,product.quantity_purchased])
    
    return response


def export_product_pdf(request):
    # Create an HTTP response with the appropriate PDF MIME type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="product.pdf"'
    
    # Create a PDF canvas
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Write the title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 40, "Product Data")
    
    # Set up the column headers
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, height - 80, "product Number")
    p.drawString(100, height - 80, "Drying_start Date")
    p.drawString(200, height - 80, "Category")
    p.drawString(300, height - 80, "Quantity Purchased")
    p.drawString(400, height - 80, "Drying status")
    p.drawString(500, height - 80, "Dried Weight")
    p.drawString(600, height - 80, "Drying_end Date")
    p.drawString(700, height - 80, "Drying Expenses")
    
    # Write the data rows
    y_position = height - 100
    products = Product.objects.all()
    for product in products:
        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, str(product.product_number))
        p.drawString(100, y_position, str(product.categoryName))
        p.drawString(200, y_position, str(product.quantity_purchased))
        p.drawString(300, y_position, str(product.driedWeight))
        p.drawString(400, y_position, str(product.drying_status))
        p.drawString(500, y_position, str(product.drying_start_date))
        p.drawString(500, y_position, str(product.drying_end_date))
        p.drawString(700, y_position, str(product.drying_expenses))
        
        y_position -= 20
        if y_position < 40: 
            p.showPage()
            y_position = height - 40
    
    # Save the PDF
    p.showPage()
    p.save()
    
    return response

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

     #Check if product has already been dried and sold
    if product.drying_status == 'dried' and product.is_sold:
        messages.warning(request, "This product has already been dried and sold. It cannot be edited.")
        return redirect('products')
    
    if request.method == 'POST':
        form = Product_Form(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products') 
    else:
        form = Product_Form(instance=product)
    return render(request, 'dashboard/edit_product.html', {'form': form})

# Delete Product
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()

     # Reorder sale_numbers
    for index, s in enumerate(Product.objects.order_by('product_number'), start=1):
        s.product_number = index
        s.save(update_fields=['product_number'])

        
    return redirect('products')


