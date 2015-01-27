from django.db import models

# Create your models here.


class Visit(models.Model):
	ip       = models.IPAddressField()
	time_start     = models.DateTimeField(auto_now_add=True, auto_now=False)
	time_end