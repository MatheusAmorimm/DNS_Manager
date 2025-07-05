import subprocess
from datetime import datetime
import os
import ctypes
import ipaddress
from dotenv import load_dotenv
from time import sleep

load_dotenv()

log_file = os.getenv("LOG_FILE")

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        log(f"❌ Erro ao verificar privilégios de admin: {e}")
        sleep(2)
        return False
    
def ipv4_isvalid(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


def get_connected_interfaces():
    res = subprocess.run("netsh interface show interface", shell=True, capture_output=True, text=True)
    lines = res.stdout.splitlines()

    connected_interfaces = []

    for line in lines:
        if line.strip().startswith("Admin") or line.strip().startswith("---") or not line.strip():
            continue
        parts = line.strip().split()
        if "Conectado" in parts or "Connected" in parts:
            try:
                # Interface name começa na posição 44 da linha (padrão das colunas netsh)
                interface_name = line[44:].strip()
                log(f"🔎 Interface conectada detectada: '{interface_name}'")
                connected_interfaces.append(interface_name)
            except Exception as e:
                log(f"❌ Erro ao processar linha: '{line}' -> {e}")

    return connected_interfaces

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


def menu():
    if not is_admin():
        print("⚠️ Este programa deve ser executado como administrador!")
        log("❌ Programa iniciado sem privilégios de administrador.")
        sleep(2)
        return
    
    while True:
        print("\n===== SISTEMA DE GERENCIAMENTO DE DNS =====")
        print("[1] - Aplicar DNS personalizado (ex: Pi-hole)")
        print("[2] - Desabilitar o IPv6")
        print("[3] - Ativar o IPv6")
        print("[4] - Restaurar o DNS")
        print("[5] - Visualizar log")
        print("[6] - Sair")
        choice = int(input("Escolha uma opção: "))

        while choice != 1 and choice != 2 and choice != 3 and choice != 4 and choice != 5 and choice != 6:
            print("Opção Inválida! Tente novamente: ")
            sleep(2)
            choice = int(input("Escolha uma opção: "))
        
        if choice == 1:
            ip_dns = input("Digite o IP do servidor DNS: ")
            if not ipv4_isvalid(ip_dns):
                print("❌ IP inválido. Tente novamente.")
                sleep(2)
                continue
            user_confirm = str(input(f"Confirmar aplicação do DNS {ip_dns} em todas as interfaces conectadas? [S/N]: ")).strip().upper()
            if user_confirm == "S":
               apply_dns(ip_dns)
            else:
                print("❌ Operação cancelada.")
                sleep(2)
        elif choice == 2:
            disable_ipv6()
        elif choice == 3:
            enable_ipv6()
        elif choice == 4:
            try:
                user_confirm = str(input("⚠️ Confirmar restauração do DNS automático em todas interfaces? [S/N]")).strip().upper()
                if user_confirm == "S":
                    restore_dns()
                else:
                    print("❌ Operação cancelada.")
                    sleep(2)
            except ValueError:
                while user_confirm != "S" and user_confirm != "N":
                    user_confirm = str(input("⚠️ Confirmar restauração do DNS automático em todas interfaces? [S/N]")).strip().upper()
                    if user_confirm == "S":
                        restore_dns()
                    else:
                        print("❌ Operação cancelada.")
                        sleep(2)

        elif choice == 5:
            if os.path.exists(log_file):
                try:
                    with open(log_file, "r", encoding="utf-8") as f:
                        print("\n=== LOGS DE EXECUÇÃO ===")
                        print(f.read())
                        sleep(2)
                except Exception as e:
                    log(f"Não foi possível ler o arquivo de log: {e}")
                    sleep(2)
            else:
                print("Nenhum log encontrado.")
                sleep(2)
        elif choice == 6:
            print("Saindo...")
            sleep(2)
            break

if __name__ == "__main__":
    menu()