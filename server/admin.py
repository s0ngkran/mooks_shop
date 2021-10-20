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
    def get_ordering(self, request):
        return ['-updated_on']

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','description','price','inventory','category_obj','barcode','updated_on')
    def get_ordering(self, request):
        return ['-updated_on']

admin.site.register(Product, ProductAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('updated_on','total','get_sub_text')
    def get_ordering(self, request):
        return ['-updated_on']

admin.site.register(Transaction, TransactionAdmin)
class SubTransactionAdmin(admin.ModelAdmin):
    list_display = ('product_obj','n_item')
    def get_ordering(self, request):
        return ['-updated_on']

admin.site.register(SubTransaction, SubTransactionAdmin)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('product_obj','n_item', 'price')
    def get_ordering(self, request):
        return ['-updated_on']

admin.site.register(Promotion, PromotionAdmin)