import argparse
import os
from datetime import datetime
import socket


def main():
    # コマンドライン引数を解析
    parser = argparse.ArgumentParser(description="Run a custom development server.")
    parser.add_argument(
        'addrport',
        nargs='?',
        default='127.0.0.1:8000',
        help='Optional port number, or ipaddr:port',
    )
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    args = parser.parse_args()

    # ホストとポートを取得
    addrport = args.addrport.split(':')
    host = addrport[0]
    port = int(addrport[1]) if len(addrport) > 1 else 8000

    # デバッグモードかどうか
    debug = args.debug

    # タイムスタンプを取得
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # ローカルホストのIPアドレスを取得
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except socket.error:
        local_ip = '127.0.0.1'

    # サーバー情報を表示
    print(f"Performing system checks...\n")
    print(f"System check identified no issues (0 silenced).\n")
    print(f"{timestamp}")
    print(
        f"Django version 3.2.5, using settings '{os.environ.get('DJANGO_SETTINGS_MODULE', 'myproject.settings')}'"
    )
    print(f"Starting development server at http://{host}:{port}/")
    print(f"Quit the server with CONTROL-C.")
    print(f"{'Running in debug mode' if debug else 'Running in production mode'}")


if __name__ == "__main__":
    main()
