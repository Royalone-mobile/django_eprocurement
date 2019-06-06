from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from itertools import chain
import datetime

from purchasemanager.models import Vendor, Purchase, PurchaseItem, Expense, PurchaseAttachment, ExpenseAttachment	



# Accounting report
@login_required(login_url='login/')
def accounting(request):
	if request.method == 'POST':
		start = datetime.datetime.strptime(request.POST['start'], "%m/%d/%Y")
		end = datetime.datetime.strptime(request.POST['end'], "%m/%d/%Y")
		
		if start > end:
			context = {
				'error_message' : "Start date must be before end date!",
			}
			return render(request, 'accounting.html', context)
		else:
			paidpurchases = Purchase.objects.filter(date__gt=start).filter(date__lt=end).filter(status = 'Paid')
			allpurchases = Purchase.objects.filter(date__gt=start).filter(date__lt=end)
			expenses = Expense.objects.filter(date__gt=start).filter(date__lt=end)
			
			# Sum of all paid purchases
			purchasetotal = 0
			for i in paidpurchases:
				purchasetotal += i.total_items()
				
			# Add purchase expenses within date range, regardless of purchase status
			for i in allpurchases:
				expenses = list(chain(expenses, Expense.objects.filter(purchase=i)))
			
			# Sum of all expenses
			expensetotal = 0
			for expense in expenses:
				expensetotal += expense.total()
			
			context = {
				'start' : start,
				'end' : end,
				'purchases' : paidpurchases,
				'expenses' : expenses,
				'purchasetotal' : purchasetotal,
				'expensetotal' : expensetotal,
				'nettotal' : purchasetotal - expensetotal,
			}
			return render(request, 'accounting.html', context)
	else:
		return render(request, 'accounting.html')