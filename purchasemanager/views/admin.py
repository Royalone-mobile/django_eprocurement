from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import datetime

from purchasemanager.models import Vendor, Product, Purchase, PurchaseItem, Expense, PurchaseAttachment, ExpenseAttachment	
from django.contrib.auth.models import User




# Administrative settings
def users(request):
    return None #User.objects.all()


def settings(request):
    return None
