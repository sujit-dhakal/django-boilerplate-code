import re

from django.db.models import Aggregate, CharField, Q
from django.utils.text import slugify
from rest_framework import status
from rest_framework.response import Response


def hyperlink(name, link):
    return '=HYPERLINK("{}", "{}")'.format(link, name)


def index_search(
    search=None,
    split_term_args=None,
    non_split_term_args=None,
):
    """
    Split term args = Fields you'd like to filter for by splitting
    the search parameter
    Non Split term args = Fields you'd like to filter for by the
    exact search parameter
    """
    qset = Q()
    qobject = Q()
    if search:
        if split_term_args:
            for term in search.split():
                for arg in split_term_args:
                    qset.add(
                        Q(**{f"{arg}__icontains": term}),
                        Q.OR,
                    )

        if non_split_term_args:
            for arg in non_split_term_args:
                qobject.add(
                    Q(**{f"{arg}__icontains": search}),
                    Q.OR,
                )
    return qset | qobject


def even_number(number):
    """Returns True if EVEN, returns False if ODD"""
    return True if (((number + 1) % 2) == 1) else False


def is_valid_filename(filename: object) -> object:
    import string

    illegal_chars = (
        string.punctuation.replace("_", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
        .replace(":", "")
        .replace(".", "")
    )
    return not any(char in illegal_chars for char in filename)


def unique_slugify(
    instance,
    value,
    slug_field_name="slug",
    queryset=None,
    slug_separator="-",
):
    """
    Calculates a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug. Chop its length down if we need to.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create a queryset, excluding the current instance.
    if not queryset:
        # pylint: disable=W0212 # Access to a protected member
        # _default_manager of a client class
        queryset = instance.__class__._default_manager.all()
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = "-%s" % next
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[: slug_len - len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = "%s%s" % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator=None):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    if separator == "-" or not separator:
        re_sep = "-"
    else:
        re_sep = "(?:-|%s)" % re.escape(separator)
        value = re.sub("%s+" % re_sep, separator, value)
    return re.sub(r"^%s+|%s+$" % (re_sep, re_sep), "", value)


class GroupConcat(Aggregate):
    function = "GROUP_CONCAT"
    template = "%(function)s(%(distinct)s%(expressions)s%(ordering)s%(separator)s)"  # noqa: E501
    allow_distinct = True

    def __init__(
        self,
        expression,
        distinct=True,
        filter=None,
        ordering=None,
        separator=", ",
        **extra,
    ):
        super(GroupConcat, self).__init__(
            expression,
            distinct=("DISTINCT " if distinct else ""),
            ordering=(" ORDER BY %s" % ordering if ordering is not None else ""),
            separator=' SEPARATOR "%s"' % separator,
            output_field=CharField(),
            filter=filter,
            **extra,
        )


def response_405():
    return Response(
        {"data": "Not Implemented on REST yet."},
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
    )  # modify this when we migrate the create code to REST
