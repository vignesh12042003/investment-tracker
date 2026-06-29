from rest_framework import serializers

from tracker.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    Read Serializer
    Used for GET APIs.
    """

    asset_symbol = serializers.CharField(
        source="asset.symbol",
        read_only=True,
    )

    asset_name = serializers.CharField(
        source="asset.display_name",
        read_only=True,
    )

    wallet_name = serializers.CharField(
        source="wallet.wallet_name",
        read_only=True,
    )

    class Meta:
        model = Transaction
        fields = (
            "id",
            "asset",
            "asset_symbol",
            "asset_name",
            "wallet",
            "wallet_name",
            "transaction_type",
            "quantity",
            "price_per_unit",
            "total_amount",
            "transaction_date",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "total_amount",
            "created_at",
            "updated_at",
        )


class BuyTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer used for BUY transactions.
    """

    class Meta:
        model = Transaction
        fields = (
            "asset",
            "wallet",
            "quantity",
            "price_per_unit",
            "transaction_date",
        )

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )
        return value

    def validate_price_per_unit(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )
        return value


class SellTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer used for SELL transactions.
    """

    class Meta:
        model = Transaction
        fields = (
            "asset",
            "wallet",
            "quantity",
            "price_per_unit",
            "transaction_date",
        )

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )
        return value

    def validate_price_per_unit(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )
        return value