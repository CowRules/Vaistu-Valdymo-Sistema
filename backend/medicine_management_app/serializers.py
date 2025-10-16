from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from medicine_management_app.models import Medicine, Profile, Category, Usage, Dosage, Reserve, ReserveMedicine, \
    PendingMedicine, ReserveActivity, MedicineIntake


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'age', 'morning_time', 'afternoon_time', 'evening_time', 'night_time', 'is_administrator']

class CategorySerializer(serializers.ModelSerializer):
    medicines = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    class Meta:
        model = Category
        fields = ['id', 'name', 'medicines']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class UsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usage
        fields = '__all__'

class DosageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dosage
        fields = '__all__'

class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ['id', 'name']

class ReserveMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReserveMedicine
        fields = '__all__'

class PendingMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingMedicine
        fields = '__all__'

class ReserveActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReserveActivity
        fields = '__all__'

class MedicineIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineIntake
        fields = ["reserve_medicine", "usage", "duration_from", "duration_to", "morning_time", "afternoon_time",
                  "evening_time", "night_time", "last_intake"]

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, validators=[
        UniqueValidator(queryset=User.objects.all(), message="Email is already registered with another account.")
    ])
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
