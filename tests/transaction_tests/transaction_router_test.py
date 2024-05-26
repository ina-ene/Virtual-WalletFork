import asyncio
import unittest
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, Mock, MagicMock, create_autospec
from fastapi.testclient import TestClient
from app.main import app
from app.api.auth_service.auth import authenticate_user
from app.api.routes.users.schemas import UserDTO, UpdateUserDTO, UserViewDTO
from app.api.routes.transactions.schemas import TransactionDTO
from app.api.routes.transactions.router import create_draft_transaction


client = TestClient(app)


def fake_transaction():
    return Mock(
        id=2,
        sender_account="test_sender",
        receiver_account="test_receiver",
        amount=11.20,
        category_id=1,
        description="test_description",
        transaction_date=None,
        status="draft",
        is_reccurring=False,
        recurring_interval=None,
        is_flagged=False,
    )


def fake_transaction_dto():
    return TransactionDTO(
        receiver_account="test_receiver",
        amount=11.30,
        category_id=1,
        description="test_description",
    )


Session = sessionmaker()


def fake_db():
    return MagicMock(spec=Session)


def fake_user_view():
    return UserViewDTO(id=1, username="testuser")


class TransactionRouter_Should(unittest.TestCase):

    @patch("app.core.db_dependency.get_db")
    @patch("app.api.routes.transactions.service.create_draft_transaction")
    @patch("app.api.auth_service.auth.get_user_or_raise_401")
    def test_createDraftTransaction_IsSuccessful(
        self, get_user_mock, create_draft_transaction_mock, mock_get_db
    ):
        # Arrange
        get_user_mock.return_value = fake_user_view()
        transaction = fake_transaction_dto()
        create_draft_transaction_mock.return_value = fake_transaction()
        mock_get_db.return_value = fake_db()
        user = fake_user_view()
        db = fake_db()

        # Act
        response = create_draft_transaction(user, transaction, db)

        # Assert
        self.assertEqual(
            response, "You are about to send 11.20 to test_receiver [Draft ID: 2]"
        )


# import unittest
# from unittest.mock import patch, MagicMock
# from fastapi.testclient import TestClient
# from sqlalchemy.orm import Session
# from app.main import app
# from app.api.routes.transactions.schemas import TransactionDTO
# from app.api.routes.users.schemas import UserViewDTO
# from app.api.routes.transactions.router import create_draft_transaction


# client = TestClient(app)


# def fake_transaction():
#     return MagicMock(
#         id=2,
#         sender_account="test_sender",
#         receiver_account="test_receiver",
#         amount=11.20,
#         category_id=1,
#         description="test_description",
#         transaction_date=None,
#         status="draft",
#         is_recurring=False,
#         recurring_interval=None,
#         is_flagged=False,
#     )


# def fake_transaction_dto():
#     return TransactionDTO(
#         receiver_account="test_receiver",
#         amount=11.20,
#         category_id=1,
#         description="test_description",
#     )


# def fake_user_view():
#     return UserViewDTO(id=1, username="testuser")


# class TestTransactionRouter(unittest.TestCase):

#     @patch("app.core.db_dependency.get_db")
#     @patch("app.api.routes.transactions.service.create_draft_transaction")
#     @patch("app.api.auth_service.auth.get_user_or_raise_401")
#     def test_create_draft_transaction_is_successful(
#         self, get_user_mock, create_draft_transaction_mock, mock_get_db
#     ):
#         # Arrange
#         get_user_mock.return_value = fake_user_view()
#         create_draft_transaction_mock.return_value = fake_transaction()
#         mock_get_db.return_value = MagicMock(spec=Session)
#         transaction_dto = fake_transaction_dto()

#         # Act
#         response = client.post(
#             "/transactions/draft",
#             json=transaction_dto.model_dump,
#             headers={"Authorization": "Bearer test_token"},
#         )

#         # Assert
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("You are about to send 11.20 to test_receiver", response.text)


# if __name__ == "__main__":
#     unittest.main()
