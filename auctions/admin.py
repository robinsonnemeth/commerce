from django.contrib import admin
from .models import User
from .models import Category
from .models import Listing
from .models import Bid
from .models import CommmentListing
from .models import Watchlist
from .models import Winnerlist

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category")

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(CommmentListing)
admin.site.register(Watchlist)
admin.site.register(Winnerlist)