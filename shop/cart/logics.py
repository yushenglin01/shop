from common import errors
from .models import Cart
from django.core.cache import cache


# 创建购物车
def Create_cart(user_id, goods_id, num):
    carts = Cart.objects.filter(user_id=user_id, goods_id=goods_id)

    if carts:
        # 如果有记录
        cart = carts.first()
        cart.num += int(num)
        cart.save()
    else:
        # 创建新的购物车记录
        cart = Cart()
        cart.user_id = user_id
        cart.goods_id = goods_id
        cart.num = int(num)
        cart.save()

    return cart




def cart_num_add(cartid):

    carts = Cart.objects.filter(id=cartid)
    # 如果没有这条购物车的记录
    if not carts:
        raise errors.NO_THIS_CART
    else:
        # 如果有记录，就把数量加1
        cart = carts.first()
        cart.num += 1
        cart.save()



# 商品数量减1
def cart_num_sub(cartid):

    carts = Cart.objects.filter(id=cartid)
    # 如果没有这条购物车的记录
    if not carts:
       raise errors.NO_THIS_CART.code
    else:
        # 如果有记录，就把数量加1
        cart = carts.first()
        if cart.num > 1:
            cart.num -= 1
            cart.save()

        else:
           # 抛出异常，购物车没有足够数量可以减少
            raise errors.NUM_ERROR('num is min')




# 购物车的删除
def cart_del(cartid):



    cart = Cart.objects.filter(id=cartid)
    # 如果没有这条购物车的记录
    if not cart:
        raise errors.NO_THIS_CART.code
    else:
        # 删除购物车记录
        cart.delete()
        cache.delete('Model-%s-%s'%(cart, cartid))
        return True


# 购物车选择或不选
def cart_select(cartid):

    carts = Cart.objects.filter(id=cartid)
    # 如果没有这条购物车的记录
    if not carts:
        raise errors.NO_THIS_CART.code
    else:
        cart = carts.first()
        # 勾选状态取反
        cart.selected = not cart.selected
        cart.save()
        return True



# 购物车全选或不选
def all_select_or_none(user,selected):

    userid = user.id
    # 取到前段提交的选择状态，0：把商品全部都不选，1：表示把商品全部都选

    # 如果要全部勾选
    if int(selected):
        cart = Cart.objects.filter(user_id=userid,is_select=False).update(is_select=True)
    else:
        cart = Cart.objects.filter(user_id=userid, is_select=True).update(is_select=False)
    cart.save()

