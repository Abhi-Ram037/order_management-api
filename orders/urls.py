from django.urls import path

from .views import (
    HomeView,
    CustomerCreateView,
    ProductCreateView,
    OrderListCreateView,
    OrderDetailView,
    OrderStatusUpdateView,
    OrderCancelView
)


urlpatterns = [

    path(
        '',
        HomeView.as_view(),
        name='home'
    ),

    path(
        'customers/',
        CustomerCreateView.as_view(),
        name='create-customer'
    ),

    path(
        'products/',
        ProductCreateView.as_view(),
        name='create-product'
    ),

    path(
        'orders/',
        OrderListCreateView.as_view(),
        name='orders'
    ),

    path(
        'orders/<int:id>/',
        OrderDetailView.as_view(),
        name='order-detail'
    ),

    path(
        'orders/<int:id>/status/',
        OrderStatusUpdateView.as_view(),
        name='update-order-status'
    ),

    path(
        'orders/<int:id>/cancel/',
        OrderCancelView.as_view(),
        name='cancel-order'
    ),
]