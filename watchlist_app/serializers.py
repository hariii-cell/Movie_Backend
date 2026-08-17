from rest_framework import serializers

from .models import Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'title', 'type', 'status', 'rating', 'owner']
        read_only_fields = ['id', 'owner']
