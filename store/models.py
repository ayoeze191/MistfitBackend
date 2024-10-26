from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=10000, null=True, blank=True)
    def __str__(self):
        return self.title

def get_image_file_path(self, instance):
    return f"products/{self.product.name}/{instance}"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50) 
    description = models.TextField(null=True, blank=True)
    stock_price = models.DecimalField(decimal_places=4, max_digits=10)
    stock_quantity = models.IntegerField()
    def __str__(self):
        return self.name
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productimage")
    image = models.ImageField(null = True, blank = True, upload_to = get_image_file_path, )

    def __str__(self):
        return self.image.url

class ProductReview(models.Model):
    description = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productreview")

class ShoeDetails(models.Model):
    title = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="shoesize")
    sizes = models.CharField(max_length=50) 
    color_option = models.CharField(max_length=50) 
# def get_image_file_path(self, filename):
#     return f"{self.foldername}/{'profile-image.png'}"

