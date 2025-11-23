from django.urls import path
from .views import CategoryViews, MedicineViews, UsageViews, DosageViews, ProfileViews, ReserveView, MedicineIntakeViews

urlpatterns = [
    #Category urls
    path("category", CategoryViews.categories_list, name="categories"),
    path("category/<int:pk>", CategoryViews.category_detail, name="category_detail"),
    path("category/create", CategoryViews.category_create, name="category_create"),
    path("category/update/<int:pk>", CategoryViews.category_update, name="category_update"),
    path("category/delete/<int:pk>", CategoryViews.category_delete, name="category_delete"),
    path("category/<int:pk>/medicine", CategoryViews.category_medicine, name="category_medicine"),

    #Medicine urls
    path("medicine", MedicineViews.medicine_list, name="medicine_list"),
    path("medicine/<int:pk>", MedicineViews.medicine_detail, name="medicine_detail"),
    path("medicine/create", MedicineViews.medicine_create, name="medicine_create"),
    path("medicine/update/<int:pk>", MedicineViews.medicine_update, name="medicine_update"),
    path("medicine/delete/<int:pk>", MedicineViews.medicine_delete, name="medicine_delete"),
    path("medicine/<int:pk>/usage", MedicineViews.medicine_usage, name="medicine_usage"),
    path("pending/medicine", MedicineViews.pending_medicine_list, name="pending_medicine_list"),
    path("pending/medicine/<int:pk>", MedicineViews.pending_medicine_detail, name="pending_medicine_detail"),
    path("pending/medicine/create", MedicineViews.pending_medicine_create, name="pending_medicine_create"),
    path("pending/medicine/update/<int:pk>", MedicineViews.pending_medicine_update, name="pending_medicine_update"),

    #Usage urls
    path("usage", UsageViews.usage_list, name="usage_list"),
    path("usage/<int:pk>", UsageViews.usage_detail, name="usage_detail"),
    path("usage/create", UsageViews.usage_create, name="usage_create"),
    path("usage/update/<int:pk>", UsageViews.usage_update, name="usage_update"),
    path("usage/delete/<int:pk>", UsageViews.usage_delete, name="usage_delete"),
    path("usage/<int:pk>/dosages", UsageViews.dosage_list, name="dosage_list"),

    #Dosage urls
    path("dosage/<int:pk>", DosageViews.dosage_detail, name="dosage_detail"),
    path("dosage/create", DosageViews.dosage_create, name="dosage_create"),
    path("dosage/update/<int:pk>", DosageViews.dosage_update, name="dosage_update"),
    path("dosage/delete/<int:pk>", DosageViews.dosage_delete, name="dosage_delete"),

    #Profile urls
    path("profile", ProfileViews.profile_details, name="profile_details"),
    path("register", ProfileViews.register_user, name="register"),
    path("login", ProfileViews.login_user, name="login_user"),
    path("logout", ProfileViews.logout_user, name="logout_user"),
    path("profile/update", ProfileViews.update_profile, name="update_profile"),
    path("profile/change_password", ProfileViews.change_password, name="change_password"),

    #Reserve urls
    path("reserves", ReserveView.reserve_list, name="reserves_list"),
    path("reserve/<int:pk>", ReserveView.reserve_detail, name="reserve_detail"),
    path("reserve/create", ReserveView.reserve_create, name="reserve_create"),
    path("reserve/update/<int:pk>", ReserveView.reserve_update, name="reserve_update"),
    path("reserve/delete/<int:pk>", ReserveView.reserve_delete, name="reserve_delete"),
    path("reserve/<int:pk>/medicine", ReserveView.reserve_medicine_list, name="reserve_medicine_list"),
    path("reserve/add_medicine", ReserveView.reserve_medicine_add, name="reserve_medicine_add"),
    path("reserve/<int:pk>/medicine/<int:med_pk>", ReserveView.reserve_medicine_detail, name="reserve_medicine_detail"),
    path("reserve/<int:pk>/medicine/update/<int:med_pk>", ReserveView.reserve_medicine_update, name="reserve_medicine_update"),
    path("reserve/<int:pk>/medicine/<int:med_pk>/consume", ReserveView.reserve_medicine_consume, name="reserve_medicine_consume"),
    path("reserve/<int:pk>/activity", ReserveView.reserve_activity_details, name="reserve_activity"),
    path("reserve/<int:pk>/medicine/<int:med_pk>/usages", ReserveView.reserve_medicine_usages, name="reserve_usages"),

    #Medicine intake urls
    path("medicine_intakes", MedicineIntakeViews.medicine_intake_list, name="medicine_intake_list"),
    path("medicine_intake/<int:pk>", MedicineIntakeViews.medicine_intake_detail, name="medicine_intake_detail"),
    path("medicine_intake/create", MedicineIntakeViews.medicine_intake_create, name="medicine_intake_create"),
    path("medicine_intake/update/<int:pk>", MedicineIntakeViews.medicine_intake_update, name="medicine_intake_update"),
    path("medicine_intake/delete/<int:pk>", MedicineIntakeViews.medicine_intake_delete, name="medicine_intake_delete"),
    path("medicine_intake/notifications", MedicineIntakeViews.retrieve_medicine_past_consumption_time, name="notifications"),
]