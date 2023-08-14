class FilteringBorrowingService:
    ALLOWED_FILTERS = {
        "staff": ("user_id", ),
        "customer": ("is_active", )
    }
    ALLOWED_ACTION = "list"

    def __init__(
            self,
            queryset,
            filters,
            is_user_staff
    ):
        self.queryset = queryset
        self.filters = filters
        self.is_user_staff = is_user_staff

    def perform(self):
        if self.__is_filters_allowed():
            return self.queryset.filter(**self.filters)

    @classmethod
    def is_action_valid(cls, action):
        return cls.ALLOWED_ACTION == action

    def __is_filters_allowed(self):
        for filters_key in self.filters:
            if filters_key not in FilteringBorrowingService.ALLOWED_FILTERS[self.__handle_permissions()]:
                return False
        return True

    def __handle_permissions(self):
        return "staff" if self.is_user_staff else "customer"
