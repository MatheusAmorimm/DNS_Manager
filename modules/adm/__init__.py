from modules.log import log
import ctypes
from time import sleep

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        log(f"❌ Erro ao verificar privilégios de admin: {e}")
        sleep(2)
        return False