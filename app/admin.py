from django.contrib import admin
from app.models import Transaction, Task, RentalBike,\
    RefurbishedBike, RevenueUpdate, TotalRevenue, PartCategory, PartOrder, MenuItem

admin.site.register(Transaction)
admin.site.register(Task)
admin.site.register(RentalBike)
admin.site.register(RefurbishedBike)
admin.site.register(RevenueUpdate)
admin.site.register(PartCategory)
admin.site.register(PartOrder)
admin.site.register(MenuItem)

class TotalRevenueAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True

admin.site.register(TotalRevenue, TotalRevenueAdmin)