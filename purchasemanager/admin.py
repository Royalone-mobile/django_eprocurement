from django.contrib import admin

# Register your models here.
from .models import Vendor
from .models import Product
from .models import Purchase
from .models import PurchaseAttachment
from .models import ExpenseAttachment
from .models import Expense

admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Expense)