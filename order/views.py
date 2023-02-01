from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.env import COIN_PRICE, ORDER_LIMIT
from order.models import Order, OrderStatus
from order.operations import buy_from_exchange, set_pending_order
from order.serializers import OrderInputSerializer, OrderSerializer
from user_balance.models import UserBalance


class Payment(APIView):
	permission_classes = [IsAuthenticated, ]

	@transaction.atomic
	def post(self, request):
		serializer = OrderInputSerializer(data=request.data)

		if serializer.is_valid():
			coin = serializer.validated_data['coin']
			# i assume coin amount is Integer but i know in real production this will be Decimal
			amount = serializer.validated_data['amount']

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		user_balance = UserBalance.objects.get(user=request.user)

		total_price = amount * COIN_PRICE

		if user_balance.balance <= total_price:
			response = {
				"status": "error",
				"message": "you don't have credit."
			}
			return Response(response, status=status.HTTP_400_BAD_REQUEST)

		# minus user balance
		user_balance.balance -= total_price
		user_balance.save()

		if total_price >= ORDER_LIMIT:

			# i assume call buy_from_exchange always is success,
			# so i didn't check if buying from exchange is success to update order in db

			buy_from_exchange(coin=coin, amount=amount)

			order = Order.objects.create(
				user=request.user,
				coin=coin,
				coin_amount=amount,
				order_price=total_price,
				status=OrderStatus.success
			)

		else:
			order = Order.objects.create(
				user=request.user,
				coin=coin,
				coin_amount=amount,
				order_price=total_price,
				status=OrderStatus.pending
			)

			set_pending_order(order_id=order.pk, coin=coin, amount=amount)

		serializer = OrderSerializer(instance=order, many=False)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
