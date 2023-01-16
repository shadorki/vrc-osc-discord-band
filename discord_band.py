from winsdk.windows.ui.notifications import UserNotification
from pythonosc.udp_client import SimpleUDPClient
from threading import Thread
import time
import osc_parameters


class DiscordBand:
    def __init__(self):
        self.osc_client = SimpleUDPClient("127.0.0.1", 9000)
        self.is_enabled = False
        self.is_disposing = False
        self.disable_timer = 0
        self.thread = Thread(target=self.run)
        self.thread.start()
        self.versions = ["Discord", "Discord Canary", "Discord PTB"]

    def is_call_notification(self, notification: UserNotification) -> bool:
        try:
            binding = notification.notification.visual.get_binding(
                "ToastGeneric")
            if binding is None:
                return False
            elements = binding.get_text_elements()
            if elements is None:
                return False
            if elements.size != 2:
                return False
            username = elements.get_at(0)
            message = elements.get_at(1)
            expected = f'{username.text} started a call.'
            return message.text == expected
        except AttributeError:
            return False

    def is_discord_notification(self, notification: UserNotification) -> bool:
        try:
            if hasattr(notification, "app_info"):
                app_name = notification.app_info.display_info.display_name
                if app_name in self.versions:
                    print('Notification from {app_name}')
                    return True
            return False
        except AttributeError:
            return False

    def run(self) -> None:
        while True:
            if self.is_disposing:
                return
            if self.should_disable():
                self.disable()
            self.disable_timer -= 1
            time.sleep(1)

    def dispose(self) -> None:
        self.is_disposing = True
        self.thread.join()

    def enable_band_notification(self) -> None:
        print("Enabling band notification")
        self.osc_client.send_message(osc_parameters.DISCORD_BAND, True)
        self.is_enabled = True
        self.disable_timer = 5

    def enable_call_notification(self) -> None:
        print("Enabling call notification")
        # Forcibly disabling the band notification because call takes higher priority
        self.osc_client.send_message(osc_parameters.DISCORD_BAND, False)
        self.osc_client.send_message(osc_parameters.DISCORD_CALL, True)
        self.is_enabled = True
        self.disable_timer = 5

    def disable(self) -> None:
        print("Disabling discord notifications")
        self.osc_client.send_message(osc_parameters.DISCORD_BAND, False)
        self.osc_client.send_message(osc_parameters.DISCORD_CALL, False)
        self.is_enabled = False
        self.disable_timer = 0

    def should_disable(self) -> bool:
        return self.is_enabled and self.disable_timer <= 0
