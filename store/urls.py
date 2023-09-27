from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('products/', views.store, name='store'),
    path('product_detail/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('update_item/', views.update_item, name='update_item'),
    path('process_order/', views.process_order, name='process_order'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('search_category/<int:id>/', views.search_category, name='search-category'),
]