from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CreditCard, Holder
from .serializers import (CreditCardCreateSerializer,
                          CreditCardSerializer,
                          HolderSerializer,
                          UserSerializer)
from django.core.exceptions import ObjectDoesNotExist
from .utils import (
    is_valid_date_format,
    get_last_day_of_month,
    is_date_valid, check_if_cc_is_valid,
    get_cc_brand, encrypt_cc_number)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CreditCardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

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
            paginator = CustomPagination()
            credit_cards = CreditCard.objects.all()
            result_page = paginator.paginate_queryset(credit_cards, request)
            serializer = CreditCardSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

    def delete(self, request, pk):
        try:
            credit_card = CreditCard.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'detail': 'Credit Card not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        credit_card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        data = request.data.copy()
        holder = data.get('holder')
        exp_date = data.get('exp_date')
        cc_number = data.get('number')

        if holder:
            try:
                holder_obj = Holder.objects.filter(name=holder).first().id
            except AttributeError:
                return Response({'error': 'Holder not found.'},
                                status=status.HTTP_404_NOT_FOUND)

            data['holder'] = holder_obj

        if exp_date:
            if not is_valid_date_format(exp_date):
                return Response({'error': 'Wrong date format, use MM/YYYY.'},
                                status=status.HTTP_400_BAD_REQUEST)

            elif not is_date_valid(get_last_day_of_month(exp_date)):
                return Response({'error': 'Date expired.'},
                                status=status.HTTP_400_BAD_REQUEST)

            data['exp_date'] = get_last_day_of_month(exp_date)

        if cc_number:
            if not check_if_cc_is_valid(cc_number):
                return Response({'error': 'Credit Card number is not valid.'},
                                status=status.HTTP_400_BAD_REQUEST)

            if not get_cc_brand(cc_number):
                return Response({'error': 'This CC has a invalid brand.'},
                                status=status.HTTP_400_BAD_REQUEST)

            data['brand'] = get_cc_brand(cc_number)
            data['number'] = encrypt_cc_number(cc_number)

        serializer = CreditCardCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(5)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HolderView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

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


class UserCreateView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'id': user.id,
                'name': user.name,
                'role': user.role,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)