from tracker.models import InvestmentNote
from tracker.services.transaction import TransactionService


class InvestmentNoteService:
    """
    Business logic related to Investment Notes.
    """

    @staticmethod
    def get_user_notes(user):
        """
        Return all investment notes for a user.
        """

        return (
            InvestmentNote.objects.filter(user=user)
            .select_related("transaction", "transaction__asset")
            .order_by("-created_at")
        )

    @staticmethod
    def get_transaction_notes(transaction):
        """
        Return all notes for a transaction.
        """

        return (
            InvestmentNote.objects.filter(
                transaction=transaction,
            )
            .order_by("-created_at")
        )

    @staticmethod
    def get_note(
        *,
        note_id,
        user,
    ):
        return InvestmentNote.objects.get(
        id=note_id,
        user=user,
    )

    @staticmethod
    def create_note(
        *,
        user,
        transaction,
        title,
        note,
    ):
        """
        Create a new investment note.
        """

        return InvestmentNote.objects.create(
            user=user,
            transaction=transaction,
            title=title,
            note=note,
        )

    @staticmethod
    def update_note(
        *,
        investment_note,
        title,
        note,
    ):
        """
        Update an investment note.
        """

        investment_note.title = title
        investment_note.note = note

        investment_note.save(
            update_fields=[
                "title",
                "note",
                "updated_at",
            ]
        )

        return investment_note

    @staticmethod
    def delete_note(
        investment_note,
    ):
        """
        Delete an investment note.
        """

        investment_note.delete()