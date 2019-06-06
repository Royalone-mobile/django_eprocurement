from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime
from ajax_select.fields import AutoCompleteSelectMultipleField
import json

from purchasemanager.models import Vendor, Product, Purchase, PurchaseItem, Expense, PurchaseAttachment, ExpenseAttachment



# List all products
@login_required(login_url='login/')
def product_list(request):
	products = Product.objects.all()
	context = {
		'title' : 'Product List',
		'products' : products,
	}
	return render(request, 'products.html', context)
	
	
	
# Show specific product details
@login_required(login_url='login/')
def product(request, product_id):
	product = get_object_or_404(Product, pk=product_id)
	context = {
		'title' : "Product info - %s" % product.name,
		'product' : product,
	}
	return render(request, 'product.html', context)

# Show specific product details
@login_required(login_url='login/')
def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Product.objects.filter(code__startswith=q)
        results = []
        print q
        for r in search_qs:
            results.append(r.code)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)	
	
# Add new product
@login_required(login_url='login/')
def new_product(request):
	if request.method == 'POST':
		# Stuff from form
		c = Product(code=request.POST['code'], name=request.POST['name'], description=request.POST['description'], unit=request.POST['unit'])
		c.save()
		return HttpResponseRedirect(reverse('purchasemanager:product_list'))
	else:
		return render(request, 'new_product.html')



# Update product
@login_required(login_url='login/')
def update_product(request, product_id):
	# Stuff from form
	c = get_object_or_404(Product, pk=product_id)
	
	c.code = request.POST['code']
	c.name = request.POST['name']
	c.description = request.POST['description']
	c.unit = request.POST['unit']

	
	c.save()
	
	return HttpResponseRedirect(reverse('purchasemanager:product', args=(c.id,)))

		
# Delete product
@login_required(login_url='login/')
def delete_product(request, product_id):
	product = get_object_or_404(Product, pk=product_id)
	product.delete()
	return HttpResponseRedirect(reverse('purchasemanager:product_list'))