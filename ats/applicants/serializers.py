from rest_framework import serializers
from django.urls import reverse
from .models import Candidates


class AddApplicant(serializers.ModelSerializer):
    class Meta:
        model = Candidates
        fields = "__all__"


class DisplayApplicant(serializers.ModelSerializer):
    rv_score = serializers.IntegerField(source="relevance_score", required=False)
    delete_applicant_url = serializers.SerializerMethodField()

    class Meta:
        model = Candidates
        fields = "__all__"

    def get_delete_applicant_url(self, obj):
        return reverse("applicant-remove_applicant", kwargs={"candidate_id": obj.id})
