import asyncio
from pythonosc.udp_client import SimpleUDPClient
from winsdk.windows.ui.notifications.management import UserNotificationListener, UserNotificationListenerAccessStatus
from winsdk.windows.foundation.metadata import ApiInformation


def handler(client: SimpleUDPClient):
    def closure(listener, event):
        notification = listener.get_notification(event.user_notification_id)
        if hasattr(notification, "app_info"):
            app_name = notification.app_info.display_info.display_name
            if app_name == "Discord":
                # dispatch to vrchat
                client.send_message("/avatar/parameters/osc_discord_band", True)
    return closure


async def init():
    if not ApiInformation.is_type_present("Windows.UI.Notifications.Management.UserNotificationListener"):
        print("UserNotificationListener is not supported on this device.")
        exit()

    listener = UserNotificationListener.get_current()
    accessStatus = await listener.request_access_async()

    if accessStatus != UserNotificationListenerAccessStatus.ALLOWED:
        print("Access to UserNotificationListener is not allowed.")
        exit()

    osc_client = SimpleUDPClient("https://127.0.0.0", 9000)
    listener.add_notification_changed(handler(osc_client))


asyncio.run(init())
input('Press Enter to exit')
