# --- 基礎的・全体に関わるMixin ---
from django.http import Http404
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)


class SafeObjectMixin:
    # object取得を安全に行う
    def get_object_safe(self):
        """get_object() を安全に実行し、
        存在しない場合は None を返す"""
        try:
            return self.get_object()
        except Http404:
            return None


class PageTitleMixin:
    page_title = None

    def get_page_title(self):
        return self.page_title or 'ページ'

    def inject_page_title(self, context):
        context['page_title'] = self.get_page_title()
        return context


class AutoPageTitleMixin(PageTitleMixin):
    page_title = None
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
