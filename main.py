import asyncio
import config
from discord_band import DiscordBand
from windows import Windows
from winsdk.windows.ui.notifications import UserNotification


def handler(discord_band: DiscordBand):
    def closure(notification: UserNotification) -> None:
        if discord_band.is_discord_notification(notification):
            if not discord_band.should_ignore_notification(notification):
                if discord_band.is_call_notification(notification):
                    discord_band.enable_call_notification()
                else:
                    discord_band.enable_band_notification()
    return closure


async def init(discord_band: DiscordBand, windows: Windows):
    if not await windows.can_read_notifications():
        exit()
    windows.add_notification_listener(handler(discord_band))
    await windows.run()

discord_band = None
try:
    print("Starting VRC Discord Notifications...")
    c = config.get_config()
    port = config.get_port_number(c)
    username_allow_list = config.get_username_allow_list(c)
    discord_band = DiscordBand(port, username_allow_list)
    windows = Windows()
    asyncio.run(init(discord_band, windows))
except KeyboardInterrupt:
    print("Shutting Down...\n")
except OSError as e:
    print(e)
    input("Caught issue with Windows\n")
finally:
    if discord_band != None:
        discord_band.dispose()
