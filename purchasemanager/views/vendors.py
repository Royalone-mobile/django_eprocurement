from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime

from purchasemanager.models import Vendor, Purchase, PurchaseItem, Expense, PurchaseAttachment, ExpenseAttachment



# List all vendors
@login_required(login_url='login/')
def vendor_list(request):
	vendors = Vendor.objects.all()
	context = {
		'title' : 'Vendor List',
		'vendors' : vendors,
	}
	return render(request, 'vendors.html', context)
	
	
	
# Show specific vendor details
@login_required(login_url='login/')
def vendor(request, vendor_id):
	vendor = get_object_or_404(Vendor, pk=vendor_id)
	purchases = Purchase.objects.filter(vendor = vendor)
	context = {
		'title' : "Vendor info - %s" % vendor.name,
		'vendor' : vendor,
		'purchases' : purchases,
	}
	return render(request, 'vendor.html', context)

	
	
# Add new vendor
@login_required(login_url='login/')
def new_vendor(request):
	if request.method == 'POST':
		# Stuff from form
		c = Vendor(name=request.POST['name'], address1=request.POST['address1'], address2=request.POST['address2'], atoll=request.POST['atoll'], island=request.POST['island'],  email=request.POST['email'])
		c.save()
		
		if 'savecreate' in request.POST:
			i = Purchase(vendor=c, date=datetime.date.today(), status='Unpaid')
			i.save()
			return HttpResponseRedirect(reverse('purchasemanager:purchase', args=(i.id,)))
		else:
			return HttpResponseRedirect(reverse('purchasemanager:vendor_list'))
	else:
		return render(request, 'new_vendor.html')



# Update vendor
@login_required(login_url='login/')
def update_vendor(request, vendor_id):
	# Stuff from form
	c = get_object_or_404(Vendor, pk=vendor_id)
	
	c.name = request.POST['name']
	c.address1 = request.POST['address1']
	c.address2 = request.POST['address2']
	c.atoll = request.POST['atoll']
	c.island = request.POST['island']
	c.email = request.POST['email']
	
	c.save()
	
	return HttpResponseRedirect(reverse('purchasemanager:vendor', args=(c.id,)))

		
# Delete vendor
@login_required(login_url='login/')
def delete_vendor(request, vendor_id):
	vendor = get_object_or_404(Vendor, pk=vendor_id)
	vendor.delete()
	return HttpResponseRedirect(reverse('purchasemanager:vendor_list'))