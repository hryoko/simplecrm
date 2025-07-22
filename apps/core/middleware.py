from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    """
    全ページ共通のログイン必須ミドルウェア。

    ログインしていないユーザーのアクセスを
    公開されているパス（例: ログインページ、サインアップページ、管理画面ログアウトなど）以外では
    /accounts/login/ にリダイレクトします。

    settings.PUBLIC_PATHS で公開パスを設定可能。

    使い方:
        MIDDLEWARE に 'core.middleware.LoginRequiredMiddleware' を追加するだけ。

    注意:
        - 静的ファイルやメディアファイルのパスはPUBLIC_PATHSに含めること
        - 適宜公開パスを増やすこと
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.public_paths = getattr(settings, 'PUBLIC_PATHS', [])

    def __call__(self, request):
        path = request.path
        if request.user.is_authenticated or any(
            path.startswith(p) for p in self.public_paths
        ):
            return self.get_response(request)
        return redirect(settings.LOGIN_URL)
