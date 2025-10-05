from rest_framework import serializers

from medicine_management_app.models import Medicine, Profile, Category, Usage, Dosage, Reserve, ReserveMedicine, \
    PendingMedicine, ReserveActivity, MedicineIntake


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
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
        fields = '__all__'

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
        fields = '__all__'
