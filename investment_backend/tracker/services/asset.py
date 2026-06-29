from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from tracker.models import Asset


class AssetService:
    """
    Business logic related to Assets.
    """

    # ==========================================================
    # Read Operations
    # ==========================================================

    @staticmethod
    def get_all_assets():
        """
        Return all active assets.
        """

        return Asset.objects.filter(
            is_active=True
        ).order_by(
            "display_name"
        )

    @staticmethod
    def get_asset_by_id(asset_id):
        """
        Return a single asset by ID.
        """

        return get_object_or_404(
            Asset,
            id=asset_id,
            is_active=True,
        )

    @staticmethod
    def get_asset_by_symbol(symbol):
        """
        Return asset using its symbol.
        """

        return Asset.objects.get(
            symbol=symbol.upper(),
            is_active=True,
        )

    @staticmethod
    def search_assets(keyword):
        """
        Search assets using symbol or company name.
        """

        return (
            Asset.objects.filter(
                Q(symbol__icontains=keyword)
                | Q(display_name__icontains=keyword),
                is_active=True,
            )
            .order_by("display_name")
        )

    # ==========================================================
    # Validation
    # ==========================================================

    @staticmethod
    def asset_exists(symbol):
        """
        Check whether an asset symbol already exists.
        """

        return Asset.objects.filter(
            symbol=symbol.upper()
        ).exists()

    # ==========================================================
    # CRUD Operations
    # ==========================================================

    @staticmethod
    @transaction.atomic
    def create_asset(**validated_data):
        """
        Create a new Asset.
        """

        if AssetService.asset_exists(
            validated_data["symbol"]
        ):
            raise ValueError(
                "Asset already exists."
            )

        validated_data["symbol"] = (
            validated_data["symbol"].upper()
        )

        return Asset.objects.create(
            **validated_data
        )

    @staticmethod
    @transaction.atomic
    def update_asset(
        asset,
        **validated_data,
    ):
        """
        Update an existing Asset.
        """

        for field, value in validated_data.items():
            setattr(
                asset,
                field,
                value,
            )

        if "symbol" in validated_data:
            asset.symbol = asset.symbol.upper()

        asset.save(
            update_fields=[
                *validated_data.keys(),
                "updated_at",
            ]
)

        return asset

    @staticmethod
    @transaction.atomic
    def delete_asset(asset):
        """
        Soft delete an Asset.
        """

        asset.is_active = False

        asset.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return asset