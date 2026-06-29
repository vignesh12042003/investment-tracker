from rest_framework import status
from rest_framework.generics import GenericAPIView

from tracker.models import Transaction
from tracker.serializers.transaction import (
    TransactionSerializer,
    BuyTransactionSerializer,
    SellTransactionSerializer,
)
from tracker.services.transaction import TransactionService
from tracker.utils.api_response import (
    success_response,
)


class TransactionAPIView(GenericAPIView):
    """
    Transaction APIs.

    Supports:
    - List Transactions
    - Retrieve Transaction
    - Buy Asset
    - Sell Asset
    """

    lookup_field = "id"

    # ---------------------------------------------------------
    # GET
    # ---------------------------------------------------------

    def get(self, request, id=None):
        """
        List all transactions or retrieve a single transaction.
        """

        if id is None:

            transactions = (
                Transaction.objects.filter(
                    user=request.user,
                )
                .select_related(
                    "asset",
                    "wallet",
                )
                .order_by(
                    "-transaction_date",
                    "-created_at",
                )
            )

            serializer = TransactionSerializer(
                transactions,
                many=True,
            )

            return success_response(
                data=serializer.data,
                message="Transactions retrieved successfully.",
            )

        transaction = Transaction.objects.get(
            id=id,
            user=request.user,
        )

        serializer = TransactionSerializer(
            transaction,
        )

        return success_response(
            data=serializer.data,
            message="Transaction retrieved successfully.",
        )

    # ---------------------------------------------------------
    # BUY
    # ---------------------------------------------------------

    def post(self, request):
        """
        Buy an asset.
        """

        serializer = BuyTransactionSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        transaction = TransactionService.buy_asset(
            user=request.user,
            asset_id=serializer.validated_data["asset"].id,
            wallet_id=serializer.validated_data["wallet"].id,
            quantity=serializer.validated_data["quantity"],
            price_per_unit=serializer.validated_data["price_per_unit"],
            transaction_date=serializer.validated_data["transaction_date"],
        )

        return success_response(
            data=TransactionSerializer(transaction).data,
            message="Asset purchased successfully.",
            status_code=status.HTTP_201_CREATED,
        )
class TransactionSellAPIView(GenericAPIView):
    """
    Sell Asset API.
    """

    def post(self, request):
        """
        Sell an asset.
        """

        serializer = SellTransactionSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        transaction = TransactionService.sell_asset(
            user=request.user,
            asset_id=serializer.validated_data["asset"].id,
            wallet_id=serializer.validated_data["wallet"].id,
            quantity=serializer.validated_data["quantity"],
            price_per_unit=serializer.validated_data["price_per_unit"],
            transaction_date=serializer.validated_data["transaction_date"],
        )

        return success_response(
            data=TransactionSerializer(transaction).data,
            message="Asset sold successfully.",
            status_code=status.HTTP_201_CREATED,
        )