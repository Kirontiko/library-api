from django.utils import timezone


class PerformCreateBorrowingService:
    ACTION_CREATE = "create"
    ACTION_PARTIAL_UPDATE = "partial_update"

    def __init__(self, serializer, book, action, user):
        self.serializer = serializer
        self.book = book
        self.action = action
        self.user = user

    def perform(self):
        self.handle_action()
        self.book.save()
        self.serializer.save(user=self.user)

    def handle_action(self):
        if self.action == PerformCreateBorrowingService.ACTION_CREATE:
            self.__action_create()
        else:
            self.__action_partial_update()

    def __action_create(self):
        self.book -= 1

    def __action_partial_update(self):
        self.book += 1
        self.serializer.is_active = False
        self.serializer.actual_return_date = timezone.now()
