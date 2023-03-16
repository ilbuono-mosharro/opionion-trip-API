from rest_framework import serializers
from ..models import City, ImageCity

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['user', 'name', 'title', 'description', 'is_active', 'copertina', 'ip', 'created_at']
        read_only_fields = ['user', 'ip', 'created_at']


    def create(self, validated_data):
        city = City(**validated_data)
        city.ip = self.context['request'].META.get("REMOTE_ADDR")
        city.save()
        return city

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.copertina = validated_data.get('copertina', instance.copertina)
        instance.ip = self.context['request'].META.get("REMOTE_ADDR")
        instance.save()
        return instance


class ImageCitySerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    class Meta:
        model = ImageCity
        fields = ['city', 'user', 'image', 'alt_text', 'is_active', 'ip', 'created_at']
        read_only_fields = ['user', 'ip']
