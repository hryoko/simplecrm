from django import template

register = template.Library()


@register.filter
def dict_get(d, key):
    if isinstance(d, dict):
        return d.get(key, '')
    return ''


@register.filter
def dict_display_or_value(d, key):
    """
    - モデルインスタンスの場合: get_<key>_display() があれば呼ぶ
    - dict の場合: そのまま値を返す
    - その他: 空文字
    """
    # モデルインスタンスなら get_<key>_display() チェック
    if hasattr(d, '__class__') and hasattr(d, f'get_{key}_display'):
        return getattr(d, f'get_{key}_display')()

    # 辞書として値を取り出す
    if isinstance(d, dict):
        return d.get(key, '')

    return ''
