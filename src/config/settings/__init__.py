from config.settings.base import *


PRODUCTION = False


if PRODUCTION:
    from config.settings.production import *
else:
    from config.settings.dev import *
