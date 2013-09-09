from django.core.mail import send_mail
from django.db import models
from django.db.models import F
from home.models import Item
import json

# Create your models here.
class Order(models.Model):
    def __unicode__(self):
        return self.invoice
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    postcode = models.CharField(max_length=10)
    items = models.CharField(max_length=1000)
    price = models.FloatField()
    tax = models.FloatField()
    shipping = models.FloatField()
    status = models.CharField(max_length=20)
    delivery_window = models.CharField(max_length=20)
    time = models.DateTimeField()
    invoice = models.CharField(max_length=30)


from paypal.standard.ipn.signals import payment_was_successful
from paypal.standard.ipn.signals import payment_was_flagged
from threading import Thread

def send_receipt(to, subject, message):
  Thread(target=lambda: send_mail(subject, message, 'noreply@fruitex.com',
      [to], fail_silently=False)).start()

def handle_payment_received(status, ipn):
  invoice = ipn.invoice
  order = Order.objects.filter(invoice=invoice)[0]
  order.status=status
  order.save()
  ids = json.loads(order.items)
  for it in Item.objects.filter(id__in=set(ids)):
    it.sold_number=it.sold_number + ids.count(it.id)
    it.save()
  send_receipt(ipn.payer_email,\
     '[Fruitex] Payment of your order %s received.' % invoice,\
     "You can track your order at http://fruitex.ca/check_order/?invoice=%s" % invoice)


def payment_successful(sender, **kwargs):
  handle_payment_received('paid', sender)

def payment_flagged(sender, **kwargs):
  handle_payment_received('flagged', sender)

payment_was_successful.connect(payment_successful)
payment_was_flagged.connect(payment_flagged)
