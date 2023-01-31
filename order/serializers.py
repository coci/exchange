from rest_framework import serializers

from order.models import Order


class OrderInputSerializer(serializers.Serializer):
	coin = serializers.CharField(required=True)
	amount = serializers.IntegerField(required=True)

	def validate(self, attrs):
		if attrs['amount'] <= 0:
			raise serializers.ValidationError(
				{
					"amount": "Must be positive and greater than zero."
				}
			)
		return attrs


class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = "__all__"
