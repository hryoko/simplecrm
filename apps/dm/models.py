from django.db import models
from django.core.validators import RegexValidator

class Customer(models.Model):
    name = models.CharField(max_length=100)
    name_kana = models.CharField(max_length=100, blank=True)
    tel_number_regex = RegexValidator(regex=r'^[0-9]+$', message = ("Tel Number must be entered in the format: '09012345678'. Up to 15 digits allowed."))
	tel_number = models.CharField(validators=[tel_number_regex], max_length=15, verbose_name='電話番号')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

class BottleKeep(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bottles')
    bottle_name = models.CharField(max_length=100)
    keep_date = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bottle_name} - {self.customer.name}"

class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateTimeField()
    people_count = models.PositiveIntegerField(default=1)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reservation_date} - {self.customer.name}"

class DMHistory(models.Model):
    METHOD_CHOICES = [
        ('LINE', 'LINE'),
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='dm_histories')
    title = models.CharField(max_length=200)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)

    def __str__(self):
        return f"{self.title} ({self.method}) - {self.customer.name}"
