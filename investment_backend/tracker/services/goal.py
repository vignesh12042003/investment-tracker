from tracker.models import Goal


class GoalService:
    """
    Business logic related to investment goals.
    """

    @staticmethod
    def get_user_goals(user):
        """
        Return all goals for a user.
        """

        return Goal.objects.filter(
            user=user
        ).order_by(
            "target_date",
            "title",
        )

    @staticmethod
    def get_active_goals(user):
        """
        Return only active goals.
        """

        return Goal.objects.filter(
            user=user,
            status=Goal.ACTIVE,
        ).order_by(
            "target_date",
        )

    @staticmethod
    def get_goal(goal_id):
        """
        Return a single goal.
        """

        return Goal.objects.get(
            id=goal_id,
        )

    @staticmethod
    def create_goal(
        *,
        user,
        title,
        description,
        target_amount,
        target_date,
    ):
        """
        Create a new investment goal.
        """

        return Goal.objects.create(
            user=user,
            title=title,
            description=description,
            target_amount=target_amount,
            target_date=target_date,
        )

    @staticmethod
    def update_goal(
        *,
        goal,
        title,
        description,
        target_amount,
        target_date,
    ):
        """
        Update an existing goal.
        """

        goal.title = title
        goal.description = description
        goal.target_amount = target_amount
        goal.target_date = target_date

        goal.save()

        return goal

    @staticmethod
    def complete_goal(goal):
        """
        Mark a goal as completed.
        """

        goal.status = Goal.COMPLETED

        goal.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return goal

    @staticmethod
    def cancel_goal(goal):
        """
        Cancel an investment goal.
        """

        goal.status = Goal.CANCELLED

        goal.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return goal

    @staticmethod
    def delete_goal(goal):
        """
        Delete a goal permanently.
        """

        goal.delete()