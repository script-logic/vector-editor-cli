from collections.abc import Callable

from .interfaces import BaseLoggerFactory


def register_in[T](
    registry: type[BaseLoggerFactory[T]], name: str
) -> Callable[..., type[T]]:
    def decorator(cls: type[T]) -> type[T]:
        registry().register(name, cls)
        return cls

    return decorator
