from django.urls import path

from tracker.views import (
    AssetAPIView,
    WalletAPIView,
    HoldingAPIView,
    TransactionAPIView,
    TransactionSellAPIView,
    WatchlistAPIView,
    GoalAPIView,
    InvestmentNoteAPIView,
    DashboardAPIView,
)

app_name = "tracker"

urlpatterns = [

    # ---------------------------------------------------------
    # Dashboard
    # ---------------------------------------------------------

    path(
        "dashboard/",
        DashboardAPIView.as_view(),
        name="dashboard",
    ),

    # ---------------------------------------------------------
    # Assets
    # ---------------------------------------------------------

    path(
        "assets/",
        AssetAPIView.as_view(),
        name="asset-list",
    ),

    path(
        "assets/<uuid:id>/",
        AssetAPIView.as_view(),
        name="asset-detail",
    ),

    # ---------------------------------------------------------
    # Wallets
    # ---------------------------------------------------------

    path(
        "wallets/",
        WalletAPIView.as_view(),
        name="wallet-list",
    ),

    path(
        "wallets/<uuid:id>/",
        WalletAPIView.as_view(),
        name="wallet-detail",
    ),

    # ---------------------------------------------------------
    # Holdings
    # ---------------------------------------------------------

    path(
        "holdings/",
        HoldingAPIView.as_view(),
        name="holding-list",
    ),

    path(
        "holdings/<uuid:id>/",
        HoldingAPIView.as_view(),
        name="holding-detail",
    ),

    # ---------------------------------------------------------
    # Transactions
    # ---------------------------------------------------------

    path(
        "transactions/",
        TransactionAPIView.as_view(),
        name="transaction-list",
    ),

    path(
        "transactions/<uuid:id>/",
        TransactionAPIView.as_view(),
        name="transaction-detail",
    ),

    path(
        "transactions/buy/",
        TransactionAPIView.as_view(),
        name="buy-asset",
    ),

    path(
        "transactions/sell/",
        TransactionSellAPIView.as_view(),
        name="sell-asset",
    ),

    # ---------------------------------------------------------
    # Watchlist
    # ---------------------------------------------------------

    path(
        "watchlist/",
        WatchlistAPIView.as_view(),
        name="watchlist",
    ),

    # ---------------------------------------------------------
    # Goals
    # ---------------------------------------------------------

    path(
        "goals/",
        GoalAPIView.as_view(),
        name="goal-list",
    ),

    path(
        "goals/<uuid:id>/",
        GoalAPIView.as_view(),
        name="goal-detail",
    ),

    # ---------------------------------------------------------
    # Investment Notes
    # ---------------------------------------------------------

    path(
        "notes/",
        InvestmentNoteAPIView.as_view(),
        name="note-list",
    ),

    path(
        "notes/<uuid:id>/",
        InvestmentNoteAPIView.as_view(),
        name="note-detail",
    ),
]