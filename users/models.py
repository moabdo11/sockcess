from django.db import models
#from django.contrib.localflavor.us.us_states import STATE_CHOICES
#from django.contrib.localflavor.us.forms import USStateField
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode




class Sock(models.Model):

    STYLE_CHOICE = (
        ('business', 'business'),
        ('pleasure', 'pleasure'),
    )
    style = models.CharField(max_length=9,
                             choices=STYLE_CHOICE)
    sub_style = models.CharField(max_length=35)
    supplier = models.CharField(max_length=35)
    cost_per_unit = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    sale_price = models.DecimalField(max_digits=4, decimal_places=2, default=9.99)
    shipping_cost_from_china_per_unit = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    shipping_cost_to_customer_per_unit = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    picture = models.ImageField(upload_to='static/img/socks')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __unicode__(self):
        return "%s, %s" %(self.style, self.sub_style)


class Subscriber(models.Model):

    customer = models.ForeignKey(User)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=7)
    sock_genre = models.CharField(max_length=10)
    sock_style = models.CharField(max_length=25)
    stripe_id = models.TextField()
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __unicode__(self):
        return "%s" %(self.customer.email)


class Order(models.Model):
    customer = models.ForeignKey(User)
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    street = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zipcode = models.CharField(max_length=7)
    sock_style = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return smart_unicode(self.email)