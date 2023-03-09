from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from credit_card.serializers import (
    CreditCardCreateSerializer,
    CreditCardSerializer,
    HolderSerializer,
    UserSerializer,
)
from credit_card.models import Holder, CreditCard, User, UserRole


class ModelSerializerTestCase(TestCase):
    def setUp(self):
        self.holder = Holder.objects.create(name='John Doe')
        self.credit_card = CreditCard.objects.create(
            exp_date='2025-12-31',
            number='4111111111111111',
            cvv='123',
            holder=self.holder,
            brand='Visa'
        )
        self.user = User.objects.create_user(
            name='testuser',
            password='testpassword',
            role=UserRole.ADMIN,
        )

    def test_holder_creation(self):
        holder = Holder.objects.create(name='Jane Doe')
        self.assertIsInstance(holder, Holder)
        self.assertEqual(holder.name, 'Jane Doe')

    def test_credit_card_creation(self):
        credit_card = CreditCard.objects.create(
            exp_date=date.today(),
            number='5555555555554444',
            cvv='123',
            holder=self.holder,
            brand='Mastercard'
        )
        self.assertIsInstance(credit_card, CreditCard)
        self.assertEqual(str(credit_card), 'Mastercard ending with 4444')

    def test_user_creation(self):
        user = User.objects.create_user(
            name='newuser',
            password='newpassword',
            role=UserRole.ADMIN,
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.name, 'newuser')
        self.assertEqual(user.role, UserRole.ADMIN)

    def test_user_name_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(name='', password='testpassword', role=UserRole.ADMIN)

    def test_user_role_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(name='testuser', password='testpassword', role='')

    def test_user_create_superuser(self):
        user = User.objects.create_superuser(name='admin', password='password')
        self.assertTrue(user.is_admin)
        self.assertEqual(user.role, UserRole.ADMIN)

    def test_user_has_perm(self):
        self.assertTrue(self.user.has_perm('credit_card.add_creditcard'))
        self.assertTrue(self.user.has_perm('credit_card.change_creditcard'))
        self.assertTrue(self.user.has_perm('credit_card.delete_creditcard'))
        self.assertTrue(self.user.has_perm('credit_card.view_creditcard'))

    def test_user_has_module_perms(self):
        self.assertTrue(self.user.has_module_perms('credit_card'))

    def test_user_is_staff(self):
        self.assertFalse(self.user.is_staff)

    def test_holder_serializer(self):
        serializer = HolderSerializer(self.holder)
        expected_data = {'id': self.holder.id, 'name': 'John Doe'}
        self.assertEqual(serializer.data, expected_data)

    def test_credit_card_serializer(self):
        serializer = CreditCardSerializer(self.credit_card)
        expected_data = {
            'id': self.credit_card.id,
            'exp_date': '2025-12-31',
            'holder': {'id': self.holder.id, 'name': 'John Doe'},
            'number': '4111111111111111',
            'cvv': '123',
            'brand': 'Visa'
        }
        self.assertEqual(serializer.data, expected_data)

    def test_credit_card_create_serializer(self):
        data = {
            'exp_date': '2025-12-31',
            'holder': self.holder.id,
            'number': '4111111111111111',
            'cvv': '123',
            'brand': 'Visa'
        }
        serializer = CreditCardCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_user_serializer(self):
        serializer = UserSerializer(self.user)
        expected_data = {'id': self.user.id, 'name': 'testuser', 'role': 'ADMIN'}
        self.assertEqual(serializer.data, expected_data)


class HolderViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(name='adminuser', password='adminpassword')
        self.token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.holder1 = Holder.objects.create(name='Holder 1')
        self.holder2 = Holder.objects.create(name='Holder 2')

    def test_get_all_holders(self):
        response = self.client.get(reverse('holder-list'), HTTP_AUTHORIZATION=f'Token {self.token}')
        holders = Holder.objects.all()
        serializer = HolderSerializer(holders, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_holder(self):
        response = self.client.get(reverse('holder-detail', kwargs={'pk': self.holder1.id}), HTTP_AUTHORIZATION=f'Token {self.token}')
        holder = Holder.objects.get(pk=self.holder1.id)
        serializer = HolderSerializer(holder)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_holder(self):
        data = {'name': 'Holder 3'}
        response = self.client.post(reverse('holder-list'), data=data, HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_holder(self):
        data = {'name': 'Updated Holder 1'}
        response = self.client.put(reverse('holder-detail', kwargs={'pk': self.holder1.id}), data=data, HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_holder(self):
        response = self.client.delete(reverse('holder-detail', kwargs={'pk': self.holder1.id}), HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_user(self):
        data = {'name': 'testuser', 'password': 'testpassword', 'role': UserRole.ADMIN}
        response = self.client.post(reverse('user-create'), data=data, HTTP_AUTHORIZATION=f'Token {self.token}')
        expected_data = {'id': 2, 'name': 'testuser', 'role': 'ADMIN'}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CreditCardViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(name='adminuser', password='adminpassword')
        self.token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.holder1 = Holder.objects.create(name='Holder 1')
        self.holder2 = Holder.objects.create(name='Holder 2')
        self.credit_card1 = CreditCard.objects.create(
            holder=self.holder1,
            number='4539578763621486',
            exp_date=timezone.now() + timedelta(days=30),
            cvv=123
        )
        self.credit_card2 = CreditCard.objects.create(
            holder=self.holder2,
            number='4539578763621486',
            exp_date=timezone.now() + timedelta(days=60),
            cvv=456
        )

    def test_list_credit_cards(self):
        response = self.client.get(reverse('credit-card-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_paginate_credit_cards(self):
        response = self.client.get(reverse('credit-card-list') + '?page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_credit_card(self):
        response = self.client.get(reverse('credit-card-detail', kwargs={'pk': self.credit_card1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number'], '4539578763621486')

    def test_delete_credit_card(self):
        response = self.client.delete(reverse('credit-card-detail', kwargs={'pk': self.credit_card1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CreditCard.objects.filter(id=self.credit_card1.id).exists())

    def test_create_credit_card(self):
        data = {
            "exp_date": "03/2035",
            "holder": self.holder1.name,
            "number": "4539578763621486",
            "cvv": "1234"
        }
        response = self.client.post(reverse('credit-card-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_credit_card_with_invalid_holder(self):
        data = {
            'holder': 'Invalid Holder Name',
            'exp_date': '02/2035',
            'number': '4539578763621486',
        }
        response = self.client.post(reverse('credit-card-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_credit_card_with_invalid_exp_date(self):
        data = {
            'holder': self.holder2.name,
            'exp_date': '02/2035',
            'number': '4539578763621486',
        }
        response = self.client.post(reverse('credit-card-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_credit_card_with_expired_exp_date(self):
        data = {
            'holder': self.holder2.name,
            'exp_date': '02/2035',
            'number': '4539578763621486',
        }
        response = self.client.post(reverse('credit-card-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)