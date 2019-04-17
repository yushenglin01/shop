
from lib.http import render_json
from .logics import *
from django.core.cache import cache
from common import errors

# 加入购物车
def create_cart(request):
    if not request.method == 'POST':
        return render_json('request method error', errors.REQUEST_ERROR.code)
    gid = request.POST.get('gid')
    num = request.POST.get('num')
    uid = request.user.id
    cart = Create_cart(uid, gid, num)
    return render_json(cart.to_string())


# 增减购物车
def update_cart(request):
    if not request.method == 'POST':
        return render_json('request method error', errors.REQUEST_ERROR.code)
    '''
     "event":"add", //可以是 minus(减)  update(开通会员,使用优惠券等)
    "goodId":1,
    "isOpendClub":0,   //是否打开会员
    "coupon":"",   //是否使用优惠券,优惠券ID
    "totalPrice": 123.3 //商品总价
    '''
    event = request.POST.get('event')
    cart = cache.get('cart')
    cartid = cart.id
    if event == 'add':
        cart_num_add(cartid)
    else:
        cart_num_sub(cartid)
    cart = cache.get(cartid)
    return render_json(cart)


# 购物车选择或不选
def cart_selected(request):

    user = request.user
    cartid = user.cart.id
    cart_select(cartid)
    cart = cache.get('cartid')
    return render_json(cart)

# 购物车全选
def seleced_all(request):
    user = request.user
    cartid = request.user.cart.id
    selected = request.POST.get('selected')
    all_select_or_none(user, selected)
    cart = cache.get(cartid)

    return render_json(cart.to_string())