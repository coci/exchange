from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "first_name", "last_name", "username"]


class RegisterUserSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(read_only=True)
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError(
				{
					"password": "Passwords not match."
				}
			)
		return attrs

	def create(self, validated_data):
		user = User.objects.create(
			username=validated_data['username'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name']
		)
		user.set_password(validated_data['password'])
		user.save()
		return user

	class Meta:
		model = User
		fields = ["id", "first_name", "last_name", "username", "password", "password2"]


class UpdateUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["first_name", "last_name"]
