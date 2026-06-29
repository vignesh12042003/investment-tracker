from rest_framework.generics import GenericAPIView

from tracker.models import Holding
from tracker.serializers.holding import HoldingSerializer
from tracker.services.holding import HoldingService
from tracker.utils.api_response import (
    success_response,
)


class HoldingAPIView(GenericAPIView):
    """
    Holding APIs.

    Holdings are automatically managed by
    TransactionService.

    Only GET operations are allowed.
    """

    serializer_class = HoldingSerializer
    lookup_field = "id"

    # ---------------------------------------------------------
    # GET
    # ---------------------------------------------------------

    def get(self, request, id=None):
        """
        List all holdings or retrieve a single holding.
        """

        if id is None:

            holdings = HoldingService.get_user_holdings(
                request.user,
            )

            serializer = HoldingSerializer(
                holdings,
                many=True,
            )

            return success_response(
                data=serializer.data,
                message="Holdings retrieved successfully.",
            )

        holding = Holding.objects.get(
            id=id,
            user=request.user,
        )

        serializer = HoldingSerializer(
            holding,
        )

        return success_response(
            data=serializer.data,
            message="Holding retrieved successfully.",
        )