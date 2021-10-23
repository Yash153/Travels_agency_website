from django.contrib import admin
from .models import ProfileModel, OrderModel_52seater, OrderModel_17seater, BookModel_MumbaiDarshan, BookModel_Shirdi, BookModel_AshtavinayakDarshan, CancelModel_Packages, CancelModel_Charter

admin.site.register(ProfileModel)
admin.site.register(OrderModel_52seater)
admin.site.register(OrderModel_17seater)
admin.site.register(BookModel_MumbaiDarshan)
admin.site.register(BookModel_Shirdi)
admin.site.register(BookModel_AshtavinayakDarshan)
admin.site.register(CancelModel_Charter)
admin.site.register(CancelModel_Packages)