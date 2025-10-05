from django.contrib import admin
from medicine_management_app.models import *
# Register your models here.

admin.site.register(Medicine)
admin.site.register(Category)
admin.site.register(Usage)
admin.site.register(Dosage)
admin.site.register(Profile)
admin.site.register(PendingMedicine)
admin.site.register(Reserve)
admin.site.register(ReserveMedicine)
admin.site.register(ReserveActivity)
admin.site.register(MedicineIntake)