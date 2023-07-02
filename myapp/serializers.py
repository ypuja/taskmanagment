from rest_framework import serializers
from .models import Task,CustomUser


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username','email', 'first_name', 'last_name', 'password', 'confirm_password')

    def __init__(self, *args, **kwargs):
        super(RegistrationSerializer, self).__init__(*args, **kwargs)
        self.fields['password'].error_messages['blank'] = 'Password Required'
        self.fields['confirm_password'].error_messages['blank'] = 'Confirm Password Required'
        self.fields['email'].error_messages['blank'] = 'Email Required'


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class GetataskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id','status')
