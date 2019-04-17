from django.db import models

# Create your models here.


# 订单
class Order(models.Model):
    orderid = models.CharField(max_length=64, verbose_name='订单id')
    userid = models.IntegerField(verbose_name='用户id')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='订单日期')
    total_price = models.FloatField(default=0, verbose_name='商品价格')
    # 标示商品状态 0:未付款 1：已付款，商家未发货 2:已付款，商家发货 3：已收货，待评价 4：已评价
    status = models.IntegerField(default=0, verbose_name='商品状态')


