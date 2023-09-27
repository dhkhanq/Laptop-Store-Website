from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.

# class CustomerUser(AbstractUser):
#     phone_number = models.CharField(default='', max_length=10)
#     address = models.CharField(default='', max_length=255)

# class Category(models.Model):
#     title = models.CharField(default='', max_length=100)
#     slug = models.CharField(max_length=100, default='')
#     description = models.TextField(default='')
#     active = models.BooleanField(default=True)

# class Product(models.Model):
#     title = models.CharField(max_length=255, default=100)
#     description = models.TextField(default='')
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     price = models.IntegerField(default=0)
#     active = models.BooleanField(default=True)

# class Variation(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     title = models.CharField(default='', max_length='')
#     price = models.IntegerField(default=0)
#     sale_price = models.IntegerField(default=0)
#     inventory = models.IntegerField(default=0)
#     active = models.BooleanField(default=True)

# class Cart(models.Model):
#     user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     item = models.ForeignKey(Variation, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=0)


# class Order(models.Model):
#     user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     shipping_address = models.CharField(max_length=255, default='')
#     order_description = models.TextField(default='')
#     is_completed = models.BooleanField(default=False)


#-----------------------------------------------------------------------------


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(default='', max_length=10)
    email = models.CharField(max_length=200, null= True)
    customer_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def user_image_url(self):
        try:
            url = self.customer_image.url
        except:
            url = ''
        return url

class Category(models.Model):
    name = models.CharField(default='', max_length=100)
    # slug = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    category_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def image_category_url(self):
        try:
            url = self.category_image.url
        except:
            url = ''
        return url

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    monitor_size = models.FloatField()
    cpu = models.CharField(default='', max_length=100)
    gpu = models.CharField(default='', max_length=100)
    ram = models.CharField(default='', max_length=100)
    harddrive = models.CharField(default='', max_length=100)
    weight = models.FloatField()
    # digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


# class Promotion(models.Model):
#     title = models.CharField(default='', max_length=100)
#     discount_rate = models.IntegerField
#     description = models.TextField(default='')
#     active = models.BooleanField(default=True)


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.customer)

    @property
    def get_cart_total(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.get_total for item in cartitems])
        return total

    @property
    def get_cart_items(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.quantity for item in cartitems])
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cart)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    price_total = models.FloatField(default=0)
    product_total = models.IntegerField(default=0)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.customer) + " " + str(self.date_orderd)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.order)
    


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
