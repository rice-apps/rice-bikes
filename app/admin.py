from django.contrib import admin
from app.models import Transaction, Task, RentalBike,\
    RefurbishedBike, RevenueUpdate, TotalRevenue, PartCategory, PartOrder, \
    TaskMenuItem, AccessoryMenuItem, PartMenuItem, BuyBackBike

admin.site.register(Transaction)
admin.site.register(RentalBike)
admin.site.register(RefurbishedBike)
admin.site.register(BuyBackBike)
admin.site.register(RevenueUpdate)
admin.site.register(TaskMenuItem)
admin.site.register(AccessoryMenuItem)
admin.site.register(PartMenuItem)


class TotalRevenueAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True

admin.site.register(TotalRevenue, TotalRevenueAdmin)