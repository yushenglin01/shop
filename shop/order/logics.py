import hashlib
import uuid

from cart.models import Cart
from common import errors
from .models import Order
from order_good.models import OrderGoods

# 加密使用
def my_sha256(str):
    # 创建sha256对象
    m = hashlib.sha256()
    # 更新这个对象
    m.update(str.encode('utf-8'))

    return m.hexdigest()



# 添加订单且加入购物车
def add_order(user):

    userid = user.id
    # 取到当前用户购物车中所有的商品
    carts = Cart.objects.filter(user_id=userid)
    if user.cart:
        order = Order()
        order.user_id = userid
        order.orderid = my_sha256(str(uuid.uuid4()))
        order.save()
        total = 0
        # 把每一个商品创建一个商品订单
        for cart in carts:
            # 创建一个商品订单
            ordergoods = OrderGoods()

            # 计算总价，把已选择商品计算总价
            if cart.is_select:
                ordergoods.order_id = order.id
                ordergoods.goods_id = cart.goods_id
                ordergoods.price = cart.goods.price
                ordergoods.num = cart.num
                ordergoods.save()
                total += ordergoods.num * ordergoods.price


        # 清空已选中结算的商品，未选中的不清除
        if total:
            carts = Cart.objects.filter(selected=True)
            carts.delete()
            order.total_price = total
            order.save()


        else:
            raise errors.NO_THIS_CART('no this cart')
    else:
        data['status'] = -2
        data['msg'] = '购物车为空不能提交'




# 订单
def order(request,oid):

    # 判断用户是否登录
    userid = request.session.get('userid')

    if not userid:
        return redirect(reverse('app:login'))
    else:
        # 根据订单id取出订单
        orders = Order.objects.filter(id=oid)

        if not orders:
            return HttpResponse('没有这个订单')
        order = orders.first()

        return render(request,'order/order.html',{'order':order})

# 订单操作
def order_handle(request):
    data = {
        'status': 1,
        'msg': 'order_unpay success',

    }
    # 判断用户是否登录
    userid = request.session.get('userid')

    if not userid:
        return redirect(reverse('app:login'))
    else:
        orderid = request.POST.get('orderid')
        orders = Order.objects.filter(user_id=userid,id=orderid)
        if not orders:
            data['status'] = -1
            data['msg'] = 'no this order'

        else:
            order = orders.first()

            order_string = alipay.api_alipay_trade_page_pay(
                out_trade_no=order.orderid,
                total_amount=str(order.total_price),
                subject="测试订单",
                return_url="http://10.3.139.178:8000/app/result/",
                notify_url=None  # 可选, 不填则使用默认notify url
            )
            # 将前面后的支付参数，拼接到支付网关
            # 注意：下面支付网关是沙箱环境，
            re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=order_string)
            print(re_url)
            data['re_url'] = re_url

    return JsonResponse(data)
alipay = AliPay(
                appid="2016092400584396",  # 设置签约的appid
                # app_notify_url="http://10.3.145.11/axf/notify/",  # 异步支付通知url
                app_private_key_string=open(r'app/alipay/ying_yong_si_yao.txt').read(),  # 设置应用私钥
                alipay_public_key_string=open(r"app/alipay/zhi_fu_bao_gong_yao.txt").read(),  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
                sign_type="RSA", # RSA 或者 RSA2
                debug=True,  # 默认False,                                   # 设置是否是沙箱环境，True是沙箱环境
                # app_notify_url="http://10.3.139.63:8000/app/result/"  # 同步支付通知url
                app_notify_url=None  # 同步支付通知url
            )

# 异步支付通知url (上线后使用)
# def notify(request):
#     # print("notify:", dict(request.GET))
#     app_id = request.GET.get('app_id')
#     print(app_id)
#     return HttpResponse("支付成功:%s" % (dict(request.GET)))

# 付款成功后跳转的url
def result(request):

    print("result:", dict(request.GET))
    print('***************************************')
    data = request.GET.dict()

    # print(type(data))
    # print(data)
    #
    signature = data.pop("sign")
    # print(signature)
    success = alipay.verify(data, signature)
    if success:
        orderid = request.GET.get("out_trade_no")
        orders = Order.objects.filter(orderid=orderid)
        orders.update(status=PAYED_UNRECEIVE)

        return HttpResponse("支付成功:%s" % (dict(request.GET)))
    return HttpResponse("支付失败")

# 更改状态
def change_status(request):
    data = {
        'status': 1,
        'msg': 'change status success',

    }
    # 判断用户是否登录
    userid = request.session.get('userid')

    if not userid:
        data['status'] = 0
        data['msg'] = 'no login'
    else:
        if request.method == 'POST':

            orderid = request.POST.get('orderid')
            status = request.POST.get('status')
            print('*****')
            print(status)
            # 查找当前用户的订单
            orders = Order.objects.filter(user_id=userid,id=orderid)
            if not orders:
                data['status'] = -1
                data['msg'] = 'no this order'

            else:
                # 更新订单状态
                orders.update(status=status)


        else:
            data['status'] = -2
            data['msg'] = 'request error'

    return JsonResponse(data)

# 待收货
def order_unreceive(request):
    '''

    :param request:http request
    :return:
    '''
    # 判断用户是否登录
    userid = request.session.get('userid')

    if not userid:
        return redirect(reverse('app:login'))
    else:
        orders = Order.objects.filter(user_id=userid,status=PAYED_UNRECEIVE)


    return render(request,'order/order_unreceive.html' ,{'orders':orders})


# 待评价
def order_unappraise(request):
    # 判断用户是否登录
    userid = request.session.get('userid')

    if not userid:
        return redirect(reverse('app:login'))
    else:
        orders = Order.objects.filter(user_id=userid, status=RECEIVE_UNCOMMENT)

    return render(request, 'appraise/appraise.html', {'orders':orders})

# 待付款
def order_unpay(request):
    # 判断用户是否登录
    userid = request.session.get('userid')

    if not userid:
        return redirect(reverse('app:login'))
    else:
        orders = Order.objects.filter(user_id=userid, status=UNPAY)

    return render(request, 'pay/order_unpay.html', {'orders':orders})

# 售后/评价
def order_returns(request):
    # 判断用户是否登录
    userid = request.session.get('userid')

    if not userid:
        return redirect(reverse('app:login'))
    else:
        orders = Order.objects.filter(user_id=userid, status=RETURNS)

    return render(request, 'returns/returns.html', {'orders':orders})


# 我的订单
def all_order(request):
    # 判断用户是否登录
    userid = request.session.get('userid')
    orderid = request.POST.get('orderid')
    if not userid:
        return redirect(reverse('app:login'))
    else:
        orders = Order.objects.filter(user_id=userid)
    return render(request, 'all_order/all_order.html', {'orders': orders})


# 成功支付页面（调试）
def success_pay(request):
    return render(request,'success_pay/success_pay.html')