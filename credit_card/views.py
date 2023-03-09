from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CreditCard, Holder
from .serializers import CreditCardCreateSerializer, CreditCardSerializer, HolderSerializer
from django.core.exceptions import ObjectDoesNotExist
from .utils import is_valid_date_format, get_last_day_of_month, is_date_valid


class CreditCardView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                credit_card = CreditCard.objects.get(pk=pk)
            except ObjectDoesNotExist:
                return Response({'error': 'Credit Card not found.'},
                                status=status.HTTP_404_NOT_FOUND)

            serializer = CreditCardSerializer(credit_card)
            return Response(serializer.data)
        else:
            credit_cards = CreditCard.objects.all()
            serializer = CreditCardSerializer(credit_cards, many=True)
            return Response(serializer.data)

    def put(self, request, pk):
        try:
            credit_card = CreditCard.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'detail': 'Credit Card not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = CreditCardCreateSerializer(credit_card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            credit_card = CreditCard.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'detail': 'Credit Card not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        credit_card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        holder = request.data.get('holder')
        exp_date = request.data.get('exp_date')

        if holder:
            try:
                holder_obj = Holder.objects.filter(name=holder).first().id
            except AttributeError:
                return Response({'error': 'Holder not found.'},
                                status=status.HTTP_404_NOT_FOUND)

            request.data['holder'] = holder_obj

        if exp_date:
            if not is_valid_date_format(exp_date):
                return Response({'error': 'Wrong date format, use MM/YYYY instead.'},
                                status=status.HTTP_400_BAD_REQUEST)

            elif not is_date_valid(get_last_day_of_month(exp_date)):
                return Response({'error': 'Date expired.'},
                                status=status.HTTP_400_BAD_REQUEST)

            request.data['exp_date'] = get_last_day_of_month(exp_date)

        serializer = CreditCardCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HolderView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                holder = Holder.objects.get(pk=pk)
            except ObjectDoesNotExist:
                return Response({'error': 'Holder not found.'},
                                status=status.HTTP_404_NOT_FOUND)

            serializer = HolderSerializer(holder)
        else:
            holders = Holder.objects.all()
            serializer = HolderSerializer(holders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HolderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            holder = Holder.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'Holder not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = HolderSerializer(holder, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            holder = Holder.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'Holder not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        holder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
