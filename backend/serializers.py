from rest_framework import serializers
from .models import Student, Candidate
from django.contrib.auth.hashers import make_password


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["username", "password", "name", "class_name", "is_teacher"]  # Added "is_teacher"

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ["name", "prn", "class_name", "votes"]