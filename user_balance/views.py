from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user_balance.models import UserBalance
from user_balance.serializers import AddUserBalanceSerializer


class AdditionUserBalanceApi(APIView):
	permission_classes = [IsAuthenticated, ]

	def put(self, request):
		user_balance = UserBalance.objects.get(user=request.user)
		serializer = AddUserBalanceSerializer(instance=user_balance, data=request.data, many=False)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
