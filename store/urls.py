from django.urls import path
from .views import ProductDetailView, ProductsView, ProductSearchView
urlpatterns = [
    path('products', ProductsView.as_view()),
    path('productSearch', ProductSearchView.as_view()),
    path('productDetails/<pk>', ProductDetailView.as_view())
]