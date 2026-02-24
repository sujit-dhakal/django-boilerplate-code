from decouple import config
from rest_framework.pagination import LimitOffsetPagination

env = config("ENV", default="dev", cast=str)
if env == "dev":
    schema = "http://"
else:
    schema = "https://"


class CustomPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data["next"] = (
            response.data["next"].replace("http://", schema)
            if response.data["next"]
            else None
        )
        response.data["previous"] = (
            response.data["previous"].replace("http://", schema)
            if response.data["previous"]
            else None
        )
        return response
