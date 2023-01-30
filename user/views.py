from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import RegisterUserSerializer, UserDetailSerializer, UpdateUserSerializer


class UserApi(APIView):
	def post(self, request):
		serializer = RegisterUserSerializer(data=request.data)

		if serializer.is_valid():

			serializer.save()

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request):
		serializer = UserDetailSerializer(instance=request.user)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def put(self, request):
		serializer = UpdateUserSerializer(instance=request.user, data=request.data, many=False, partial=True)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
