from django.contrib import admin
from app.models import Transaction, Task, RentalBike, RefurbishedBike

admin.site.register(Transaction)
admin.site.register(Task)
admin.site.register(RentalBike)
admin.site.register(RefurbishedBike)