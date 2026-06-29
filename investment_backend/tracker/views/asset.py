from rest_framework import status
from rest_framework.generics import GenericAPIView

from tracker.serializers.asset import (
    AssetSerializer,
    AssetWriteSerializer,
)
from tracker.services.asset import AssetService
from tracker.utils.api_response import (
    success_response,
    error_response,
)


class AssetAPIView(GenericAPIView):
    """
    Asset CRUD API.
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
            return AssetWriteSerializer

        return AssetSerializer

    # ----------------------------------------------------------
    # GET
    # ----------------------------------------------------------

    def get(self, request, id=None):
        """
        List all assets or retrieve a single asset.
        """

        if id is None:

            assets = AssetService.get_all_assets()

            serializer = AssetSerializer(
                assets,
                many=True,
            )

            return success_response(
                data=serializer.data,
                message="Assets retrieved successfully.",
            )

        asset = AssetService.get_asset_by_id(id)

        serializer = AssetSerializer(asset)

        return success_response(
            data=serializer.data,
            message="Asset retrieved successfully.",
        )

    # ----------------------------------------------------------
    # POST
    # ----------------------------------------------------------

    def post(self, request):
        """
        Create a new asset.
        """

        serializer = AssetWriteSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        asset = AssetService.create_asset(
            **serializer.validated_data,
        )

        return success_response(
            data=AssetSerializer(asset).data,
            message="Asset created successfully.",
            status_code=status.HTTP_201_CREATED,
        )

    # ----------------------------------------------------------
    # PUT
    # ----------------------------------------------------------

    def put(self, request, id):
        """
        Update an existing asset.
        """

        asset = AssetService.get_asset_by_id(id)

        serializer = AssetWriteSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        asset = AssetService.update_asset(
            asset,
            **serializer.validated_data,
        )

        return success_response(
            data=AssetSerializer(asset).data,
            message="Asset updated successfully.",
        )

    # ----------------------------------------------------------
    # DELETE
    # ----------------------------------------------------------

    def delete(self, request, id):
        """
        Soft delete an asset.
        """

        asset = AssetService.get_asset_by_id(id)

        AssetService.delete_asset(asset)

        return success_response(
            data=None,
            message="Asset deleted successfully.",
            status_code=status.HTTP_204_NO_CONTENT,
        )