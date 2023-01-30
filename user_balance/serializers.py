from rest_framework import serializers
from .models import UserBalance


class AddUserBalanceSerializer(serializers.ModelSerializer):
	balance = serializers.IntegerField(required=True)
	user = serializers.PrimaryKeyRelatedField(read_only=True)

	def validate(self, attrs):
		if attrs['balance'] < 0:
			raise serializers.ValidationError(
				{
					"balance": "Must be positive or zero."
				}
			)
		return attrs

	class Meta:
		model = UserBalance
		fields = ["balance","user"]
