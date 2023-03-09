from rest_framework import serializers
from .models import CreditCard, Holder, User


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
        representation = super().to_representation(instance)
        representation['holder'] = {'id': representation['holder'],
                                    'name': instance.holder.name}
        return representation


class CreditCardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['exp_date', 'holder', 'number', 'cvv', 'brand']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
