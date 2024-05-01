from config.settings.base import *


PRODUCTION = True


if PRODUCTION:
    from config.settings.production import *
else:
    from config.settings.dev import *
