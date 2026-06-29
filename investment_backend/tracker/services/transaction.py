from decimal import Decimal

from django.db import transaction

from tracker.models import Transaction
from tracker.services.asset import AssetService
from tracker.services.wallet import WalletService
from tracker.services.holding import HoldingService


class TransactionService:
    """
    Handles all Buy and Sell operations.

    Every transaction must go through this service.
    """

    @staticmethod
    @transaction.atomic
    def buy_asset(
        *,
        user,
        asset_id,
        wallet_id,
        quantity,
        price_per_unit,
        transaction_date,
    ):
        """
        Buy an Asset.

        Flow:
            Validate Asset
                ↓
            Validate Wallet
                ↓
            Check Wallet Balance
                ↓
            Create Transaction
                ↓
            Update Wallet
                ↓
            Update Holding
        """

        asset = AssetService.get_asset_by_id(asset_id)
        wallet = WalletService.get_wallet(wallet_id)

        quantity = Decimal(quantity)
        price_per_unit = Decimal(price_per_unit)
        total_amount = quantity * price_per_unit

        if wallet.current_balance < total_amount:
            raise ValueError("Insufficient wallet balance.")

        WalletService.withdraw(
            wallet=wallet,
            amount=total_amount,
        )

        transaction_obj = Transaction.objects.create(
            user=user,
            asset=asset,
            wallet=wallet,
            transaction_type=Transaction.BUY,
            quantity=quantity,
            price_per_unit=price_per_unit,
            total_amount=total_amount,
            transaction_date=transaction_date,
        )

        TransactionService._update_buy_holding(
            user=user,
            asset=asset,
            quantity=quantity,
            price_per_unit=price_per_unit,
            total_amount=total_amount,
        )

        return transaction_obj

    @staticmethod
    def _update_buy_holding(
        *,
        user,
        asset,
        quantity,
        price_per_unit,
        total_amount,
    ):
        """
        Create a new Holding or update an existing Holding
        after a BUY transaction.
        """

        holding = HoldingService.get_holding(
            user=user,
            asset=asset,
        )

        if holding is None:
            HoldingService.create_holding(
                user=user,
                asset=asset,
                quantity=quantity,
                average_buy_price=price_per_unit,
                invested_amount=total_amount,
            )
            return

        previous_quantity = holding.quantity
        previous_investment = holding.invested_amount

        new_quantity = previous_quantity + quantity
        new_investment = previous_investment + total_amount

        holding.quantity = new_quantity
        holding.invested_amount = new_investment
        holding.average_buy_price = new_investment / new_quantity

        HoldingService.save_holding(holding)
