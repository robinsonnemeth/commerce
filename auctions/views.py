from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db import IntegrityError
from .models import User, Listing, Category, Bid, CommmentListing, Watchlist, Winnerlist


class NewAuctionForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Description")
    choices_category = (('Option 1', 'Option 1'), ('Option 2', 'Option 2'),)
    category_select = forms.ModelChoiceField(queryset=Category.objects.all())
    price = forms.DecimalField(label="Initial price")
    url_image = forms.CharField(label="URL image")

def index(request):
    num_wins = 0
    msg = ''
    listings = Listing.objects.all().filter(active_listing=True)
    dict_list = {}
    element_listing = []
    for lists in listings:
        dict_list["title_listing"] = lists.title_listing
        dict_list["price"] = lists.price
        dict_list["last_bid"] = get_last_bid(lists.id)
        dict_list["image_listing"] = lists.image_listing
        dict_list["description"] = lists.description
        dict_list["id"] = lists.id
        element_listing.append(dict_list.copy())

    if request.user.id:
        user = User.objects.get(pk=request.user.id)
        wins = Winnerlist.objects.all().filter(user_winner=user, show_msg=True)
        num_wins = len(Winnerlist.objects.all().filter(user_winner=user))
        if len(wins) != 0:
            msg = 'Congratulations! You win an auction, check your winning list'

    return render(request, "auctions/index.html",{
        "categories": Category.objects.all(),
        "listings": element_listing,
        "msg": msg,
        "wins": num_wins,
    })

def categorization(request):
    if request.method == "POST" and request.POST["cat_select"]!="All":
        cat_select = request.POST.getlist("cat_select")
        return render(request, "auctions/index.html",{
            "listings": Listing.objects.all().filter(active_listing=True, category=cat_select[0]),
            "categories": Category.objects.all(),
            "cat_selected": cat_select[0],
        })
    else:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all().filter(active_listing=True),
            "categories": Category.objects.all()
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

@login_required
def createListing(request):
    return render(request, "auctions/createListing.html",{
        "form": NewAuctionForm()
    })

