'''Registration all handlers'''
from .startHandlers import register_start_handlers
from .makeCardHandlers import register_make_card_handlers
from .adminHandlers import register_admin_handlers
from .getTripSucces import register_succes_trip_handlers


def register_all_handlers(dp) -> None:
    register_start_handlers(dp)
    register_make_card_handlers(dp)
    register_admin_handlers(dp)
    register_succes_trip_handlers(dp)