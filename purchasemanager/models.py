from __future__ import unicode_literals

from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.
class Vendor(models.Model):
	name = models.CharField(max_length=256)
	address1 = models.CharField(max_length=256, blank=True)
	address2 = models.CharField(max_length=256, blank=True)
	atoll = models.CharField(max_length=256, blank=True)
	island = models.CharField(max_length=256, blank=True)
	email = models.CharField(max_length=256, blank=True)

	def __str__(self):
		return self.name

	def purchases(self):
		return Purchase.objects.filter(vendor=self).count()

class Product(models.Model):
	code = models.CharField(max_length=256)
	name = models.CharField(max_length=256)
	description = models.CharField(max_length=256, blank=True)
	unit = models.CharField(max_length=256, blank=True)

	def __str__(self):
		return self.code

class Purchase(models.Model):
	vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
	date = models.DateField()
	status = models.CharField(max_length=10)

	def __str__(self):
	    return str(self.id)

	def total_items(self):
		total = 0
		items = self.purchaseitem_set.all()

		for item in items:
			total += item.cost * item.qty

		return total

	def total_expenses(self):
		total = 0
		expenses = self.expense_set.all()

		for expense in expenses:
			total += expense.cost * expense.qty

		return total

	def total(self):
		items = self.total_items()
		expenses = self.total_expenses()

		return items - expenses

	def paid(self):
		return self.status == 'Paid'

	def unpaid(self):
		return self.status == 'Unpaid'

	def draft(self):
		return self.status == 'Draft'

class PurchaseItem(models.Model):
	purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
	name = models.CharField(max_length=128)
	description = models.TextField()
	cost = models.DecimalField(decimal_places=2, max_digits=10)
	qty = models.IntegerField()

	def total(self):
		return self.cost * self.qty

class Expense(models.Model):
	description = models.TextField()
	cost = models.DecimalField(decimal_places=2, max_digits=10)
	qty = models.IntegerField()
	purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, blank=True, null=True)
	date = models.DateField(blank=True, null=True)

	def total(self):
		return self.cost * self.qty

	def is_business_expense(self):
		return self.purchase is None

class PurchaseAttachment(models.Model):
	file = models.FileField(upload_to='purchase/')
	displayname = models.CharField(max_length=128)
	purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)

class ExpenseAttachment(models.Model):
	file = models.FileField(upload_to='expense/')
	displayname = models.CharField(max_length=128)
	expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
