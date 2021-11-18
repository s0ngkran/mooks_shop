from django.contrib import admin
from .models import *


# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('updated_on','user')
#     def get_ordering(self, request):
#         return ['-updated_on']

# admin.site.register(Profile, ProfileAdmin)

# admin.site.register(UserImage)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'updated_on')
    search_fields = ['name', 'description']
    def get_ordering(self, request):
        return ['-updated_on']

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','description','price','inventory','category_obj','barcode','updated_on')
    search_fields = ['name', 'description', 'price', 'category_obj__name','barcode']
    def get_ordering(self, request):
        return ['-updated_on']

admin.site.register(Product, ProductAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('updated_on','total','get_sub_text', 'received', 'received_cash', 'received_online')
    search_fields = ['total', 'updated_on']
    def get_ordering(self, request):
        return ['-updated_on']

admin.site.register(Transaction, TransactionAdmin)
class SubTransactionAdmin(admin.ModelAdmin):
    list_display = ('product_obj','n_item')
    search_fields = ['product_obj__name', 'n_item']
    def get_ordering(self, request):
        return ['-updated_on']

admin.site.register(SubTransaction, SubTransactionAdmin)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('product_obj','n_item', 'price')
    search_fields = ['product_obj__name', 'n_item', 'price', 'name','code']
    def get_ordering(self, request):
        return ['-updated_on']

admin.site.register(Promotion, PromotionAdmin)
class PromotionOnGroupAdmin(admin.ModelAdmin):
    list_display = ('code', '_products', '_pricings')
    search_fields = ['code', '_products', '_pricings']
    def get_ordering(self, request):
        return ['-updated_on']

admin.site.register(PromotionOnGroup, PromotionOnGroupAdmin)