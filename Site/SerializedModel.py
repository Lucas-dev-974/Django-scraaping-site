from rest_framework import serializers
from Site.models import *

class ThreadReplysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threads_Replys
        fields = "__all__"

class ThreadsSerializer(serializers.ModelSerializer):
    # thread = ThreadReplysSerializer(many=True)

    class Meta:
        model = Threads
        fields = "__all__"