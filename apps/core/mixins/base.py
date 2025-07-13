# --- 基礎的・全体に関わるMixin ---
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)


class PageTitleMixin:
    page_title = None

    def get_page_title(self):
        return self.page_title or 'ページ'

    def inject_page_title(self, context):
        context['page_title'] = self.get_page_title()
        return context


class AutoPageTitleMixin(PageTitleMixin):
    action_label = None

    def get_page_title(self):
        if self.page_title:
            return self.page_title
        if getattr(self, 'model', None):
            return f"{self.model._meta.verbose_name}{self.get_action_label()}"
        return super().get_page_title()

    def get_action_label(self):
        if self.action_label:
            return self.action_label

        match self:
            case ListView():
                return '一覧'
            case CreateView():
                return '新規登録'
            case DetailView():
                return '詳細'
            case UpdateView():
                return '編集'
            case DeleteView():
                return '削除'
            case _:
                return ''


class BaseContextMixin(AutoPageTitleMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.inject_page_title(context)

        # from pprint import pprint

        # pprint(context)  # ← これでコンソールに中身出る

        return context
