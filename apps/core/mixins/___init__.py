# from .context import BaseContextMixin, ObjectContextMixin
# from .form import FormContextMixin
# from .table import BaseListViewMixin
# from .viewtypes import ListMixin, FormViewMixin
# from .mixins import ListViewMixin
from .url import AutoContextMixin

__all__ = [
    #     'BaseContextMixin',
    #     'ObjectContextMixin',
    #     'FormContextMixin',
    #     'BaseListViewMixin',
    AutoContextMixin,
    #     'FormViewMixin',
    #     ListViewMixin,
]

"""
| ファイル名          | 内容（Mixin名の例）                                                    |
| -------------- | --------------------------------------------------------------- |
| `context.py`   | `BaseContextMixin`, `ObjectContextMixin`, `get_page_title()` など |
| `form.py`      | `FormContextMixin`, `FormLabelMixin`, `get_submit_label()` など   |
| `table.py`     | `BaseListViewMixin`, `get_table_headers()`, `get_table_rows()`  |
| `url.py`       | `AutoContextMixin`, `namespaced_url()`, `get_namespace()`       |
| `viewtypes.py` | `ListMixin`, `DetailMixin`, `FormViewMixin` などまとめた統合用           |
"""
