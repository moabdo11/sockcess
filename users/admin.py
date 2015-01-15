from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from .models import Sock, Subscriber, Order
from django.contrib.auth.models import User



class SockAdmin(admin.ModelAdmin):
    list_display = ['style', 'sub_style', 'cost_per_unit', 'created']

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'sock_genre', 'sock_style','__unicode__',
                    'created','updated']
    class Meta:
        model = Subscriber

class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'street', 'city', 'state', 'zipcode', 'sock_style']
    pass


admin.site.register(Sock, SockAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
