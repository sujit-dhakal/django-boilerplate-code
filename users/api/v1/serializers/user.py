from core.serializers import DynamicFieldsModelSerializer
from users.models import CustomUser


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "uuid",
            "first_name",
            "last_name",
            "contact",
            "email",
            "is_admin"
        ]