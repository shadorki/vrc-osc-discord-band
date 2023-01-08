import asyncio
from discord_band import DiscordBand
from winsdk.windows.ui.notifications.management import UserNotificationListener, UserNotificationListenerAccessStatus
from winsdk.windows.foundation.metadata import ApiInformation


def handler(discord_band: DiscordBand):
    def closure(listener, event):
        notification = listener.get_notification(event.user_notification_id)
        if hasattr(notification, "app_info"):
            app_name = notification.app_info.display_info.display_name
            if app_name == "Discord":
                discord_band.enable()
    return closure


async def init(discord_band: DiscordBand):
    if not ApiInformation.is_type_present("Windows.UI.Notifications.Management.UserNotificationListener"):
        print("UserNotificationListener is not supported on this device.")
        exit()

    listener = UserNotificationListener.get_current()
    accessStatus = await listener.request_access_async()

    if accessStatus != UserNotificationListenerAccessStatus.ALLOWED:
        print("Access to UserNotificationListener is not allowed.")
        exit()

    listener.add_notification_changed(handler(discord_band))


discord_band = DiscordBand()
try:
    asyncio.run(init(discord_band))
    input("Press Enter to exit\n")
except KeyboardInterrupt:
    print("Shutting Down...")
finally:
    discord_band.dispose()
