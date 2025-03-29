from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from django.urls import reverse
from django.conf import settings
from rest_framework.permissions import AllowAny
from .models import Candidates
from .serializers import AddApplicant, DisplayApplicant


class ATSHome(viewsets.ViewSet):
    """
    Ats Home route renders the base html
    """
    permission_classes=[AllowAny]

    @action(detail=False, methods=["get"], url_path="home", url_name="ats_home")
    def ats_home(self, request):
        """
        handles adding the applicants
        """
        search_url = reverse("applicant-display_applicant")
        context = {"search_url": search_url}
        template_name = f"{settings.TEMPLATES_DIR}/display_template.html"
        res = render(request, template_name=template_name, context=context)
        return res


class Applicants(viewsets.ViewSet):
    """
    A View set for operations related to applicants
        Create
        Display
        Update
        Delete
        Serach
    """

    permission_classes=[AllowAny]


    @action(
        detail=False,
        methods=["get"],
        url_path="form",
        url_name="add_applicant_form",
    )
    def display_add_form(self, request):
        """
        Renders the add applicant form
        """
        try:
            template_name = f"{settings.TEMPLATES_DIR}/add_applicant.html"
            return render(request, template_name=template_name)
        except Exception as e:
            print(e)

    @action(
        detail=False,
        methods=["get"],
        url_path="form/(?P<candidate_id>\d+)",
        url_name="edit_applicant_form",
    )
    def display_edit_form(self, request, candidate_id):
        """
        Renders the applicant form in the edit mode with prefilled values
        """
        try:
            qs = Candidates.get_applicant(candidate_id=candidate_id)
            applicant = DisplayApplicant(qs)
            context = {
                "applicant": applicant.data,
            }
            template_name = f"{settings.TEMPLATES_DIR}/edit_applicant.html"
            return render(request, template_name=template_name, context=context)
        except Exception as e:
            print(e)

    @action(
        detail=False, methods=["get"], url_path="list", url_name="display_applicant"
    )
    def display_applicants(self, request):
        """
        Renders the list of the applicants , takes the optional query parameter sq which filters the candidates based on names
        """
        try:
            query_params = request.query_params
            qs = Candidates.get_candidates(search_text=query_params.get("sq"))
            applicants = DisplayApplicant(qs, many=True)
            context = {
                "applicants": applicants.data,
            }
            template_name = f"{settings.TEMPLATES_DIR}/candidate_row.html"
            return render(request, template_name=template_name, context=context)
        except Exception as e:
            print(e)

    @action(
        detail=False,
        methods=["delete"],
        url_path="remove/(?P<candidate_id>\d+)",
        url_name="remove_applicant",
    )
    def delete_applicant(self, request, candidate_id):
        """
        Delete's the applicant corresponding to the candidate id
        """
        try:
            Candidates.get_applicant(candidate_id=candidate_id).delete()
            headers = {
                "HX-Trigger": "refresh_list",
            }
            return Response(headers=headers)
        except Exception as e:
            print(e)

    @action(detail=False, methods=["post"], url_path="add", url_name="add_applicant")
    def add_applicant(self, request):
        """
        Creates the new applicant after validating the request data
        """
        try:
            applicant_data = request.data
            add_applicant_serializer = AddApplicant(data=applicant_data)
            if add_applicant_serializer.is_valid(raise_exception=True):
                add_applicant_serializer.save()
            headers = {"HX-Trigger": "refresh_list"}
            return Response(headers=headers)
        except Exception as e:
            print(e)

    @action(
        detail=False,
        methods=["patch"],
        url_path="(?P<candidate_id>\d+)",
        url_name="edit_applicant",
    )
    def edit_candidate(self, request, candidate_id):
        """
        Edits the candidate details for corresponding candidate id
        """
        try:
            # existing applicant
            updated_data = request.data
            qs = Candidates.get_applicant(candidate_id=candidate_id)
            edit_applicant_serializer = AddApplicant(qs, data=updated_data)
            if edit_applicant_serializer.is_valid(raise_exception=True):
                edit_applicant_serializer.save()
            headers = {
                "HX-Trigger": "refresh_list",
            }
            return Response(headers=headers)
        except Exception as e:
            print(e)
