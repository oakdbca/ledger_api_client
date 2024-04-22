from django.core.exceptions import PermissionDenied

from ledger_api_client import helpers
from ledger_api_client import utils
from ledger_api_client import ledger_models

class InvoiceOwnerMixin(object):

    #def belongs_to(self, user, group_name):
    #    return helpers.belongs_to(user, group_name)

    def is_payment_admin(self,user):
        return helpers.is_payment_admin(user)

    def check_owner(self, user):
        user_id = user.id
        if user_id:
            order_number = self.get_object().order_number
            order = utils.Order.objects.get(number=order_number)
            user = ledger_models.EmailUserRO.objects.get(id=user_id)        
            return order.user_id == user_id or self.is_payment_admin(user)
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.check_owner(request.user):
            raise PermissionDenied
        return super(InvoiceOwnerMixin, self).dispatch(request, *args, **kwargs)


