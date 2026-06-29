from rest_framework.generics import GenericAPIView

from tracker.utils.api_response import success_response


class DashboardAPIView(GenericAPIView):
    """
    Dashboard API.

    Will be implemented after all backend
    APIs are completed.
    """

    def get(self, request):
        return success_response(
            data={},
            message="Dashboard API is under development.",
        )