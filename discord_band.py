from pythonosc.udp_client import SimpleUDPClient
from threading import Thread
import time


class DiscordBand:
    def __init__(self):
        self.osc_client = SimpleUDPClient("127.0.0.1", 9000)
        self.is_enabled = False
        self.is_disposing = False
        self.disable_timer = 0
        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            if self.is_disposing:
                return
            if self.should_disable():
                self.disable()
            self.disable_timer -= 1
            time.sleep(1)

    def dispose(self):
        self.is_disposing = True
        self.thread.join()

    def enable(self):
        print("Enabling")
        self.osc_client.send_message(
            "/avatar/parameters/osc_discord_band", True)
        self.is_enabled = True
        self.disable_timer = 5

    def disable(self):
        print("Disabling")
        self.osc_client.send_message(
            "/avatar/parameters/osc_discord_band", False)
        self.is_enabled = False
        self.disable_timer = 0

    def should_disable(self) -> bool:
        return self.is_enabled and self.disable_timer <= 0
