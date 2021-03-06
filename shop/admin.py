from django.contrib import admin
from shop.models import Store
from shop.models import StoreCustomization
from shop.models import DeliveryOption
from shop.models import Category
from shop.models import ItemMetaFilter
from shop.models import Item
from shop.models import ItemMeta

class StoreAdmin(admin.ModelAdmin):
  list_display = ['name', 'id', 'address']
  ordering = ['-id']
  search_fields = ['id', 'name']
  prepopulated_fields = { 'slug': ['name'] }

admin.site.register(Store, StoreAdmin)

class StoreCustomizationAdmin(admin.ModelAdmin):
  list_display = ['store', 'featured', 'show_banner', 'show_on_sale', 'show_best_selling']
  search_fields = ['store__name']
  list_filter = ['show_banner', 'show_on_sale', 'show_best_selling']

admin.site.register(StoreCustomization, StoreCustomizationAdmin)

class DeliveryOptionAdmin(admin.ModelAdmin):
  list_display = ['id', 'store', 'name', 'display_name', 'start_time', 'time_interval', 'weekday_availability', 'cost']
  ordering = ['store', 'start_time']
  list_filter = ['store', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

admin.site.register(DeliveryOption, DeliveryOptionAdmin)

class CategoryAdmin(admin.ModelAdmin):
  list_display = ['__unicode__', 'id', 'store', 'icon', 'shop_order']
  ordering = ['store', 'parent']
  search_fields = ['name']
  list_filter = ['store']
  raw_id_fields = ['parent']
  prepopulated_fields = { 'slug': ['name'] }

admin.site.register(Category, CategoryAdmin)

class ItemAdmin(admin.ModelAdmin):
  date_hierarchy = 'when_added'
  list_display = [
    'name', 'id', 'price', 'sales_price', 'category',
    'sold_number', 'out_of_stock', 'on_sale'
  ]
  list_filter = [ 'out_of_stock', 'on_sale', 'tax_class', 'featured' ]
  raw_id_fields = ['category']
  ordering = [ '-id' ]
  search_fields = ['id', 'name', 'sku', 'category__name', 'featured']
  actions = ['remove_sales']

  def remove_sales(self, request, queryset):
    rows_updated = queryset.update(on_sale=False)
    if rows_updated == 1:
        message_bit = "1 item was "
    else:
        message_bit = "%s items were" % rows_updated
    self.message_user(request, "%s successfully marked as not on sale." % message_bit)
  remove_sales.short_description = "Mark as not on sale"

admin.site.register(Item, ItemAdmin)

class ItemMetaAdmin(admin.ModelAdmin):
  list_display = ['id', 'key', 'value', 'item']
  ordering = [ 'item' ]
  search_fields = ['item__name', 'key', 'value']
  raw_id_fields = ['item']

admin.site.register(ItemMeta, ItemMetaAdmin)

class ItemMetaFilterAdmin(admin.ModelAdmin):
  list_display = ['key', 'display_order', 'filterable']
  ordering = ['display_order']
  search_fields = ['key']
  list_filter = ['filterable']

admin.site.register(ItemMetaFilter, ItemMetaFilterAdmin)
