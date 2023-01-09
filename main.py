import asyncio
from discord_band import DiscordBand
from windows import Windows
from winsdk.windows.ui.notifications.management import UserNotificationListener, UserNotificationListenerAccessStatus
from winsdk.windows.foundation.metadata import ApiInformation


def handler(discord_band: DiscordBand):
    def closure(notification):
        if hasattr(notification, "app_info"):
            app_name = notification.app_info.display_info.display_name
            if app_name == "Discord":
                discord_band.enable()
    return closure


async def init(discord_band: DiscordBand, windows: Windows):
    if not ApiInformation.is_type_present("Windows.UI.Notifications.Management.UserNotificationListener"):
        print("UserNotificationListener is not supported on this device.")
        exit()

    listener = UserNotificationListener.get_current()
    accessStatus = await listener.request_access_async()

    if accessStatus != UserNotificationListenerAccessStatus.ALLOWED:
        print("Access to UserNotificationListener is not allowed.")
        exit()

    windows.add_notification_listener(handler(discord_band))
    await windows.run()


discord_band = DiscordBand()
try:
    print("Starting VRC Discord Notifications...")
    windows = Windows()
    asyncio.run(init(discord_band, windows))
except KeyboardInterrupt:
    print("Shutting Down...\n")
except OSError as e:
    print(e)
    input("Caught issue with Windows\n")
finally:
    discord_band.dispose()
