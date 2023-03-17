from rest_framework import serializers
from ..models import Attractions, ImageAttractions
from accounts.api.serializers import UserInfoSerializer


class AttractionsSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    users_wishlist = UserInfoSerializer(read_only=True, many=True)

    class Meta:
        model = Attractions
        fields = ['city', 'user', 'name', 'adress', 'cap', 'title', 'description', 'is_active', 'copertina',
                  'users_wishlist', 'ip', 'created_at']
        read_only_fields = ['ip']

    def create(self, validated_data):
        return Attractions.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.city = validated_data.get('city', instance.city)
        instance.name = validated_data.get('name', instance.name)
        instance.adress = validated_data.get('adress', instance.adress)
        instance.cap = validated_data.get('cap', instance.cap)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.copertina = validated_data.get('copertina', instance.copertina)
        instance.save()
        return instance

class ImageAttractionSerializer(serializers.ModelSerializer):
    attraction = AttractionsSerializer(read_only=True)

    class Meta:
        model = ImageAttractions
        fields = ['attraction', 'user', 'image', 'alt_text', 'is_active', 'ip', 'created_at']
        read_only_fields = ['user', 'ip']