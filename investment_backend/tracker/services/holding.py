from decimal import Decimal

from tracker.models import Holding


class HoldingService:
    """
    Business logic related to Holdings.
    """

    @staticmethod
    def get_user_holdings(user):

        return (
            Holding.objects.filter(user=user)
            .select_related("asset")
            .order_by("asset__display_name")
        )

    @staticmethod
    def get_holding(user, asset):

        return Holding.objects.filter(
            user=user,
            asset=asset,
        ).first()

    @staticmethod
    def holding_exists(user, asset):

        return Holding.objects.filter(
            user=user,
            asset=asset,
        ).exists()

    @staticmethod
    def create_holding(
        user,
        asset,
        quantity,
        average_buy_price,
        invested_amount,
    ):

        return Holding.objects.create(
            user=user,
            asset=asset,
            quantity=Decimal(quantity),
            average_buy_price=Decimal(average_buy_price),
            invested_amount=Decimal(invested_amount),
        )

    @staticmethod
    def save_holding(holding):
        """
        Save changes to an existing holding.
        """

        holding.save()

        return holding

    @staticmethod
    def delete_holding(holding):

        holding.delete()
    
    @staticmethod
    def get_holding_by_id(
        holding_id,
        user,
        ):
        """
    Return a holding by ID for a specific user.
    """
        return Holding.objects.get(
            id=holding_id,
            user=user,
        )
