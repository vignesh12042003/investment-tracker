from rest_framework import status
from rest_framework.generics import GenericAPIView

from tracker.serializers.watchlist import (
    WatchlistSerializer,
    WatchlistWriteSerializer,
)
from tracker.services.watchlist import WatchlistService
from tracker.utils.api_response import (
    success_response,
)


class WatchlistAPIView(GenericAPIView):
    """
    Watchlist APIs.
    """

    lookup_field = "id"

    # ---------------------------------------------------------
    # GET
    # ---------------------------------------------------------

    def get(self, request):
        """
        Return the user's watchlist.
        """

        watchlist = WatchlistService.get_user_watchlist(
            request.user,
        )

        serializer = WatchlistSerializer(
            watchlist,
            many=True,
        )

        return success_response(
            data=serializer.data,
            message="Watchlist retrieved successfully.",
        )

    # ---------------------------------------------------------
    # POST
    # ---------------------------------------------------------

    def post(self, request):
        """
        Add an asset to the watchlist.
        """

        serializer = WatchlistWriteSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        watchlist = WatchlistService.add_asset(
            user=request.user,
            asset_id=serializer.validated_data["asset"].id,
        )

        return success_response(
            data=WatchlistSerializer(watchlist).data,
            message="Asset added to watchlist.",
            status_code=status.HTTP_201_CREATED,
        )

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    def delete(self, request):
        """
        Remove an asset from the watchlist.
        """

        serializer = WatchlistWriteSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        WatchlistService.remove_asset(
            user=request.user,
            asset_id=serializer.validated_data["asset"].id,
        )

        return success_response(
            data=None,
            message="Asset removed from watchlist.",
            status_code=status.HTTP_204_NO_CONTENT,
        )