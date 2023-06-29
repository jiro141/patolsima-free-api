from rest_framework import serializers


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        pass
