from rest_framework import serializers


class GenreSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=127)
