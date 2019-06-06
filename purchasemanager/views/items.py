from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from purchasemanager.models import Vendor, Purchase, PurchaseItem, Expense, PurchaseAttachment, ExpenseAttachment



# Add purchaseitem to purchase
@login_required(login_url='login/')
def add_item(request, purchase_id):
	purchase = get_object_or_404(Purchase, pk=purchase_id)
	try:
		i = purchase.purchaseitem_set.create(name=request.POST['name'], description=request.POST['description'], cost=request.POST['cost'], qty=request.POST['qty'])
		i.save()
	except (KeyError, Purchase.DoesNotExist):
		return render(request, 'view_purchase.html', {
			'purchase': purchase,
			'error_message': 'Not all fields were completed.',
		})
	else:
		return HttpResponseRedirect(reverse('purchasemanager:purchase', args=(purchase.id,)))



# Delete purchaseitem from purchase
@login_required(login_url='login/')
def delete_item(request, purchaseitem_id, purchase_id):
	
	item = get_object_or_404(PurchaseItem, pk=purchaseitem_id)
	purchase = get_object_or_404(Purchase, pk=purchase_id)
	try:
		item.delete()
	except (KeyError, PurchaseItem.DoesNotExist):
		return render(request, 'view_purchase.html', {
			'purchase': purchase,
			'error_message': 'Item does not exist.',
		})
	else:
		return HttpResponseRedirect(reverse('purchasemanager:purchase', args=(purchase.id,)))