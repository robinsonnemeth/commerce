from django.urls import path

from . import views
from django.urls import include, path


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("newAuction", views.newAuction, name="newAuction"),
    path("categorization", views.categorization, name="categorization"),
    path("detail_listing/<int:id_listing>", views.detail_listing, name="detail_listing"),
    path("newBid", views.newBid, name="newBid"),
    path("get_last_bid", views.get_last_bid, name="get_last_bid"),
    path("makecomment", views.makecomment, name="makecomment"),
    path("addwatchlist/<int:id_listing>", views.addwatchlist, name="addwatchlist"),
    path("removewatchlist/<int:id_listing>", views.removewatchlist, name="removewatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("finalize/<int:id_listing>", views.finalize, name="finalize"),
    path("nomsg", views.nomsg, name="nomsg"),
    path("winninglist", views.winninglist, name="winninglist"),
]
