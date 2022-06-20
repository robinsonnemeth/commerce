from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    title_listing = models.CharField(max_length=64)
    active_listing = models.BooleanField(default=True)
    description = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_listing = models.URLField(blank=True, null=True)
    date_listing = models.DateTimeField(auto_now=...)

    def __str__(self):
        return f"{self.title_listing}: {self.price} From: {self.date_listing}"

class Bid(models.Model):
    user_bid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_bid")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")
    date_bid = models.DateTimeField(auto_now=...)
    bid = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.bid}: {self.listing} By:{self.user_bid} From:{self.date_bid}"

class CommmentListing(models.Model):
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_comment")
    listing_comment = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings_comment")
    date_comment = models.DateTimeField(auto_now=...)
    comment_text = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.user_comment}: {self.listing_comment} From:{self.date_comment}"

class Watchlist(models.Model):
    user_watchlist = models.OneToOneField(User, on_delete=models.CASCADE, related_name="users_watchlist")
    listing_watchlist = models.ManyToManyField(Listing)

class Winnerlist(models.Model):
    user_winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_winner")
    listing_winner = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="users_winner")
    show_msg = models.BooleanField(default=True)