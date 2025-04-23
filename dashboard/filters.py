import django_filters
from .models import Category, Product, Purchase, Sale

class SaleFilter(django_filters.FilterSet):
    categoryName = django_filters.CharFilter(method='filter_category_name')

    class Meta:
        model = Sale
        fields = []

    def filter_category_name(self, queryset, name, value):
        # Get Category objects matching the search term
        categories = Category.objects.filter(categoryName__icontains=value)
        
        # Get the ids of the matching categories
        category_ids = categories.values_list('id', flat=True)
        
        # Filter Sale objects by matching category IDs
        return queryset.filter(categoryName__in=category_ids)
    

class PurchaseFilter(django_filters.FilterSet):
      categoryName = django_filters.CharFilter(method='filter_category_name')

      class Meta:
        model = Purchase
        fields = []

      def filter_category_name(self, queryset, name, value):
        # Get Category objects matching the search term
        categories = Category.objects.filter(categoryName__icontains=value)
        
        # Get the ids of the matching categories
        category_ids = categories.values_list('id', flat=True)
        
        # Filter Sale objects by matching category IDs
        return queryset.filter(categoryName__in=category_ids)


class ProductFilter(django_filters.FilterSet):
      categoryName = django_filters.CharFilter(method='filter_category_name')

      class Meta:
        model = Product
        fields = []

      def filter_category_name(self, queryset, name, value):
        # Get Category objects matching the search term
        categories = Category.objects.filter(categoryName__icontains=value)
        
        # Get the ids of the matching categories
        category_ids = categories.values_list('id', flat=True)
        
        # Filter Sale objects by matching category IDs
        return queryset.filter(categoryName__in=category_ids)

