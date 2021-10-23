# Generated by Django 3.2.6 on 2021-09-01 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_num', models.CharField(max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderModel_52seater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('source', models.CharField(max_length=500)),
                ('destination', models.CharField(blank=True, max_length=500, null=True)),
                ('date_booked', models.DateField()),
                ('date_released', models.DateField(blank=True, null=True)),
                ('dt', models.DateTimeField(auto_now_add=True, null=True)),
                ('amount', models.FloatField()),
                ('payment_mode', models.CharField(max_length=10)),
                ('total_days_bus_reserved', models.IntegerField()),
                ('no_days_to_be_disabled', models.IntegerField()),
                ('payment_status', models.IntegerField(choices=[(0, 'CANCELED'), (1, 'SUCCESS'), (2, 'FAILURE'), (3, 'PENDING')], default=3)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderModel_17seater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('source', models.CharField(max_length=50)),
                ('destination', models.CharField(blank=True, max_length=50, null=True)),
                ('date_booked', models.DateField()),
                ('date_released', models.DateField(blank=True, null=True)),
                ('dt', models.DateTimeField(auto_now_add=True, null=True)),
                ('amount', models.FloatField()),
                ('payment_mode', models.CharField(max_length=10)),
                ('total_days_bus_reserved', models.IntegerField()),
                ('no_days_to_be_disabled', models.IntegerField()),
                ('payment_status', models.IntegerField(choices=[(0, 'CANCELED'), (1, 'SUCCESS'), (2, 'FAILURE'), (3, 'PENDING')], default=3)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DateBetweenModel_52seater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_between', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DateBetweenModel_17seater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_between', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CancelModel_Packages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('package', models.CharField(max_length=50)),
                ('boarding_point', models.CharField(max_length=50)),
                ('number_of_passengers', models.IntegerField()),
                ('date_booked', models.DateField()),
                ('dt', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_time_booked', models.DateTimeField()),
                ('amount', models.FloatField()),
                ('seats_available', models.IntegerField(default=52)),
                ('payment_mode', models.CharField(max_length=10)),
                ('payment_status', models.IntegerField(choices=[(0, 'CANCELED'), (1, 'SUCCESS'), (2, 'FAILURE'), (3, 'PENDING')], default=3)),
                ('refund_status', models.IntegerField(choices=[(1, 'SUCCESS'), (2, 'PENDING')], default=2)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CancelModel_Charter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('source', models.CharField(max_length=50)),
                ('destination', models.CharField(blank=True, max_length=50, null=True)),
                ('date_booked', models.DateField()),
                ('date_released', models.DateField(blank=True, null=True)),
                ('dt', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_time_booked', models.DateTimeField()),
                ('amount', models.FloatField()),
                ('payment_mode', models.CharField(max_length=10)),
                ('total_days_bus_reserved', models.IntegerField()),
                ('no_days_to_be_disabled', models.IntegerField()),
                ('payment_status', models.IntegerField(choices=[(0, 'CANCELED'), (1, 'SUCCESS'), (2, 'FAILURE'), (3, 'PENDING')], default=3)),
                ('refund_status', models.IntegerField(choices=[(1, 'SUCCESS'), (2, 'PENDING')], default=2)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookModel_Shirdi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('package', models.CharField(max_length=50)),
                ('boarding_point', models.CharField(max_length=50)),
                ('number_of_passengers', models.IntegerField()),
                ('date_booked', models.DateField()),
                ('dt', models.DateTimeField(auto_now_add=True, null=True)),
                ('amount', models.FloatField()),
                ('seats_available', models.IntegerField(default=52)),
                ('payment_mode', models.CharField(max_length=10)),
                ('payment_status', models.IntegerField(choices=[(0, 'CANCELED'), (1, 'SUCCESS'), (2, 'FAILURE'), (3, 'PENDING')], default=3)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookModel_MumbaiDarshan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('package', models.CharField(max_length=50)),
                ('boarding_point', models.CharField(max_length=50)),
                ('number_of_passengers', models.IntegerField()),
                ('date_booked', models.DateField()),
                ('dt', models.DateTimeField(auto_now_add=True, null=True)),
                ('amount', models.FloatField()),
                ('seats_available', models.IntegerField(default=52)),
                ('payment_mode', models.CharField(max_length=10)),
                ('payment_status', models.IntegerField(choices=[(0, 'CANCELED'), (1, 'SUCCESS'), (2, 'FAILURE'), (3, 'PENDING')], default=3)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookModel_AshtavinayakDarshan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('package', models.CharField(max_length=50)),
                ('boarding_point', models.CharField(max_length=50)),
                ('number_of_passengers', models.IntegerField()),
                ('date_booked', models.DateField()),
                ('dt', models.DateTimeField(auto_now_add=True, null=True)),
                ('amount', models.FloatField()),
                ('seats_available', models.IntegerField(default=17)),
                ('payment_mode', models.CharField(max_length=10)),
                ('payment_status', models.IntegerField(choices=[(0, 'CANCELED'), (1, 'SUCCESS'), (2, 'FAILURE'), (3, 'PENDING')], default=3)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
