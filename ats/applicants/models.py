from django.db import models
from django.db.models import Case, When, Value, IntegerField, Sum
from django.db.models.functions import Lower, Coalesce
from functools import reduce


class Candidates(models.Model):
    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]
    name = models.CharField(max_length=255, null=False, blank=False)
    age = models.PositiveIntegerField(null=False, blank=False)
    gender = models.CharField(
        max_length=8, choices=GENDER_CHOICES, null=False, blank=False
    )
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)

    class Meta:
        db_table = "candidate"

    @classmethod
    def get_candidates(cls, search_text=None):
        qs = cls.objects.all()
        if search_text:
            # sorting by relevance
            query_words = search_text.strip().split()
            relevance_cases = [
                Case(
                    When(name__icontains=word, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
                for word in query_words
            ]
            qs = (
                qs.annotate(
                    relevance_score=reduce(lambda x, y: x + y, relevance_cases),
                    lower_name=Lower("name"),
                )
                .filter(relevance_score__gt=0)
                .order_by("-relevance_score", "lower_name")
            )

        return qs

    @classmethod
    def get_applicant(cls, candidate_id):
        return cls.objects.get(id=candidate_id)
