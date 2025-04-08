import django_tables2 as tables
from .models import Product, Purchase, Sale

class SaleTable(tables.Table):
    totalSellingPrice = tables.Column(accessor='totalSellingPrice', verbose_name="Total Selling Price")
    sale_date = tables.DateColumn(format="Y-m-d", verbose_name="Sale Date")
    def render_sale_date(self, value):
         if value:
            return value.strftime('%d-%m-%Y')
         return ''
    
      # Adding the action column
    actions = tables.TemplateColumn(
        template_name="dashboard/actions_column.html", verbose_name="Action"
    )
      
    class Meta:
        model = Sale
        fields = ('sale_number','sale_date', 'categoryName', 'customerName', 'quantitySold', 'sellingPrice', 'selling_expenses')
        attrs = {"class": "table table-striped"}
        template_name = "django_tables2/bootstrap5.html" 
        

class PurchaseTable(tables.Table):
    totalBuyingPrice = tables.Column(accessor='totalBuyingPrice', verbose_name="Total Buying Price")
    purchasedate = tables.DateColumn(format="Y-m-d", verbose_name="Purchase Date")
    def render_purchase_date(self, value):
         if value:
            return value.strftime('%d-%m-%Y')
         return ''
    
      # Adding the action column
    actions = tables.TemplateColumn(
        template_name="dashboard/purchase_action.html", verbose_name="Action"
    )
      
    class Meta:
        model = Purchase
        fields = ('purchase_number','purchasedate','categoryName','supplierName','quantityPurchased','buyingPrice','buying_expenses')
        attrs = {"class": "table table-striped"}
        template_name = "django_tables2/bootstrap5.html"


class ProductTable(tables.Table):
 
    drying_start_date = tables.DateColumn(format="Y-m-d", verbose_name="Start_Drying Date")
    drying_end_date = tables.DateColumn(format="Y-m-d", verbose_name="End_Drying Date")
    def render_drying_start_date(self, value):
         if value:
            return value.strftime('%d-%m-%Y')
         return ''
    
    def render_drying_end_date(self, value):
         if value:
            return value.strftime('%d-%m-%Y')
         return ''
    
      # Adding the action column
    actions = tables.TemplateColumn(
        template_name="dashboard/product_action.html", verbose_name="Action"
    )
      
    class Meta:
        model = Product
        fields = ('product_number','categoryName', 'quantity_purchased','drying_start_date', 'drying_status', 'drying_end_date', 'driedWeight','drying_expenses')
        attrs = {"class": "table table-striped"}
        template_name = "django_tables2/bootstrap5.html"
