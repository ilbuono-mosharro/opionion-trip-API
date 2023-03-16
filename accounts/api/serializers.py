from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils import send_activation_email

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, style={"input_type": "password"}, )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password1', 'age', 'terms_and_privacy']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, attrs):
        if User.objects.filter(username__iexact=attrs).exists():
            raise serializers.ValidationError("That username is already taken.")
        return attrs

    def validate(self, attrs):
        password = attrs.get('password')
        password1 = attrs.pop('password1', None)
        if password != password1:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        user = User(
            username=validated_data['username'], email=validated_data['email'], age=validated_data['age'],
            terms_and_privacy=validated_data['terms_and_privacy']
        )
        user.set_password(validated_data['password'])
        user.ip = self.context.get('request').META.get("REMOTE_ADDR")
        user.is_active = False
        user.save()
        send_activation_email(request=self.context.get('request'), user=user)
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'gender', 'city',
                  'contry', 'ip']
        read_only_fields = ['username', 'email', 'ip']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.city = validated_data.get('city', instance.city)
        instance.contry = validated_data.get('contry', instance.contry)
        instance.save()
        return instance
