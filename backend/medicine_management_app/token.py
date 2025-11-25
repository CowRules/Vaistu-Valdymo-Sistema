from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print("In serializer")
        token = super().get_token(user)
        print("got token")
        print(user)
        token['role'] = user.profile.role
        print("added role")
        return token