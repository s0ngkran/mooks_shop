from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
import datetime
import pytz
import rest_framework.permissions as rfperm

class MyAPIView(APIView):
    model = None
    serializer = None
    perm_get_groups = None
    perm_create_groups = None
    perm_update_groups = None
    is_allow_all = None
    permission_level = None

    def get_amount_from_price_control(self, nri, trn_res):
        # nri is non_room_item
        if nri.price_control == 'A':
            amount = nri.price * trn_res.adult
        elif nri.price_control == 'C':
            amount = nri.price * trn_res.child
        elif nri.price_control == 'P':
            amount = nri.price * (trn_res.adult + trn_res.child)
        elif nri.price_control == 'R':
            amount = nri.price
        return amount
    
    def add_day(self, date, daydiff):
        return date + datetime.timedelta(days=daydiff)

    def wrap_with_try(self, function, request):
        try:
            return function(request)
        except:
            self.func_if_fail(request)
            return Response('something wrong', status=400)

    def func_if_fail(self, request):
        return None
    
    def get(self, request):
        return self.wrap_with_try(self.fake_get, request)
    
    def post(self, request):
        return self.wrap_with_try(self.fake_post, request)

    def update_detail_for_create(self,request,detail):
        detail.update({
            'created_by_username': request.user.username,
            'updated_by_username': request.user.username,
            'created_on': timezone.now()
        })
    
    def update_detail_for_update(self,request,detail):
        detail.update({
            'updated_by_username': request.user.username,
        })
    
    def has_perm(self, request, *args, **kwargs):
        data = request.data
        act = data.get('act')
        if act == None:
            self.perm_groups = self.perm_get_groups
        elif act == 'create':
            self.perm_groups = self.perm_create_groups
        elif act == 'update':
            self.perm_groups = self.perm_update_groups

        # recheck
        if self.is_allow_all == True:
            assert self.perm_groups == None, 'DANGER: no need to set perm_[%s]_groups'%str(act)
        else:
            assert type(self.perm_groups) == list, 'DANGER: perm_groups must be a list'
            assert len(self.perm_groups) > 0, 'DANGER: Did you forgot to set perm_[%s]_groups?'%str(act)

        # allow all for super admin
        if request.user.is_superuser:
            return True
        
        # get user group
        user_groups = request.user.groups.all()

        assert type(self.perm_groups) == list
        # capsulation
        def get_has_perm(user_groups, perm_groups):
            for group in user_groups:
                group_name = group.name
                if group_name in perm_groups:
                    return True
            print('user perm = ', user_groups)
            print('To use this api, this user must have', perm_groups)
            return False

        return get_has_perm(user_groups, self.perm_groups)
    def is_valid_fields(self, data):
        field_names = [field.name for field in self.model._meta.get_fields()]
        for element in data:  # dat.type == list
            for key, value in element.items():
                if key not in field_names:
                    return False
        return True
    
    def get_aware_date(self, date_string, date_format=None):
        assert type(date_string) == str
        if date_format is None:
            date_format = '%Y-%m-%d'
        unaware_date = datetime.datetime.strptime(date_string, date_format)
        aware_date = pytz.utc.localize(unaware_date)
        return aware_date
    
    def print_dictionary(self, data):
        assert type(data) == dict
        print('')
        print('')
        print('')
        for key, value in data.items():
            print(key, value)
        print('')
        print('')
        print('')
