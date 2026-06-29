from tracker.models import Watchlist

from tracker.services.asset import AssetService


class WatchlistService:
    """
    Business logic related to Watchlist.
    """

    @staticmethod
    def get_user_watchlist(user):
        """
        Return all watchlist items for a user.
        """
        return (
            Watchlist.objects.filter(user=user)
            .select_related("asset")
            .order_by("asset__display_name")
        )

    @staticmethod
    def is_asset_in_watchlist(user, asset):
        """
        Check whether an asset already exists in
        the user's watchlist.
        """
        return Watchlist.objects.filter(
            user=user,
            asset=asset,
        ).exists()

    @staticmethod
    def add_asset(user, asset_id):
        """
        Add an asset to the user's watchlist.
        """

        asset = AssetService.get_asset_by_id(asset_id)

        if WatchlistService.is_asset_in_watchlist(
            user=user,
            asset=asset,
        ):
            raise ValueError(
                "Asset already exists in watchlist."
            )

        return Watchlist.objects.create(
            user=user,
            asset=asset,
        )

    @staticmethod
    def remove_asset(user, asset_id):
        """
        Remove an asset from the watchlist.
        """

        asset = AssetService.get_asset_by_id(asset_id)

        watchlist = Watchlist.objects.filter(
            user=user,
            asset=asset,
        ).first()

        if watchlist is None:
            raise ValueError(
                "Asset not found in watchlist."
            )

        watchlist.delete()

    @staticmethod
    def clear_watchlist(user):
        """
        Remove every asset from a user's watchlist.
        """

        Watchlist.objects.filter(
            user=user,
        ).delete()