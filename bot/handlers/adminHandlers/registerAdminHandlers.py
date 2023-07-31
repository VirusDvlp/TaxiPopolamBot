from .mailingHandlers import register_mailing_hadnlers
from .mainAdminHandlers import register_main_admin_handlers
from .editPointsHandlers import register_points_config_handlers
from .printStatHandlers import register_stat_handlers

def register_admin_handlers(dp) -> None:
    register_mailing_hadnlers(dp)
    register_main_admin_handlers(dp)
    register_points_config_handlers(dp)
    register_stat_handlers(dp)
    