from winsdk.windows.ui.notifications.management import UserNotificationListener, UserNotificationListenerAccessStatus
from winsdk.windows.ui.notifications import NotificationKinds, UserNotification
from winsdk.windows.foundation.metadata import ApiInformation
import time


class Windows:
    def __init__(self):
        self.seen_ids = set()
        self.listeners = []

    async def can_read_notifications(self) -> bool:
        if not ApiInformation.is_type_present("Windows.UI.Notifications.Management.UserNotificationListener"):
            print("UserNotificationListener is not supported on this device.")
            return False

        listener = UserNotificationListener.get_current()
        accessStatus = await listener.request_access_async()

        if accessStatus != UserNotificationListenerAccessStatus.ALLOWED:
            print("Access to UserNotificationListener is not allowed.")
            return False

        return True

    async def run(self) -> None:
        # Call here before loop in order to fill seen_ids
        await self.get_new_notifications()
        while True:
            notifications = await self.get_new_notifications()
            for notification in notifications:
                self.dispatch(notification)
            time.sleep(.3)

    async def get_new_notifications(self) -> list[UserNotification]:
        listener = UserNotificationListener.get_current()
        notifications = await listener.get_notifications_async(NotificationKinds.TOAST)
        new_notifications = []
        for notification in notifications:
            if hasattr(notification, "id"):
                if not notification.id in self.seen_ids:
                    new_notifications.append(notification)
                    self.seen_ids.add(notification.id)
        return new_notifications

    def dispatch(self, notification) -> None:
        for listener in self.listeners:
            listener(notification)

    def add_notification_listener(self, listener) -> None:
        self.listeners.append(listener)
