from winsdk.windows.ui.notifications import UserNotification
from katosc import KatOsc
from pythonosc.udp_client import SimpleUDPClient
from threading import Thread
import time
import osc_parameters


class DiscordBand:
    def __init__(self, osc_client: SimpleUDPClient, kat_text: KatOsc):
        self.osc_client = osc_client
        self.is_enabled = False
        self.is_disposing = False
        self.disable_timer = 0
        self.versions = ["Discord", "Discord Canary", "Discord PTB"]
        self.kat_text = kat_text
        self.last_seen_message: dict[str, str] = None
        self.thread = Thread(target=self.run)
        self.thread.start()

    def handle_display_notification(self) -> None:
        if self.last_seen_message == None:
            return print("No message found")
        self.kat_text.set_text(
            f'{self.last_seen_message["username"]}: {self.last_seen_message["message"]}')

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

    def store_message(self, notification: UserNotification) -> bool:
        try:
            binding = notification.notification.visual.get_binding(
                "ToastGeneric")
            elements = binding.get_text_elements()
            if elements.size != 2:
                return
            username = elements.get_at(0)
            message = elements.get_at(1)
            if username is None or message is None:
                return
            if username.text == "" or message.text == "":
                return
            self.last_seen_message = {
                "username": username.text,
                "message": message.text
            }
        except:
            pass

    def is_discord_notification(self, notification: UserNotification) -> bool:
        try:
            if hasattr(notification, "app_info"):
                app_name = notification.app_info.display_info.display_name
                if app_name in self.versions:
                    print(f'Notification from {app_name}')
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
