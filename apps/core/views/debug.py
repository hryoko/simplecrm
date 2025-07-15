import pprint

from django.http import HttpResponse
from django.views.generic import TemplateView

from ..mixins.base import BaseContextMixin


class DebugContextView(BaseContextMixin, TemplateView):
    template_name = "core/home.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        pprint.pprint(context)  # コンソール出力
        return HttpResponse("<h1>コンテキストを出力しました（サーバーログ参照）</h1>")
