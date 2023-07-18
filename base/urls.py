from django.contrib import admin
from django.urls import path

from myproj import settings
from . import views
from .views import LoginView
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index),
    path('products', views.ProductViewSet.as_view()),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', views.register),
    path('products/<pk>', views.ProductViewSet.as_view()),
    path('get_all_images', views.getImages),
    path('cart', views.CartView.as_view()),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns = [
#     path('user', views.get_user_info),
#     path('prods', views.ProductViewSet.as_view()),
#     path('prods/<pk>', views.ProductViewSet.as_view()),
#     path('orders', views.OrderViewSet.as_view()),
#     path('orders/<pk>', views.OrderViewSet.as_view()),
#     path('deliveries', views.DeliveriesViewSet.as_view()),
#     path('deliveries/<pk>', views.DeliveriesViewSet.as_view()),
#     path('register/', views.register),
#     path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('about', views.about),
#     path('cart', views.CartView.as_view()),
#     path('get_all_images', views.getImages),
#     path('upload_image',views.APIViews.as_view()),
#     path('my-orders', views.CartView.as_view())
# ]