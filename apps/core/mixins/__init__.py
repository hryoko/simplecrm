from .base import AutoPageTitleMixin, BaseContextMixin, PageTitleMixin
from .list import ListViewMixin
from .object import (
    DetailFieldsMixin,
    ObjectContextMixin,
    ObjectMetaContextMixin,
    ObjectUrlMixin,
    SafeObjectMixin,
)
from .urls import AutoNamespaceMixin
from .view import CreateViewMixin, DeleteViewMixin, DetailViewMixin, UpdateViewMixin

# 必要なら ObjectViewMixin や NavigationMixin も
__all__ = [
    "ListViewMixin",
    "CreateViewMixin",
    "UpdateViewMixin",
    "DeleteViewMixin",
    "DetailViewMixin",
    "BaseContextMixin",
]
