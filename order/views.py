from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .env import COIN_PRICE, ORDER_LIMIT
from order.exchange import ExchangeHandler
from order.models import OrderStatus
from order.order import PendingOrderHandler, RedisHandler
from order.payment import PaymentHandler
from order.serializers import OrderInputSerializer, OrderSerializer


class MakeOrderAPI(APIView):
	permission_classes = [IsAuthenticated, ]

	def post(self, request):
		serializer = OrderInputSerializer(data=request.data)

		if serializer.is_valid():
			coin = serializer.validated_data['coin']
			# i assume coin amount is Integer but i know in real production this will be Decimal
			amount = serializer.validated_data['amount']

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		payment = PaymentHandler(user=request.user, coin=coin, amount=amount, coin_price=COIN_PRICE, order_limit=ORDER_LIMIT)

		if not payment.is_user_have_balance():
			response = {
				"status": "error",
				"message": "you don't have credit."
			}
			return Response(response, status=status.HTTP_400_BAD_REQUEST)

		# minus user balance
		payment.decrease_user_balance()

		if payment.is_total_price_allowed():
			# i assume call buy_from_exchange always is success,
			# so i didn't check if buying from exchange is success to update order in db

			ExchangeHandler.buy_from_exchange(coin=coin, amount=amount)

			order = payment.create_database_record(status=OrderStatus.success)

		else:
			order = payment.create_database_record(status=OrderStatus.pending)

			pending_order = PendingOrderHandler(coin=coin, amount=amount, coin_price=COIN_PRICE, order_id=order.id,
			                                    cache=RedisHandler)
			pending_order.set_pending_order()

		serializer = OrderSerializer(instance=order, many=False)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
