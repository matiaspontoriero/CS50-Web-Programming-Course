from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userBids")
    bid = models.DecimalField(max_digits=30, decimal_places=2)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="listingBids")

    def __str__(self):
        if self.user == self.listing.user:
            return f"{self.bid}"
        else:
            return f"{self.user} bid on {self.listing} for {self.bid}"
    
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    year = models.IntegerField(blank=True, null=True)
    kilometres = models.IntegerField(blank=True, null=True)
    isUsed = models.BooleanField(default=True)
    isWorking = models.BooleanField(default=True)
    isStock = models.BooleanField(default=True)
    warranty = models.IntegerField(blank=True, null=True)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="price", blank=True, null=True)
    image = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", blank=True, null=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title}"
    
class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="authorComm")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="ListingComm")
    comment = models.TextField()

    def __str__(self):
        return f"{self.author} comment on {self.listing}"
