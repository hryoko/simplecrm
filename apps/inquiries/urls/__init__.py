from . import inquiry, reception  # ← 各モジュールを読み込む

app_name = 'inquiries'

urlpatterns = inquiry.urlpatterns + reception.urlpatterns
