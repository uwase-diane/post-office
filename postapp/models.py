from django.db import models
from django.contrib.auth.models import User


class Office(models.Model):
    name = models.CharField(max_length=300)
    country = models.CharField(max_length=300)
    province = models.CharField(max_length=300)
    district = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Address(models.Model):
    name = models.CharField(max_length=300)
    country = models.CharField(max_length=300)
    province = models.CharField(max_length=300)
    district = models.CharField(max_length=300)
    street = models.CharField(max_length=300)
    house_number = models.CharField(max_length=300)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.house_number


class Parcel(models.Model):
    tracking_number = models.CharField(max_length=10)
    image = models.ImageField(upload_to="item_images", null=True)
    quantity = models.DecimalField(default=0, decimal_places=1, max_digits=10)
    dimension_height = models.DecimalField(max_digits=2, decimal_places=2, default=0, help_text="in mm")
    dimension_width = models.DecimalField(max_digits=2, decimal_places=2, default=0, help_text="in mm")
    dimension_length = models.DecimalField(max_digits=2, decimal_places=2, default=0, help_text="in mm")
    total_price = models.IntegerField(default=0)
    description = models.TextField()
    statuses = {
        ("Waiting", "Waiting"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
        ("Waiting pickup", "Waiting pickup"),
        ("Checking", "Checking"),
        ("On way", "On way"),
        ("Delivered", "Delivered")
    }

    options = {
        ("Express", "Express"),
        ("Regular", "Regular")
    }
    delivery_option = models.CharField(max_length=300, default="Regular", choices=options)
    status = models.CharField(max_length=300, default="Waiting pickup", choices=statuses)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    sender_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="sender_address")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    receiver_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="receiver_address", null=True, blank=True)
    picked_up_at_office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)
    picked_up_by = models.ForeignKey(User, related_name="picked_up_by", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.tracking_number + " " + self.status