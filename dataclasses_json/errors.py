import dataclasses
import sys

from dataclasses_json import cfg


@dataclasses.dataclass
class ErrorProcessor:
    on_error: cfg.OnError = cfg.OnError.RAISE
    exceptions: list[Exception] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        assert self.on_error == cfg.OnError.RAISE or sys.version_info >= (3, 11), \
            f"On error {self.on_error} is not supported in Python early 3.11"

    def __bool__(self):
        return bool(self.exceptions)

    def get_group_exception(self, message: str) -> Exception | None:
        assert sys.version_info >= (3, 11), "Group exception is only supported on Python 3.11"
        if not self.exceptions:
            return None
        return ExceptionGroup(message, self.exceptions)

    def add(self, exc: Exception, *notes: str) -> bool:
        """
        Try to add an exception to the list of exceptions with provided notes..
        Usually, if it can not be added, it should be raised.

        :return: True if exception was collected, False otherwise
        """
        if self.on_error == cfg.OnError.RAISE or isinstance(exc, AssertionError):
            return False
        for item in notes:
            exc.add_note(item)
        if self.on_error == cfg.OnError.GROUP_WITH_TRACEBACK_AND_RAISE:
            exc = exc.with_traceback(None)
        self.exceptions.append(exc)
        return True