@login_required
def newAuction(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        category = Category.objects.get(pk=request.POST["category_select"])
        title_listing = request.POST["title"]
        description = request.POST["content"]
        price = request.POST["price"]
        image_listing = request.POST["url_image"]
        auction = Listing(user=user, category=category, title_listing=title_listing, description=description, price=price, image_listing=image_listing)
        auction.save()
        return redirect('/')
    else:
        return render(request, "auctions/createListing.html", {
            "form": NewAuctionForm()
        })

@login_required
def newBid(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        listing_id = Listing.objects.get(pk=request.POST["listingId"])
        bid = request.POST["newBid"]

        auction_bid = Bid(user_bid=user, listing=listing_id, bid=bid)
        auction_bid.save()
        response = '/detail_listing/' + str(listing_id.id)
        return redirect(response)
    else:
        return redirect('/')

@login_required
def detail_listing(request, id_listing):
    price_detail = (Listing.objects.all().filter(pk=id_listing))[0].price
    last_bid = (Bid.objects.all().filter(listing=id_listing)).last()
    if last_bid is not None:
        last_bid = last_bid.bid
    else:
        last_bid = price_detail

    return render(request, "auctions/detail_listing.html", {
        "listing_detail": Listing.objects.all().filter(pk=id_listing),
        "title_detail": (Listing.objects.all().filter(pk=id_listing))[0].title_listing,
        "image_detail": (Listing.objects.all().filter(pk=id_listing))[0].image_listing,
        "description_detail": (Listing.objects.all().filter(pk=id_listing))[0].description,
        "price_detail": price_detail,
        "id_listing": id_listing,
        "last_bid": last_bid,
        "price_min": float(last_bid)+0.01,
        "comments": CommmentListing.objects.all().filter(listing_comment=id_listing).order_by('-date_comment'),
        "listing_user": (Listing.objects.all().filter(pk=id_listing))[0].user,
        "active_listing": (Listing.objects.all().filter(pk=id_listing))[0].active_listing,
    })

def get_last_bid(id_listing):
    last_bid = (Bid.objects.all().filter(listing=id_listing)).last()
    if last_bid is not None:
        return last_bid.bid
    else:
        return 'No Bid'

@login_required
def makecomment(request):
    comment_text = request.POST["makecomment"]
    user_comment = User.objects.get(pk=request.user.id)
    listing_id = Listing.objects.get(pk=request.POST["listingId"])
    auction = CommmentListing(user_comment=user_comment, listing_comment=listing_id, comment_text=comment_text)
    auction.save()
    response = '/detail_listing/'+ str(listing_id.id)
    return redirect(response)

@login_required
def addwatchlist(request, id_listing):
    user_watchlist = User.objects.get(pk=request.user.id)
    listing_watchlist = Listing.objects.get(pk=id_listing)
    auction = Watchlist(user_watchlist=user_watchlist)
    try:
        auction.save()
        auction.listing_watchlist.set([listing_watchlist])
    except IntegrityError as e:
        if 'UNIQUE constraint' in e.args[0]:
            try:
                add_to_watchlist = Watchlist.objects.get(user_watchlist=User.objects.get(pk=request.user.id))
                add_to_watchlist.listing_watchlist.add(listing_watchlist)
            except IntegrityError as e:
                print(e)

    return redirect('/watchlist')

@login_required
def removewatchlist(request, id_listing):
    listing_watchlist = Listing.objects.get(pk=id_listing)
    remove_watchlist = Watchlist.objects.get(user_watchlist=User.objects.get(pk=request.user.id))
    remove_watchlist.listing_watchlist.remove(listing_watchlist)

    return redirect('/watchlist')

@login_required
def watchlist(request):
    user_watchlist = User.objects.get(pk=request.user.id)
    try:
        watchlists = Watchlist.objects.get(user_watchlist=user_watchlist)
        watcheslist = watchlists.listing_watchlist.all()
        listings = Listing.objects.all()
        dict_list = {}
        element_listing = []
        for lists in listings:
            for watches in watcheslist:
                if watches == lists:
                    print(watches)
                    print(lists)
                    dict_list["title_listing"] = lists.title_listing
                    dict_list["price"] = lists.price
                    dict_list["last_bid"] = get_last_bid(lists.id)
                    dict_list["image_listing"] = lists.image_listing
                    dict_list["description"] = lists.description
                    dict_list["id"] = lists.id
                    element_listing.append(dict_list.copy())

        return render(request, "auctions/watchlist.html", {
            "categories": Category.objects.all(),
            "listings": element_listing,
        })
    except:
        return render(request, "auctions/watchlist.html")

@login_required
def finalize(request, id_listing):
    listing_finalize = Listing.objects.get(pk=id_listing)
    listing_finalize.active_listing = False
    listing_finalize.save()

    last_bid = (Bid.objects.all().filter(listing=id_listing)).last()
    if last_bid is not None:
        user_winner = last_bid.user_bid
        winnerlist = Winnerlist(user_winner=user_winner , listing_winner=listing_finalize)
        winnerlist.save()

    return redirect('/')


class HttpRequest(object):
    pass


@login_required
def nomsg(request):
    user_nomsg = User.objects.get(pk=request.user.id)
    list_wins = Winnerlist.objects.all().filter(user_winner=user_nomsg)
    if len(list_wins)>1:
        for lists_wins in list_wins:
            lists_wins.show_msg = False
            lists_wins.save()
    else:
        list_wins.show_msg = False
        list_wins.save()

    return redirect('/')

@login_required
def winninglist(request):
    user_nomsg = User.objects.get(pk=request.user.id)
    list_wins = Winnerlist.objects.all().filter(user_winner=user_nomsg)

    listings = Listing.objects.all().filter(active_listing=False)
    dict_list = {}
    element_listing = []
    for lists in listings:
        for wins in list_wins:
            print(wins.listing_winner)
            if wins.listing_winner == lists:
                dict_list["title_listing"] = lists.title_listing
                dict_list["price"] = lists.price
                dict_list["last_bid"] = get_last_bid(lists.id)
                dict_list["image_listing"] = lists.image_listing
                dict_list["description"] = lists.description
                dict_list["id"] = lists.id
                element_listing.append(dict_list.copy())

    return render(request, "auctions/winninglist.html", {
        "categories": Category.objects.all(),
        "listings": element_listing,
        "list_wins": list_wins,
    })
