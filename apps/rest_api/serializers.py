from rest_framework import serializers


class ExcelSerializer(serializers.Serializer):
    ranking = serializers.CharField(required=True, max_length=4)
    novel = serializers.CharField(required=True)
    author = serializers.CharField(required=True)
    country = serializers.CharField(required=True)
    novel_link = serializers.CharField(required=True)
    author_link = serializers.CharField(required=True)
    country_link = serializers.CharField(required=True)
    index = serializers.CharField(read_only=True)
    details = serializers.CharField(read_only=True)








