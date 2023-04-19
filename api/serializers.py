from rest_framework import serializers

from block0.models import Post


class PostModelSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ('title', 'content', 'publication_date', 'author')
        read_only_fields = ('publication_date', 'author')
