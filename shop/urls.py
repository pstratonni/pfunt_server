from django.urls import path

from .views import *

urlpatterns = [
    # URL for purchaser
    path('manufacturers/', ManufacturerAPIList.as_view(), ),
    path('manufacturer/<int:pk>/', ManufacturerAPIRetriever.as_view(), ),
    path('products/', ProductAPIList.as_view(), ),
    path('product/<int:pk>/', ProductAPIRetriever.as_view(), ),
    path('categories/', CategoryListView.as_view()),
    path('orders/', OrderAPIListCreate.as_view(), ),
    path('order_ip/', OrderIPAPICreate.as_view(), ),
    path('order/<int:pk>/', OrderAPIRetrieve.as_view(), ),
    path('order_item/', OrderItemAPICreate.as_view(), ),
    path('cart/', CartAuthAPIRetrieveUpdateDestroy.as_view(), ),
    path('cart_ip/', CartIPAPI.as_view(), ),
    path('cart_item/create/', CartItemAPICreate.as_view(), ),
    path('cart_item/<int:pk>/', CartItemAPIUpdateDestroy.as_view(), ),
    path('cart_ip_item/create/', CartItemIPAPICreate.as_view(), ),
    path('cart_ip_item/<int:pk>/', CartItemIPAPIUpdateDestroy.as_view(), ),
    path('purchaser/<int:pk>', PurchaserAPIRetrieve.as_view()),

    # URL for admin
    path('admin/manufacturers/', ManufacturerIsAdminAPIList.as_view(), ),
    path('admin/manufacturer/<int:pk>/', ManufacturerIsAdminAPIRUD.as_view(), ),
    path('admin/products/', ProductIsAdminAPIList.as_view(), ),
    path('admin/product/<int:pk>/', ProductIsAdminAPIRUD.as_view(), ),
    path('admin/order/<int:pk>/', OrderAPIUpdate.as_view(),),
    path('admin/order_item/<int:pk>/', OrderItemAPIUpdate.as_view(),),
]
