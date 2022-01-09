"""rantangin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', accounts_views.HomeView.as_view(), name="home"),
    path('signup/', accounts_views.register, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),

    path('product/<pk>/', accounts_views.ProductView.as_view(), name='product'),
    path('add-to-cart/<pk>/', accounts_views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<pk>/', accounts_views.remove_from_cart, name='remove-from-cart'),
    path('keranjang/', accounts_views.OrderSummaryView.as_view(), name='keranjang'),
    path('reduce-quantity-item/<pk>/', accounts_views.reduce_quantity_item, name='reduce-quantity-item'),
    path('checkout/', accounts_views.CheckoutView.as_view(), name='checkout'),
    path('payments/', accounts_views.PaymentView.as_view(), name='payments')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)