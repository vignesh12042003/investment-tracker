from rest_framework import status
from rest_framework.generics import GenericAPIView

from tracker.serializers.goal import (
    GoalSerializer,
    GoalWriteSerializer,
)
from tracker.services.goal import GoalService
from tracker.utils.api_response import success_response


class GoalAPIView(GenericAPIView):
    """
    Goal APIs.
    """

    lookup_field = "id"

    def get(self, request, id=None):
        """
        List all goals or retrieve a single goal.
        """

        if id is None:

            goals = GoalService.get_user_goals(
                request.user,
            )

            serializer = GoalSerializer(
                goals,
                many=True,
            )

            return success_response(
                data=serializer.data,
                message="Goals retrieved successfully.",
            )

        goal = GoalService.get_goal(
            user=request.user,
            goal_id=id,
        )

        serializer = GoalSerializer(goal)

        return success_response(
            data=serializer.data,
            message="Goal retrieved successfully.",
        )

    def post(self, request):
        """
        Create a new goal.
        """

        serializer = GoalWriteSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        goal = GoalService.create_goal(
            user=request.user,
            **serializer.validated_data,
        )

        return success_response(
            data=GoalSerializer(goal).data,
            message="Goal created successfully.",
            status_code=status.HTTP_201_CREATED,
        )

    def put(self, request, id):
        """
        Update an existing goal.
        """

        serializer = GoalWriteSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        goal = GoalService.update_goal(
            user=request.user,
            goal_id=id,
            **serializer.validated_data,
        )

        return success_response(
            data=GoalSerializer(goal).data,
            message="Goal updated successfully.",
        )

    def delete(self, request, id):
        """
        Delete a goal.
        """

        GoalService.delete_goal(
            user=request.user,
            goal_id=id,
        )

        return success_response(
            data=None,
            message="Goal deleted successfully.",
            status_code=status.HTTP_204_NO_CONTENT,
        )