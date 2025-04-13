from typing_extensions import override

from zerver.lib.test_classes import ZulipTestCase


class WelcomeBotCustomMessageTest(ZulipTestCase):
    @override
    def setUp(self) -> None:
        super().setUp()
        self.user_profile = self.example_user("iago")

    def test_welcome_bot_custom_message(self) -> None:
        user = self.example_user("desdemona")
        self.login_user(user)
        welcome_bot_custom_message = "Welcome Bot custom for testing"

        result = self.client_post(
            "/json/realm/test_welcome_bot_custom_message",
            {"welcome_bot_custom_message": welcome_bot_custom_message},
        )
        response_dict = self.assert_json_success(result)
        welcome_bot_message_id = response_dict["message_id"]

        received_welcome_bot_message = self.get_second_to_last_message()
        received_welcome_bot_custom_message = self.get_last_message()

        self.assertEqual(received_welcome_bot_message.sender.email, "welcome-bot@zulip.com")
        self.assertTrue(
            received_welcome_bot_message.content.startswith("Hello, and welcome to Zulip!")
        )
        self.assertEqual(welcome_bot_message_id, received_welcome_bot_message.id)

        self.assertEqual(received_welcome_bot_custom_message.sender.email, "welcome-bot@zulip.com")
        self.assertIn(welcome_bot_custom_message, received_welcome_bot_custom_message.content)
