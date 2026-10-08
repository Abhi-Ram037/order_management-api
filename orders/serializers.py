from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Customer name cannot be empty."
            )
        return value

    def validate_email(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Email cannot be empty."
            )
        return value


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Product name cannot be empty."
            )
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value


class OrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_name',
            'quantity',
            'price'
        ]


class OrderSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source='customer.name',
        read_only=True
    )

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'customer_name',
            'order_date',
            'total_amount',
            'status',
            'items'
        ]


class OrderCreateItemSerializer(serializers.Serializer):

    product = serializers.IntegerField()
    quantity = serializers.IntegerField(
        min_value=1
    )


class OrderCreateSerializer(serializers.Serializer):

    customer = serializers.IntegerField()

    items = OrderCreateItemSerializer(
        many=True
    )

    def validate_customer(self, value):

        if not Customer.objects.filter(
            id=value
        ).exists():

            raise serializers.ValidationError(
                "Customer does not exist."
            )

        return value

    def validate_items(self, value):

        if not value:

            raise serializers.ValidationError(
                "At least one product is required."
            )

        product_ids = [
            item['product']
            for item in value
        ]

        products = Product.objects.filter(
            id__in=product_ids
        )

        existing_ids = set(
            products.values_list(
                'id',
                flat=True
            )
        )

        for product_id in product_ids:

            if product_id not in existing_ids:

                raise serializers.ValidationError(
                    f"Product with id {product_id} "
                    f"does not exist."
                )

        for item in value:

            product = Product.objects.get(
                id=item['product']
            )

            if item['quantity'] > product.stock:

                raise serializers.ValidationError(
                    f"Not enough stock for "
                    f"{product.name}. "
                    f"Available stock: "
                    f"{product.stock}."
                )

        return value