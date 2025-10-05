import datetime
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField(null=True, blank=True)
    morning_time = models.TimeField(null=True, blank=True)
    afternoon_time = models.TimeField(null=True, blank=True)
    evening_time = models.TimeField(null=True, blank=True)
    night_time = models.TimeField(null=True, blank=True)
    is_administrator = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    UNIT_CHOICES = {
        "ml": "milliliters",
        "g": "grams",
        "pcs": "pieces",
    }
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    unit = models.CharField(max_length=100, choices=UNIT_CHOICES)
    categories = models.ManyToManyField(Category, related_name="medicines")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_global = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.amount} {self.unit})"

class Usage(models.Model):
    UNIT_CHOICES = {
        "y": "years",
        "m": "months",
        "d": "days",
    }
    age_from = models.IntegerField(null=True, blank=True)
    age_to = models.IntegerField(null=True, blank=True)
    age_unit = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True)
    comments = models.TextField(blank=True)
    duration_days = models.IntegerField(null=True, blank=True)
    hours_between = models.IntegerField(null=True, blank=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.age_from is not None and self.age_to is not None:
            return f"{self.medicine.name} ({self.age_from}-{self.age_to} {self.age_unit})"
        elif self.age_from is not None:
            return f"{self.medicine.name} ({self.age_from}+ {self.age_unit})"
        else:
            return f"{self.medicine.name}"

class Dosage(models.Model):
    TIME_CHOICES = {
        "Morning": "06:00-12:00",
        "Afternoon": "12:00-17:00",
        "Evening": "17:00-21:00",
        "Night": "21:00-06:00",
    }
    amount = models.FloatField()
    time = models.CharField(max_length=100, choices=TIME_CHOICES)
    usage = models.ForeignKey(Usage, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount}-{self.time} ({self.usage})"

class PendingMedicine(models.Model):
    STATUS_CHOICES = {
        "a": "approved",
        "r": "rejected",
        "p": "pending",
    }
    is_closed = models.BooleanField(default=False)
    medicine = models.OneToOneField(Medicine, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    last_modified = models.DateTimeField(auto_now=True)
    comments = models.TextField(blank=True)
    def __str__(self):
        return f"{self.medicine} ({self.status})"

class Reserve(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}"

class ReserveMedicine(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    amount = models.FloatField()
    reserve = models.ForeignKey(Reserve, on_delete=models.CASCADE, related_name="medicine")
    def __str__(self):
        return f"{self.medicine} ({self.reserve})"

class ReserveActivity(models.Model):
    reserve_medicine = models.ForeignKey(ReserveMedicine, on_delete=models.CASCADE)
    consumed_amount = models.FloatField()
    date_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"-{self.consumed_amount} {self.reserve_medicine.medicine.unit} ({self.reserve_medicine})"

class MedicineIntake(models.Model):
    reserve_medicine = models.ForeignKey(ReserveMedicine, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    usage = models.ForeignKey(Usage, on_delete=models.CASCADE)
    duration_from = models.DateField(default=datetime.date.today)
    duration_to = models.DateField(null=True, blank=True)
    morning_time = models.TimeField(null=True, blank=True)
    afternoon_time = models.TimeField(null=True, blank=True)
    evening_time = models.TimeField(null=True, blank=True)
    night_time = models.TimeField(null=True, blank=True)
    last_intake = models.DateTimeField(default=datetime.datetime.now)
    def __str__(self):
        return f"{self.reserve_medicine} - {self.user}"
