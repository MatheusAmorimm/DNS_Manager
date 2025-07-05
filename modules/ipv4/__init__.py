import ipaddress
import subprocess
from modules.log import log
from time import sleep

def ipv4_isvalid(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False
    
def disable_ipv4():
    log("🔧 Desativando IPv6 em todas as interfaces via PowerShell...")
    try:
        subprocess.run('powershell "Disable-NetAdapterBinding -Name * -ComponentID ms_tcpip -Confirm:$false"', shell=True, check=True)
        log("✅ IPv6 desativado com sucesso em todas as interfaces.")
        sleep(2)
    except subprocess.CalledProcessError as e:
        log(f"❌ Falha ao desativar IPv6. Erro: {e}")
        sleep(2)


def enable_ipv4():
    log("🔧 Ativando IPv4 em todas as interfaces via PowerShell...")
    try:
        subprocess.run('powershell "Enable-NetAdapterBinding -Name * -ComponentID ms_tcpip -Confirm:$false"', shell=True, check=True)
        log("✅ IPv4 ativado com sucesso em todas as interfaces.")
        sleep(2)
    except subprocess.CalledProcessError as e:
        log(f"❌ Falha ao ativar IPv4. Erro: {e}")
        sleep(2)