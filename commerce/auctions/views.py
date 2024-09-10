from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comments, Bid


def index(request):
    active_listings = Listing.objects.filter(active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "categories": categories
    })


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

def create_listing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
           "categories": categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        year = request.POST["year"]
        kilometres = request.POST["kilometres"]
        isUsed = request.POST.get("isUsed", False)
        isWorking = request.POST.get("isWorking", False)
        isStock = request.POST.get("isStock", False)
        warranty = request.POST["warranty"]
        price = request.POST["price"]
        image = request.POST["image"]
        category_name = request.POST["category"]
        category = Category.objects.get(category=category_name)
        user = request.user
        newList = Listing(
            title=title, 
            description=description, 
            year=year, 
            kilometres=kilometres, 
            isUsed=isUsed, 
            isWorking=isWorking, 
            isStock=isStock, 
            warranty=warranty, 
            image=image, 
            category=category, 
            user=user
        )
        newList.save()
        bid = Bid(bid=float(price), user=user, listing=newList)
        bid.save()
        newList.price = bid
        newList.save()
        
        return HttpResponseRedirect(reverse("index"))

def filter_categories(request):
    category_name = request.POST["category"]
    category = Category.objects.get(category=category_name)
    active_listings = Listing.objects.filter(category=category, active=True)
    categories = Category.objects.all()
    if category_name == "All":
        active_listings = Listing.objects.filter(active=True)
    else:
        active_listings = Listing.objects.filter(category=category, active=True)
        if not active_listings:
            return render(request, "auctions/index.html", {
                "message": "No listings found.",
                "categories": categories
            })
        if not categories:
            return render(request, "auctions/index.html", {
                "message": "No categories found.",
                "listings": active_listings
            })
        if not active_listings and not categories:
            return render(request, "auctions/index.html", {
                "message": "No listings or categories found."
            }) 
        return render(request, "auctions/index.html", {
            "listings": active_listings,
            "categories": categories
        })
    
def listing(request, id):
    listing = Listing.objects.get(pk=id)
    watchlist = request.user in listing.watchlist.all()
    all_comments = Comments.objects.filter(listing=id)
    owner = request.user.username == listing.user.username
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": watchlist,
        "comments": all_comments,
        "owner": owner,
    })

def add_to_watchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def remove_watchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def watchlist(request):
    user = request.user
    watchlist = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def add_comment(request, id):
    if request.method == "POST":
        comment = request.POST["comment"]
        author = request.user
        listing = Listing.objects.get(pk=id)
        newComment = Comments(author=author, listing=listing, comment=comment)
        newComment.save()
        return HttpResponseRedirect(reverse("listing", args=(id,)))
    else:
        return render(request, "auctions/listing.html")
    
def delete_comment(request, id):
    comment = Comments.objects.get(pk=id)
    if request.user != comment.author and request.user != comment.listing.user:
        return HttpResponse("ERROR: You are not allowed to delete this comment.")
    else:
        comment.delete()
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def bid(request, id):
    new_bid = request.POST["bid"]
    listing = Listing.objects.get(pk=id)
    isOnWatchlist = request.user in listing.watchlist.all()
    all_comments = Comments.objects.filter(listing=id)
    if float(new_bid) <= listing.price.bid:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "watchlist": isOnWatchlist,
            "comments": all_comments,
            "message": "Your bid must be higher than the current price."
        })
    else:
        newBid = Bid(bid=float(new_bid), user=request.user, listing=listing)
        newBid.save()
        listing.price = newBid
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(id,)))
    
def close_listing(request, id):
    listing = Listing.objects.get(pk=id)
    listing.active = False
    listing.winner = listing.listingBids.last().user
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))

