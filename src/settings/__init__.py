from decouple import config

ENV = config("ENV", default="dev", cast=str)
if ENV == "dev":
    from .local import *
elif ENV == "prod":
    from .prod import *
else:
    print("Invalid ENV: %s" % ENV)
