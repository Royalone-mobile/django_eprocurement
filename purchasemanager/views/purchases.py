from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import datetime

from purchasemanager.models import Vendor, Purchase, PurchaseItem, Expense, PurchaseAttachment, ExpenseAttachment



# Default purchase list, show 25 recent purchases
@login_required(login_url='login/')
def index(request):
    purchases = Purchase.objects.order_by('-date')[:25]
    context = {
		'title' : 'Recent Purchases',
        'purchase_list' : purchases,
    }
    return render(request, 'index.html', context)

	
	
	
# Show big list of all purchases
@login_required(login_url='login/')
def all_purchases(request):
    purchases = Purchase.objects.order_by('-date')
    context = {
		'title' : 'All Purchases',
        'purchase_list' : purchases,
    }
    return render(request, 'index.html', context)
	
	
	
# Show draft purchases
@login_required(login_url='login/')
def draft_purchases(request):
    purchases = Purchase.objects.filter(status='Draft').order_by('-date')
    context = {
		'title' : 'Draft Purchases',
        'purchase_list' : purchases,
    }
    return render(request, 'index.html', context)

	
	
# Show paid purchases
@login_required(login_url='login/')
def paid_purchases(request):
    purchases = Purchase.objects.filter(status='Paid').order_by('-date')
    context = {
		'title' : 'Paid Purchases',
        'purchase_list' : purchases,
    }
    return render(request, 'index.html', context)

	
	
# Show unpaid purchases
@login_required(login_url='login/')
def unpaid_purchases(request):
    purchases = Purchase.objects.filter(status='Unpaid').order_by('-date')
    context = {
		'title' : 'Unpaid Purchases',
        'purchase_list' : purchases,
    }
    return render(request, 'index.html', context)

	
	
# Display a specific purchase
@login_required(login_url='login/')
def purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    context = {
		'title' : 'Purchase ' + purchase_id,
	    'purchase' : purchase,
	}
    return render(request, 'purchase.html', context)
	
	
	
# Search for purchase
@login_required(login_url='login/')
def search_purchase(request):
    id = request.POST['id']
    return HttpResponseRedirect(reverse('purchasemanager:purchase', args=(id,)))



# Create new purchase
@login_required(login_url='login/')
def new_purchase(request):
	# If no vendor_id is defined, create a new purchase
	if request.method=='POST':
		vendor_id = request.POST['vendor_id']
		
		if vendor_id=='None':
			vendors = Vendor.objects.order_by('name')
			context = {
				'title' : 'New Purchase',
				'vendor_list' : vendors,
				'error_message' : 'Please select a vendor.',
				}
			return render(request, 'new_purchase.html', context)
		else:
			vendor = get_object_or_404(Vendor, pk=vendor_id)
			i = Purchase(vendor=vendor, date=datetime.date.today(), status='Unpaid')
			i.save()
			return HttpResponseRedirect(reverse('purchasemanager:purchase', args=(i.id,)))
			
	else:
		# Vendor list needed to populate select field
		vendors = Vendor.objects.order_by('name')
		context = {
			'title' : 'New Purchase',
			'vendor_list' : vendors,
		}
		return render(request, 'new_purchase.html', context)



# Print purchase
@login_required(login_url='login/')
def print_purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    context = {
		'title' : "Purchase " + purchase_id,
	    'purchase' : purchase,
	}
    return render(request, 'print_purchase.html', context)



# Delete an purchase
@login_required(login_url='login/')
def delete_purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    purchase.delete()
    return HttpResponseRedirect(reverse('purchasemanager:index'))
	
	
	
# Update purchase
@login_required(login_url='login/')
def update_purchase(request, purchase_id):
	purchase = get_object_or_404(Purchase, pk=purchase_id)
	try:
		purchase.date = datetime.datetime.strptime(request.POST['date'], "%m/%d/%Y")
		purchase.status = request.POST['status']
		purchase.save()
	except (KeyError, Purchase.DoesNotExist):
		return render(request, 'purchase.html', {
			'purchase': purchase,
			'error_message': 'Not able to update purchase!',
		})
	else:
		context = {
			'confirm_update' : True,
			'title' : 'Purchase ' + purchase_id,
			'purchase' : purchase,
			}
		return render(request, 'purchase.html', context)



# Upload attachment for purchase
@login_required(login_url='login/')
def upload_purchase_attachment(request, purchase_id):
    myfile = request.FILES['file']
    purchase = get_object_or_404(Purchase, pk=purchase_id)

    fs = FileSystemStorage()
    fs.save(myfile.name, myfile)

    e = purchase.purchaseattachment_set.create(file=myfile, displayname=myfile.name)
    e.save()

    return HttpResponseRedirect(reverse('purchasemanager:purchase', args=(purchase.id,)))

	
	
# Delete attachment from purchase
@login_required(login_url='login/')
def delete_purchase_attachment(request, purchase_id, purchaseattachment_id):
	purchase = get_object_or_404(Purchase, pk=purchase_id)
	purchaseattachment = get_object_or_404(PurchaseAttachment, pk=purchaseattachment_id)
	try:
		purchaseattachment.delete()
		fs = FileSystemStorage()
		fs.delete(purchaseattachment)
	except:
		context = {
			'error_message' : "Unable to delete attachment!",
			'purchase_id' : purchase_id
		}
		return render(request, 'view_purchase.html', context)
	else:
		return HttpResponseRedirect(reverse('purchasemanager:purchase', args=(purchase.id,)))