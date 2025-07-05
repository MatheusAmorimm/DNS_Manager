from modules.log import log
from modules.interfaces import get_connected_interfaces
from time import sleep
import subprocess


def apply_dns(ip_dns):
    interfaces = get_connected_interfaces()
    if not interfaces:
        log("❌ Nenhuma interface conectada encontrada.")
        sleep(2)
        return

    for interface in interfaces:
        try:
            log(f"🔧 Aplicando DNS {ip_dns} na interface: {interface}")
            cmd = f'netsh interface ip set dns name="{interface}" static {ip_dns}'
            log(f"Executando comando: {cmd}")
            subprocess.run(cmd, shell=True, check=True)
            subprocess.run(f'netsh interface ip set dns name="{interface}" static {ip_dns}', shell=True, check=True)
            log(f"✅ DNS aplicado com sucesso na interface {interface}")
            sleep(2)
        except subprocess.CalledProcessError as e:
            log(f"❌ Falha ao aplicar DNS na interface {interface}. Erro: {e}")
            sleep(2)

def restore_dns():
    interfaces = get_connected_interfaces()
    if not interfaces:
        log("❌ Nenhuma interface conectada encontrada.")
        sleep(2)
        return
    for interface in interfaces:
        try:
            log(f"🔁 Restaurando DNS automático na interface: {interface}")
            subprocess.run(f'netsh interface ip set dns name="{interface}" source=dhcp', shell=True, check=True)
            sleep(2)
            log(f"✅ DNS restaurado com sucesso na interface {interface}")
            sleep(2)
        except subprocess.CalledProcessError as e:
            log(f"❌ Falha ao restaurar DNS na interface {interface}. Erro: {e}")
            sleep(2)