from rest_framework import status
from rest_framework.generics import GenericAPIView

from tracker.serializers.investment_note import (
    InvestmentNoteSerializer,
    InvestmentNoteWriteSerializer,
)
from tracker.services.investment_note import (
    InvestmentNoteService,
)
from tracker.utils.api_response import success_response


class InvestmentNoteAPIView(GenericAPIView):
    """
    Investment Note APIs.
    """

    lookup_field = "id"

    def get(self, request, id=None):
        """
        List all notes or retrieve a single note.
        """

        if id is None:

            notes = InvestmentNoteService.get_user_notes(
                request.user,
            )

            serializer = InvestmentNoteSerializer(
                notes,
                many=True,
            )

            return success_response(
                data=serializer.data,
                message="Investment notes retrieved successfully.",
            )

        note = InvestmentNoteService.get_note(
            user=request.user,
            note_id=id,
        )

        serializer = InvestmentNoteSerializer(note)

        return success_response(
            data=serializer.data,
            message="Investment note retrieved successfully.",
        )

    def post(self, request):
        """
        Create an investment note.
        """

        serializer = InvestmentNoteWriteSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        note = InvestmentNoteService.create_note(
            user=request.user,
            **serializer.validated_data,
        )

        return success_response(
            data=InvestmentNoteSerializer(note).data,
            message="Investment note created successfully.",
            status_code=status.HTTP_201_CREATED,
        )

    def put(self, request, id):
        """
        Update an investment note.
        """

        serializer = InvestmentNoteWriteSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        note = InvestmentNoteService.update_note(
            user=request.user,
            note_id=id,
            **serializer.validated_data,
        )

        return success_response(
            data=InvestmentNoteSerializer(note).data,
            message="Investment note updated successfully.",
        )

    def delete(self, request, id):
        """
        Delete an investment note.
        """

        InvestmentNoteService.delete_note(
            user=request.user,
            note_id=id,
        )

        return success_response(
            data=None,
            message="Investment note deleted successfully.",
            status_code=status.HTTP_204_NO_CONTENT,
        )