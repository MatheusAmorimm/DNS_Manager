from modules.log import log
from time import sleep
import subprocess


def disable_ipv6():
    log("🔧 Desativando IPv6 em todas as interfaces via PowerShell...")
    try:
        subprocess.run('powershell "Disable-NetAdapterBinding -Name * -ComponentID ms_tcpip6 -Confirm:$false"', shell=True, check=True)
        log("✅ IPv6 desativado com sucesso em todas as interfaces.")
        sleep(2)
    except subprocess.CalledProcessError as e:
        log(f"❌ Falha ao desativar IPv6. Erro: {e}")
        sleep(2)


def enable_ipv6():
    log("🔧 Ativando IPv6 em todas as interfaces via PowerShell...")
    try:
        subprocess.run('powershell "Enable-NetAdapterBinding -Name * -ComponentID ms_tcpip6 -Confirm:$false"', shell=True, check=True)
        log("✅ IPv6 ativado com sucesso em todas as interfaces.")
        sleep(2)
    except subprocess.CalledProcessError as e:
        log(f"❌ Falha ao ativar IPv6. Erro: {e}")
        sleep(2)