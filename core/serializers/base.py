from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property
from rest_framework import serializers


class GenericForeignKeyField(serializers.Field):
    def to_representation(self, obj):
        """Serialize the GenericForeignKey to a dict representation."""
        if obj:
            return {
                "type": obj.__class__.__name__,
                "id": obj.id,
                "name": str(obj),
            }
        return None

    def to_internal_value(self, data):
        """Deserialize the GenericForeignKey from the input data."""
        try:
            content_type = ContentType.objects.get(model=data["content_type"].lower())
            instance = content_type.get_object_for_this_type(id=data["id"])
            return {
                "content_type": content_type,
                "object_id": instance.id,
            }
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("Invalid content type.")
        except content_type.model_class().DoesNotExist:
            raise serializers.ValidationError("Invalid object ID.")


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    @cached_property
    def request(self):
        return self.context.get("request")


class DynamicFieldsSerializer(serializers.Serializer):
    """
    A Serializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class DynamicFieldsReadOnlyModelSerializer(DynamicFieldsModelSerializer):
    """
    Use this serializer for Public serializers, where the data is limited and read only.  # noqa: E501
    """

    def create(self, validated_data):
        raise serializers.ValidationError(
            "Read-only serializer does not have write access"
        )

    def update(self, instance, validated_data):
        raise serializers.ValidationError(
            "Read-only serializer does not have write access"
        )


class DummySerializer(serializers.Serializer):
    # Dummy serializer for using when serializer class is
    # needed in ViewSet but actual serializer is not used
    # for maintaining swagger doc

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
