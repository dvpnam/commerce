from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField(
        "Listing", blank=True, related_name="watched_by"
    )


class Listing(models.Model):
    CATEGORIES = [
        ("fashion", "Fashion"), ("toys", "Toys"),
        ("electronics", "Electronics"), ("home", "Home"),
        ("others", "Others"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="other")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, null=True, blank=True,
                               on_delete=models.SET_NULL, related_name="won_listings")
    created_at = models.DateTimeField(auto_now_add=True)

    def current_price(self):
        top = self.bids.order_by("-amount").first()
        return top.amount if top else self.starting_bid

    def __str__(self):
        return self.title


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
