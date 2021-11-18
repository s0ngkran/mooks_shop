from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import uuid
class MyModel(models.Model):
    id = models.CharField(max_length=25, primary_key=True,
                          editable=False, default=uuid.uuid4, unique=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    created_by_username = models.CharField(
        max_length=255, default='not assigned')
    updated_by_username = models.CharField(
        max_length=255, default='not assigned')
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(null=True, blank=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.code)
class Category(MyModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return str(self.name)
    
class Product(MyModel):
    category_obj = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    barcode = models.CharField(max_length=25, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    inventory = models.IntegerField(default=0)
    def __str__(self):
        return str(self.name)

class Package(MyModel):
    category_obj = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    barcode = models.CharField(max_length=25, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    inventory = models.IntegerField(default=0)

    # product part
    product_obj = models.ForeignKey(Product,  on_delete=models.CASCADE, null=True, blank=True)
    n_item = models.IntegerField()

    def __str__(self):
        return str(self.name)
class PaymentType(MyModel):
    pass
class Transaction(MyModel):
    received = models.FloatField(null=True, blank=True)
    received_cash = models.FloatField(null=True, blank=True)
    received_online = models.FloatField(null=True, blank=True)
    balance = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    is_adjust = models.BooleanField(default=False)
    is_success = models.BooleanField(default=False)
    status = models.CharField(max_length=255, null=True, blank=True)
    discount_from_promotion = models.FloatField(null=True, blank=True)
    discount_from_promotion_on_group = models.FloatField(null=True, blank=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, null=True, blank=True)
    def get_sub_text(self):
        subs = self.subtransaction_set.all()
        text = ''
        for sub in subs:
            product_name = sub.product_obj.name
            n_item = sub.n_item
            sub_total = sub.product_obj.price * n_item
            text += '| %s x %d = %.2f '%(product_name, n_item, sub_total)

        return str(text)

class SubTransaction(MyModel):
    transaction_obj = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True)
    product_obj = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    n_item = models.IntegerField(default=1)
    is_adjust = models.BooleanField(default=False)
    price = models.FloatField(null=True, blank=True)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # first_name = models.CharField(max_length=255, null=True, blank=True)
    # last_name = models.CharField(max_length=255, null=True, blank=True)
    current_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    current_transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='hand', null=True, blank=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Promotion(MyModel):
    product_obj = models.ForeignKey(Product, on_delete=models.CASCADE)
    n_item = models.IntegerField()
    price = models.FloatField()

    # promotion and discount
class PromotionOnGroupPricing(MyModel):
    n_item = models.IntegerField()
    price = models.FloatField()
    def __str__(self):
        return str(self.n_item) +'->'+str(self.price)
class PromotionOnGroup(MyModel):
    products = models.ManyToManyField(Product, blank=True)
    pricings = models.ManyToManyField(PromotionOnGroupPricing, blank=True)
    def _products(self):
        text = ''
        for product in  self.products.all():
            text += str(product.name) + ' | '
        return text
    def _pricings(self):
        text = ''
        for pricing in self.pricings.all():
            text += str(pricing.n_item) + '->'+str(pricing.price)+' | '
        return text

class ChangeProduct(MyModel):
    old_product = models.ForeignKey(Product, related_name='change_product_old_product', on_delete=models.CASCADE)
    new_product = models.ForeignKey(Product, related_name='change_product_new_product', on_delete=models.CASCADE)
    balance = models.FloatField()







    
    