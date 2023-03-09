from rest_framework import serializers
from .models import CreditCard, Holder


class HolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holder
        fields = '__all__'


class CreditCardSerializer(serializers.ModelSerializer):
    holder = serializers.PrimaryKeyRelatedField(queryset=Holder.objects.all())

    class Meta:
        model = CreditCard
        fields = ['id', 'exp_date', 'holder', 'number', 'cvv', 'brand']

    def to_representation(self, instance):
        """
        Serializes the CreditCard object with Holder name instead of ID for GET requests
        """
        representation = super().to_representation(instance)
        representation['holder'] = {'id': representation['holder'],
                                    'name': instance.holder.name}
        return representation


class CreditCardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['exp_date', 'holder', 'number', 'cvv', 'brand']