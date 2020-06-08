from django.urls import path
from accounts.views.views import home, customers, products, createOrder, \
    updateOrder, deleteOrder, userPage, accountSetting
from accounts.views.classbased_view import HomeView, UserPageView, AccountSettingView, \
    ProductsView, CustomerView, OrderCreateView, OrderUpdateView, OrderDeleteView

urlpatterns = [

    # Function based views urls
    # path('', home, name='home'),
    # path('user/', userPage, name='user-page'),
    # path('account/', accountSetting, name='account'),
    # path('products/', products, name='products'),
    # path('customers/<str:pk>', customers, name='customers'),

    # path('create_order/<str:pk>', createOrder, name='create_order'),
    # path('update_order/<str:pk>', updateOrder, name='update_order'),
    path('delete_order/<str:pk>', deleteOrder, name='delete_order'),

    # Class based views urls
    path('', HomeView.as_view(), name='home'),
    path('user/', UserPageView.as_view(), name='user-page'),
    path('account/', AccountSettingView.as_view(), name='account'),
    path('products/', ProductsView.as_view(), name='products'),
    path('customers/<str:pk>', CustomerView.as_view(), name='customers'),

    path('create_order/<str:pk>', OrderCreateView.as_view(), name='create_order'),
    path('update_order/<str:pk>', OrderUpdateView.as_view(), name='update_order'),
    # path('delete_order/<str:pk>', OrderDeleteView.as_view(), name='delete_order'),
]
