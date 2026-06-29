from rest_framework import status
from rest_framework.generics import GenericAPIView

from tracker.serializers.wallet import (
    WalletSerializer,
    WalletWriteSerializer,
)
from tracker.services.wallet import WalletService
from tracker.utils.api_response import (
    success_response,
    error_response,
)


class WalletAPIView(GenericAPIView):
    """
    Wallet CRUD API.
    """

    lookup_field = "id"

    def get_serializer_class(self):
        """
        Return serializer based on request method.
        """

        if self.request.method in (
            "POST",
            "PUT",
            "PATCH",
        ):
            return WalletWriteSerializer

        return WalletSerializer

    # ---------------------------------------------------------
    # GET
    # ---------------------------------------------------------

    def get(self, request, id=None):
        """
        List all wallets or retrieve a single wallet.
        """

        if id is None:

            wallets = WalletService.get_user_wallets(
                request.user
            )

            serializer = WalletSerializer(
                wallets,
                many=True,
            )

            return success_response(
                data=serializer.data,
                message="Wallets retrieved successfully.",
            )

        wallet = WalletService.get_wallet(id)

        serializer = WalletSerializer(wallet)

        return success_response(
            data=serializer.data,
            message="Wallet retrieved successfully.",
        )

    # ---------------------------------------------------------
    # POST
    # ---------------------------------------------------------

    def post(self, request):
        """
        Create a new wallet.
        """

        serializer = WalletWriteSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        wallet = WalletService.create_wallet(
            user=request.user,
            **serializer.validated_data,
        )

        return success_response(
            data=WalletSerializer(wallet).data,
            message="Wallet created successfully.",
            status_code=status.HTTP_201_CREATED,
        )

    # ---------------------------------------------------------
    # PUT
    # ---------------------------------------------------------

    def put(self, request, id):
        """
        Update an existing wallet.
        """

        wallet = WalletService.get_wallet(id)

        serializer = WalletWriteSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        wallet = WalletService.update_wallet(
            wallet,
            **serializer.validated_data,
        )

        return success_response(
            data=WalletSerializer(wallet).data,
            message="Wallet updated successfully.",
        )

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    def delete(self, request, id):
        """
        Soft delete a wallet.
        """

        wallet = WalletService.get_wallet(id)

        WalletService.delete_wallet(wallet)

        return success_response(
            data=None,
            message="Wallet deleted successfully.",
            status_code=status.HTTP_204_NO_CONTENT,
        )