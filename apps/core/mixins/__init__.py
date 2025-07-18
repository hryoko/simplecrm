from .base import (
    AutoPageTitleMixin,
    BaseContextMixin,
    PageTitleFromObjectMixin,
    PageTitleMixin,
)
from .list import ListViewMixin
from .object import DetailFieldsMixin  # ObjectMetaContextMixin,
from .object import ObjectContextMixin, ObjectUrlMixin, SafeObjectMixin
from .urls import AutoNamespaceMixin
from .view import (
    CreateViewMixin,
    DeleteViewMixin,
    DetailViewMixin,
    FormContextMixin,
    UpdateViewMixin,
)

# 必要なら ObjectViewMixin や NavigationMixin も
__all__ = [
    'ListViewMixin',
    'CreateViewMixin',
    'UpdateViewMixin',
    'DeleteViewMixin',
    'DetailViewMixin',
    'BaseContextMixin',
    'PageTitleFromObjectMixin',
]
