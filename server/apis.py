from mooks_shop.utils import *
from .models import *
from .sers import *

class APITest(APIView):
    permission_classes = [rfperm.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response('hi from get', status=200)

    def post(self, request):
        return Response('hi from post', status=200)

class APIPromotionOnGroup(MyAPIView):
    permission_classes = [rfperm.AllowAny]

    def get_product_list(self, barcode_list):
        product_list = []
        for barcode in barcode_list:
            products = Product.objects.filter(barcode=barcode)
            if len(products) != 1:
                continue
            product = products[0]

            # check duplicate with other groupPromotion
            promotions = PromotionOnGroup.objects.filter(products=product.id)
            if len(promotions) >= 1:
                # duplicated
                return []

            product_list.append(product.id)
        return product_list
    def get_cleaned_pricing_list(self, pricing_list):
        cleaned = []
        all_n_items = []
        for pricing in pricing_list:
            if type(pricing) != list:
                return []
            if len(pricing) != 2:
                return []
            n_item = int(pricing[0])
            price = float(pricing[1])

            # check duplicate n_item
            if n_item in all_n_items:
                return []
            cleaned.append([n_item, price])
            all_n_items.append(n_item)
        return cleaned

    def post(self, request):
        data = request.data
        # check barcode
        barcode_list = data.get('barcode_list')
        product_list = self.get_product_list(barcode_list)
        if product_list == []:
            return Response('Product is not valid', status=201)
        
        # check pricing
        pricing_list = data.get('pricing_list')
        pricing_list = self.get_cleaned_pricing_list(pricing_list)
        if pricing_list == []:
            return Response('Pricing is not valid', status=201)

        name = data.get('name')

        _ = {
            'code': name,
        }
        ser = PromotionOnGroupSer(data=_, many=False)
        if ser.is_valid():
            obj = ser.save()
            promotion = PromotionOnGroup.objects.get(id=obj.id)


            # create pricing
            pricings = []
            for pricing in pricing_list:
                n_item = pricing[0]
                price = pricing[1]
                pricing = PromotionOnGroupPricing.objects.create(n_item=n_item, price=price)
                pricings.append(pricing.id)
            
            # add pricing
            promotion.pricings.add(*pricings)
            # add products
            promotion.products.add(*product_list)

            return Response('success', status=200)
        else:
            print(ser.errors)
            return Response('fail', status=201)
