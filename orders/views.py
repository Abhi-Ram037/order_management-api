from decimal import Decimal

from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer, Product, Order, OrderItem
from .serializers import (
    CustomerSerializer,
    ProductSerializer,
    OrderSerializer,
    OrderCreateSerializer
)


class HomeView(APIView):

    def get(self, request):
        return Response({
            "message": "Order Management API",
            "endpoints": {
                "customers": "/customers/",
                "products": "/products/",
                "orders": "/orders/",
                "admin": "/admin/"
            }
        })


class CustomerCreateView(APIView):

    def post(self, request):

        serializer = CustomerSerializer(
            data=request.data
        )

        if serializer.is_valid():
            customer = serializer.save()

            return Response(
                CustomerSerializer(customer).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductCreateView(APIView):

    def post(self, request):

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():
            product = serializer.save()

            return Response(
                ProductSerializer(product).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class OrderListCreateView(APIView):

    def get(self, request):

        orders = Order.objects.all().order_by('-id')

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):

        serializer = OrderCreateSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        customer_id = serializer.validated_data['customer']
        items = serializer.validated_data['items']

        customer = Customer.objects.get(
            id=customer_id
        )

        order = Order.objects.create(
            customer=customer,
            total_amount=Decimal('0.00'),
            status='Pending'
        )

        total_amount = Decimal('0.00')

        for item in items:

            product = Product.objects.select_for_update().get(
                id=item['product']
            )

            quantity = item['quantity']

            if quantity > product.stock:

                return Response(
                    {
                        'error': (
                            f'Not enough stock for '
                            f'{product.name}. '
                            f'Available stock: '
                            f'{product.stock}.'
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            item_total = product.price * quantity

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            product.stock -= quantity
            product.save()

            total_amount += item_total

        order.total_amount = total_amount
        order.save()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )


class OrderDetailView(APIView):

    def get(self, request, id):

        try:

            order = Order.objects.get(
                id=id
            )

        except Order.DoesNotExist:

            return Response(
                {
                    'error': 'Order not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderSerializer(order)

        return Response(serializer.data)


class OrderStatusUpdateView(APIView):

    def put(self, request, id):

        try:

            order = Order.objects.get(
                id=id
            )

        except Order.DoesNotExist:

            return Response(
                {
                    'error': 'Order not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if order.status == 'Cancelled':

            return Response(
                {
                    'error': (
                        'Cancelled orders '
                        'cannot be updated.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        new_status = request.data.get('status')

        valid_statuses = [
            'Pending',
            'Confirmed',
            'Shipped',
            'Delivered',
        ]

        if new_status not in valid_statuses:

            return Response(
                {
                    'error': (
                        'Invalid status. Choose from: '
                        'Pending, Confirmed, Shipped, '
                        'Delivered. Use the cancel endpoint'
                        ' to cancel an order.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        return Response(
            {
                'message': (
                    'Order status updated '
                    'successfully.'
                ),
                'order_id': order.id,
                'status': order.status
            }
        )


class OrderCancelView(APIView):

    @transaction.atomic
    def post(self, request, id):

        try:

            order = Order.objects.select_for_update().get(
                id=id
            )

        except Order.DoesNotExist:

            return Response(
                {
                    'error': 'Order not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if order.status == 'Cancelled':

            return Response(
                {
                    'error': (
                        'Order is already cancelled.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if order.status == 'Delivered':

            return Response(
                {
                    'error': (
                        'Delivered orders '
                        'cannot be cancelled.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order_items = OrderItem.objects.filter(
            order=order
        )

        for item in order_items:

            product = Product.objects.select_for_update().get(
                id=item.product.id
            )

            product.stock += item.quantity
            product.save()

        order.status = 'Cancelled'
        order.save()

        return Response(
            {
                'message': (
                    'Order cancelled '
                    'successfully.'
                ),
                'order_id': order.id,
                'status': order.status
            }
        )