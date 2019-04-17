from django.db import models

# 导入用户信息
# Create your models here.


# 商品订单（单个）
from goods.models import Goods


class OrderGoods(models.Model):

    goods_id = models.IntegerField(verbose_name='商品id')
    order_id = models.IntegerField(verbose_name='订单id')
    num = models.IntegerField(verbose_name='商品数量')
    price = models.FloatField(verbose_name='订单价格')

    @property
    def goods(self):
        if not hasattr(self, '_goods'):
            self._goods = Goods.objects.filter(id=self.goods_id)

        return self._goods
