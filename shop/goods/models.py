from django.db import models

# Create your models here.


class Goods(models.Model):
    productid = models.CharField(max_length=20)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=30)
    productlongname = models.CharField(max_length=50)

    isxf = models.BooleanField()
    pmdesc = models.BooleanField()
    specifics = models.CharField(max_length=20)
    price = models.FloatField()
    marketprice = models.FloatField()
    categoryid = models.IntegerField()

    childcid = models.IntegerField()
    childcidname = models.CharField(max_length=20)
    dealerid = models.CharField(max_length=20)
    storenums = models.IntegerField()
    productnum = models.IntegerField()

    class Meta:
        db_table = 'shop_goods'


