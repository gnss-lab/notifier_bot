
import threading
from fast_api import start_api
from main_bot import start_bot


if __name__ == '__main__':
    # Создайте и запустите потоки
    fastapi_thread = threading.Thread(target=start_api)
    telegram_thread = threading.Thread(target=start_bot)
    
    fastapi_thread.start()
    telegram_thread.start()
