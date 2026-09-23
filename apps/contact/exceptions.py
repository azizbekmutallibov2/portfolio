from apps.core.exceptions import ApplicationError


class RateLimitExceeded(ApplicationError):
    pass
