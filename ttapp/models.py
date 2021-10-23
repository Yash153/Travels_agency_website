from django.db import models
from django.contrib.auth.models import User
import uuid

class ProfileModel(models.Model):
    phone_num = models.CharField(max_length = 15)
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

# class BookModel(models.Model):
#     user = models.ForeignKey(User, on_delete = models.PROTECT)
#     package = models.CharField(max_length = 50)
#     boarding_point = models.CharField(max_length = 50)
#     number_of_passengers = models.IntegerField()
#     date_booked = models.DateField()

#     def __str__(self):
#         return str(self.date_booked)

class BookModel_MumbaiDarshan(models.Model):
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    package = models.CharField(max_length = 50)
    boarding_point = models.CharField(max_length = 50)
    number_of_passengers = models.IntegerField()
    date_booked = models.DateField()
    dt = models.DateTimeField(auto_now_add = True,null=True)
    amount = models.FloatField()
    seats_available = models.IntegerField(default = 52)
    payment_mode = models.CharField(max_length = 10)
    payment_status_choices = (
        (0, 'CANCELED'),
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.date_booked)

class BookModel_Shirdi(models.Model):
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    package = models.CharField(max_length = 50)
    boarding_point = models.CharField(max_length = 50)
    number_of_passengers = models.IntegerField()
    date_booked = models.DateField()
    dt = models.DateTimeField(auto_now_add = True,null=True)
    amount = models.FloatField()
    seats_available = models.IntegerField(default = 52)
    payment_mode = models.CharField(max_length = 10)
    payment_status_choices = (
        (0, 'CANCELED'),
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.date_booked)

class BookModel_AshtavinayakDarshan(models.Model):
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    package = models.CharField(max_length = 50)
    boarding_point = models.CharField(max_length = 50)
    number_of_passengers = models.IntegerField()
    date_booked = models.DateField()
    dt = models.DateTimeField(auto_now_add = True,null=True)
    amount = models.FloatField()
    seats_available = models.IntegerField(default = 17)
    payment_mode = models.CharField(max_length = 10)
    payment_status_choices = (
        (0, 'CANCELED'),
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.date_booked)

class OrderModel_52seater(models.Model):
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    source = models.CharField(max_length = 500)
    destination = models.CharField(max_length = 500, blank = True, null = True)
    date_booked = models.DateField()
    date_released = models.DateField(blank = True, null = True)
    dt = models.DateTimeField(auto_now_add = True,null=True)
    amount = models.FloatField()
    payment_mode = models.CharField(max_length = 10)
    total_days_bus_reserved = models.IntegerField()
    no_days_to_be_disabled = models.IntegerField()
    payment_status_choices = (
        (0, 'CANCELED'),
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    

    def __str__(self):
            return self.user.username + ' ' + str(self.unique_id)

class DateBetweenModel_52seater(models.Model):
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date_between = models.DateField()


class OrderModel_17seater(models.Model):
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    source = models.CharField(max_length = 50)
    destination = models.CharField(max_length = 50, blank = True, null = True)
    date_booked = models.DateField()
    date_released = models.DateField(blank = True, null = True)
    dt = models.DateTimeField(auto_now_add = True,null=True)
    amount = models.FloatField()
    payment_mode = models.CharField(max_length = 10)
    total_days_bus_reserved = models.IntegerField()
    no_days_to_be_disabled = models.IntegerField()
    payment_status_choices = (
        (0, 'CANCELED'),
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
            return self.user.username + ' ' + str(self.unique_id)

class DateBetweenModel_17seater(models.Model):
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date_between = models.DateField()

class CancelModel_Charter(models.Model):
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    source = models.CharField(max_length = 50)
    destination = models.CharField(max_length = 50, blank = True, null = True)
    date_booked = models.DateField()
    date_released = models.DateField(blank = True, null = True)
    dt = models.DateTimeField(auto_now_add = True,null=True)
    date_time_booked = models.DateTimeField()
    amount = models.FloatField()
    payment_mode = models.CharField(max_length = 10)
    total_days_bus_reserved = models.IntegerField()
    no_days_to_be_disabled = models.IntegerField()
    payment_status_choices = (
        (0, 'CANCELED'),
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    refund_status_choices = (
        (1, 'SUCCESS'),
        (2, 'PENDING' ),
    )
    refund_status = models.IntegerField(choices = refund_status_choices, default=2)
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

class CancelModel_Packages(models.Model):
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    package = models.CharField(max_length = 50)
    boarding_point = models.CharField(max_length = 50)
    number_of_passengers = models.IntegerField()
    date_booked = models.DateField()
    dt = models.DateTimeField(auto_now_add = True,null=True)
    date_time_booked = models.DateTimeField()
    amount = models.FloatField()
    seats_available = models.IntegerField(default = 52)
    payment_mode = models.CharField(max_length = 10)
    payment_status_choices = (
        (0, 'CANCELED'),
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    refund_status_choices = (
        (1, 'SUCCESS'),
        (2, 'PENDING' ),
    )
    refund_status = models.IntegerField(choices = refund_status_choices, default=2)
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)