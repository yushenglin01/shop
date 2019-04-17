from django.db import models
from goods.models import Goods

# Create your models here.

# 购物车
class Cart(models.Model):
    user_id = models.IntegerField(verbose_name='用户id')
    goods_id = models.IntegerField(verbose_name='商品id')
    num = models.IntegerField(default=1, verbose_name='商品数量')
    selected = models.BooleanField(default=True, verbose_name='是否选择')


    # 获取购物车对应的商品
    @property
    def goods(self):
        if not hasattr(self, '_goods'):
            self._goods = Goods.objects.filter(id=self.goods_id)

        return self._goods



