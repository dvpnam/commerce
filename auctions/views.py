from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bid, Comment, Listing, User


def index(request):
    return render(
        request,
        "auctions/index.html",
        {
            "listings": Listing.objects.filter(active=True),
        },
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST.get("image_url", "")
        category = request.POST.get("category", "other")

        listing = Listing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            category=category,
            creator=request.user,
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create_listing.html",
        {
            "categories": Listing.CATEGORIES  
        }
    )


def listing(request, listing_id):
    item = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html",
        {
            "listing": item,
            "current_price": item.current_price(),  
        }
    )


@login_required
def place_bid(request, listing_id):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    item = Listing.objects.get(pk=listing_id)
    amount = float(request.POST["amount"])

    if amount <= item.current_price():
        return render(request, "auctions/listing.html",
            {
                "listing": item,
                "current_price": item.current_price(),
                "error": "Bid must be higher than current price.",  
            }
        )

    Bid.objects.create(listing=item, bidder=request.user, amount=amount)
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def close_auction(request, listing_id):
    item = Listing.objects.get(pk=listing_id)

    if request.user != item.creator:
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    top_bid = item.bids.order_by("-amount").first()
    item.active = False
    item.winner = top_bid.bidder if top_bid else None
    item.save()

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def toggle_watchlist(request, listing_id):
    item = Listing.objects.get(pk=listing_id)
    if item in request.user.watchlist.all():
        request.user.watchlist.remove(item)
    else:
        request.user.watchlist.add(item)
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def watch_list(request):
    return render(request, "auctions/watchlist.html",
        {
            "listings": request.user.watchlist.all()
        }
    )


@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        item = Listing.objects.get(pk=listing_id)
        Comment.objects.create(
            listing=item,
            author=request.user,
            text=request.POST["text"]
        )
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def categories(request):
    return render(request, "auctions/categories.html",
        {
            "categories": Listing.CATEGORIES
        }
    )


def category(request, name):
    return render(request, "auctions/category.html",
        {
            "category_name": name,
            "listings": Listing.objects.filter(category=name, active=True)
        }
    )
