from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static


from . import views

app_name = 'purchasemanager'

patterns = [

	# # # DEFAULT

	url(r'^$', views.purchases.index, name='index'),

    # # # PURCHASES

    url(r'^purchase/new/$', views.purchases.new_purchase, name='new_purchase'),
    url(r'^purchase/all/$', views.purchases.all_purchases, name='all_purchases'),
    url(r'^purchase/draft/$', views.purchases.draft_purchases, name='draft_purchases'),
    url(r'^purchase/paid/$', views.purchases.paid_purchases, name='paid_purchases'),
    url(r'^purchase/unpaid/$', views.purchases.unpaid_purchases, name='unpaid_purchases'),
    url(r'^purchase/(?P<purchase_id>[0-9]+)/$', views.purchases.purchase, name='purchase'),
    url(r'^purchase/search/$', views.purchases.search_purchase, name='search_purchase'),
    url(r'^purchase/(?P<purchase_id>[0-9]+)/update/$', views.purchases.update_purchase, name='update_purchase'),
    url(r'^purchase/(?P<purchase_id>[0-9]+)/print/$', views.purchases.print_purchase, name='print_purchase'),
    url(r'^purchase/(?P<purchase_id>[0-9]+)/delete/$', views.purchases.delete_purchase, name='delete_purchase'),

    # # # ITEMS

    url(r'^purchase/(?P<purchase_id>[0-9]+)/item/add/$', views.items.add_item, name='add_item'),
    url(r'^purchase/(?P<purchase_id>[0-9]+)/item/(?P<purchaseitem_id>[0-9]+)/delete/$', views.items.delete_item, name='delete_item'),

    # # # PURCHASE EXPENSES

    url(r'^purchase/(?P<purchase_id>[0-9]+)/expenses/add/$', views.expenses.add_purchase_expense, name='add_purchase_expense'),
    url(r'^purchase/(?P<purchase_id>[0-9]+)/expenses/(?P<expense_id>[0-9]+)/delete/$', views.expenses.delete_purchase_expense, name='delete_purchase_expense'),

    # # # BUSINESS EXPENSES

    url(r'^expenses/$', views.expenses.expense_list, name='expense_list'),
    url(r'^expenses/new/$', views.expenses.new_business_expense, name='new_business_expense'),
    url(r'^expenses/(?P<expense_id>[0-9]+)/delete/$', views.expenses.delete_business_expense, name='delete_business_expense'),

    # # # REPORTS

    url(r'^accounting/$', views.reports.accounting, name='accounting'),

    # # # ATTACHMENTS

    url(r'^purchase/(?P<purchase_id>[0-9]+)/attachments/add/$', views.purchases.upload_purchase_attachment, name='upload_purchase_attachment'),
    url(r'^purchase/(?P<purchase_id>[0-9]+)/attachments/(?P<purchaseattachment_id>[0-9]+)/delete/$', views.purchases.delete_purchase_attachment, name='delete_purchase_attachment'),
    url(r'^expenses/(?P<expense_id>[0-9]+)/attachments/add/$', views.expenses.upload_business_expense_attachment, name='upload_business_expense_attachment'),

    # # # vendorS

    url(r'^vendors/$', views.vendors.vendor_list, name='vendor_list'),
    url(r'^vendor/(?P<vendor_id>[0-9]+)/$', views.vendors.vendor, name='vendor'),
	url(r'^vendor/(?P<vendor_id>[0-9]+)/update/$', views.vendors.update_vendor, name='update_vendor'),
    url(r'^vendor/(?P<vendor_id>[0-9]+)/delete/$', views.vendors.delete_vendor, name='delete_vendor'),
    url(r'^vendor/new/$', views.vendors.new_vendor, name='new_vendor'),


    # # # PRODUCTS

    url(r'^products/$', views.products.product_list, name='product_list'),
    url(r'^product/(?P<product_id>[0-9]+)/$', views.products.product, name='product'),
    url(r'^product/(?P<product_id>[0-9]+)/update/$', views.products.update_product, name='update_product'),
    url(r'^product/(?P<product_id>[0-9]+)/delete/$', views.products.delete_product, name='delete_product'),
    url(r'^product/new/$', views.products.new_product, name='new_product'),
    url(r'^ajax_calls/search/', views.products.autocompleteModel),


    # # # USER AUTHENTICATION

    url(r'^login/$', views.userauth.login_view, name='login'),
    url(r'^logout/$', views.userauth.logout_view, name='logout'),

    # # # ADMIN
	#url(r'^admin/$', admin.site.urls),
    url(r'^users/$', views.admin.users, name='users'),
    url(r'^settings/$', views.admin.settings, name='settings'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    url(r'^', include(patterns, namespace="purchasemanager")),
]
