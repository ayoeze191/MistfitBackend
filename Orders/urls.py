from django.urls import path
from .views import CartComponents, AuthenticatedUserCart, ProcessOrder
urlpatterns = [
    path('UserCart', CartComponents.as_view()),
    path('AddorDelete/<int:pk>', AuthenticatedUserCart.as_view()),
    path('processOrder', ProcessOrder.as_view())
]
