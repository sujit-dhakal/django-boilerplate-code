import pandas as pd
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ListViewSetMixin(mixins.ListModelMixin, viewsets.GenericViewSet):
    list_success_message = "Fetched successfully"

    def paginate_queryset(self, queryset, view=None):
        if (
            self.paginator is None
            or self.request.query_params.get("no_pagination", "false") == "true"
        ):
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        if isinstance(response.data, dict) and "results" in response.data:
            return Response(
                {
                    "message": self.list_success_message,
                    "count": response.data.get("count"),
                    "next": response.data.get("next"),
                    "previous": response.data.get("previous"),
                    "data": response.data.get("results"),
                },
                status=response.status_code,
            )

        return Response(
            {
                "message": self.list_success_message,
                "data": response.data,
            },
            status=response.status_code,
        )


class UpdateViewSetMixin(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    update_success_message = "Updated successfully"

    def get_request_data(self, request, *args, **kwargs):
        return request.data

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=self.get_request_data(request), partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(
            {"message": self.update_success_message, "data": serializer.data}
        )


class AutocompleteViewSetMixin(viewsets.GenericViewSet):
    autocomplete_fields = ["id", "name"]
    rename_dict = {"stock__symbol": "symbol", "stock__security_name": "name"}

    @action(detail=False, methods=["get"], url_path="autocomplete")
    def autocomplete(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        df = pd.DataFrame(queryset.values(*self.autocomplete_fields))
        df.rename(columns=self.rename_dict, inplace=True)
        return Response({"results": df.to_dict("records")})


class AutocompleteModelViewSetMixin(AutocompleteViewSetMixin, viewsets.ModelViewSet):
    pass


class ListAutoCompleteViewSetMixin(ListViewSetMixin, AutocompleteViewSetMixin):
    pass


class CreateViewSetMixin(mixins.CreateModelMixin, viewsets.GenericViewSet):
    create_success_message = "Created successfully"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": self.create_success_message, "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
