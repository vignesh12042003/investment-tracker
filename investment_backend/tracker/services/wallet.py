from decimal import Decimal

from django.db import transaction

from tracker.models import Wallet


class WalletService:
    """
    Business logic related to Wallets.
    """

    # ==========================================================
    # Read Operations
    # ==========================================================

    @staticmethod
    def get_wallet(wallet_id):
        """
        Return a single active wallet.
        """

        return Wallet.objects.get(
            id=wallet_id,
            is_active=True,
        )

    @staticmethod
    def get_user_wallets(user):
        """
        Return all active wallets for a user.
        """

        return Wallet.objects.filter(
            user=user,
            is_active=True,
        ).order_by(
            "wallet_name"
        )

    # ==========================================================
    # Validation
    # ==========================================================

    @staticmethod
    def wallet_exists(
        user,
        wallet_name,
    ):
        """
        Check whether a wallet already exists
        for the user.
        """

        return Wallet.objects.filter(
            user=user,
            wallet_name__iexact=wallet_name,
            is_active=True,
        ).exists()

    @staticmethod
    def has_sufficient_balance(
        wallet,
        amount,
    ):
        """
        Check whether the wallet has
        sufficient balance.
        """

        amount = Decimal(amount)

        return wallet.current_balance >= amount

    # ==========================================================
    # CRUD Operations
    # ==========================================================

    @staticmethod
    @transaction.atomic
    def create_wallet(
        *,
        user,
        **validated_data,
    ):
        """
        Create a new wallet.
        """

        if WalletService.wallet_exists(
            user=user,
            wallet_name=validated_data["wallet_name"],
        ):
            raise ValueError(
                "Wallet already exists."
            )

        return Wallet.objects.create(
            user=user,
            **validated_data,
        )

    @staticmethod
    @transaction.atomic
    def update_wallet(
        wallet,
        **validated_data,
    ):
        """
        Update an existing wallet.
        """

        for field, value in validated_data.items():
            setattr(
                wallet,
                field,
                value,
            )

        wallet.save(
            update_fields=[
                *validated_data.keys(),
                "updated_at",
            ]
        )

        return wallet

    @staticmethod
    @transaction.atomic
    def delete_wallet(
        wallet,
    ):
        """
        Soft delete a wallet.
        """

        wallet.is_active = False

        wallet.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return wallet

    # ==========================================================
    # Business Operations
    # ==========================================================

    @staticmethod
    @transaction.atomic
    def deposit(
        *,
        wallet,
        amount,
    ):
        """
        Deposit money into a wallet.
        """

        amount = Decimal(amount)

        wallet.current_balance += amount

        wallet.save(
            update_fields=[
                "current_balance",
                "updated_at",
            ]
        )

        return wallet

    @staticmethod
    @transaction.atomic
    def withdraw(
        *,
        wallet,
        amount,
    ):
        """
        Withdraw money from a wallet.
        """

        amount = Decimal(amount)

        if not WalletService.has_sufficient_balance(
            wallet=wallet,
            amount=amount,
        ):
            raise ValueError(
                "Insufficient wallet balance."
            )

        wallet.current_balance -= amount

        wallet.save(
            update_fields=[
                "current_balance",
                "updated_at",
            ]
        )

        return wallet