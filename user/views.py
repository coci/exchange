from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from permission.method_permission import method_permission_classes
from user.serializers import RegisterUserSerializer, UserDetailSerializer, UpdateUserSerializer


class UserApi(APIView):
	def post(self, request):
		serializer = RegisterUserSerializer(data=request.data)

		if serializer.is_valid():

			serializer.save()

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@method_permission_classes([IsAuthenticated])
	def get(self, request):
		serializer = UserDetailSerializer(instance=request.user)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@method_permission_classes([IsAuthenticated])
	def put(self, request):
		serializer = UpdateUserSerializer(instance=request.user, data=request.data, many=False, partial=True)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)