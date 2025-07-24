from users.models import User
from rest_framework import serializers

class RegisterSerilizer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user
