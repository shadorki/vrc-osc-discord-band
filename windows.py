from winsdk.windows.ui.notifications.management import UserNotificationListener
from winsdk.windows.ui.notifications import NotificationKinds
import time

class Windows:
    def __init__(self):
        self.seen_ids = set()
        self.listeners = []

    async def run(self):
        # Call here before loop in order to fill seen_ids
        await self.get_new_notifications()
        while True:
            notifications = await self.get_new_notifications()
            for notification in notifications:
                self.dispatch(notification)
            time.sleep(.3)

    async def get_new_notifications(self):
        listener = UserNotificationListener.get_current()
        notifications = await listener.get_notifications_async(NotificationKinds.TOAST)
        new_notifications = []
        for notification in notifications:
            if hasattr(notification, "id"):
                if not notification.id in self.seen_ids:
                    new_notifications.append(notification)
                    self.seen_ids.add(notification.id)
        return new_notifications

    def dispatch(self, notification):
        for listener in self.listeners:
            listener(notification)

    def add_notification_listener(self, listener):
        self.listeners.append(listener)
