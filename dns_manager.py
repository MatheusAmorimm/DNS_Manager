import subprocess
from datetime import datetime
import os
import ctypes
import ipaddress
from dotenv import load_dotenv

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
        return False
    
def ipv4_isvalid(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def get_connected_interfaces():
    res = subprocess.run("netsh interface show interface", shell=True, capture_output=True, text=True)
    connecteds_interfaces = list()

    for line in res.stdout.splitlines():
        if "Conectado" in line:
            parts = line.split()
            interface_name = parts[-1]
            connecteds_interfaces.append(interface_name)
    
    return connecteds_interfaces

def apply_dns(ip_dns):
    interfaces = get_connected_interfaces()
    if not interfaces:
        log("❌ Nenhuma interface conectada encontrada.")
        return

    for interface in interfaces:
        try:
            log(f"🔧 Aplicando DNS {ip_dns} na interface: {interface}")
            subprocess.run(f'netsh interface ip set dns name="{interface}" static {ip_dns}', shell=True, check=True)
            log(f"✅ DNS aplicado com sucesso na interface {interface}")
        except subprocess.CalledProcessError as e:
            log(f"❌ Falha ao aplicar DNS na interface {interface}. Erro: {e}")
        
def restore_dns():
    interfaces = get_connected_interfaces()
    if not interfaces:
        log("❌ Nenhuma interface conectada encontrada.")
        return
    for interface in interfaces:
        try:
            log(f"🔁 Restaurando DNS automático na interface: {interface}")
            subprocess.run(f'netsh interface ip set dns name="{interface}" source=dhcp', shell=True, check=True)
            log(f"✅ DNS restaurado com sucesso na interface {interface}")
        except subprocess.CalledProcessError as e:
            log(f"❌ Falha ao restaurar DNS na interface {interface}. Erro: {e}")

def disable_ipv6():
    log("🔧 Tentando desativar componentes de túnel do IPv6...")
    commands = {
        "Teredo": "netsh interface teredo set state disable",
        "6to4": "netsh interface 6to4 set state disable",
        "ISATAP": "netsh interface isatap set state disable"
    }
    all_successful = True
    for component, command in commands.items():
        try:
            subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            log(f"✅ Componente {component} do IPv6 desativado com sucesso.")
        except subprocess.CalledProcessError as e:
            error_message = e.stdout.strip() if e.stdout.strip() else e.stderr.strip()
            if "O sistema não pode encontrar o arquivo especificado" in error_message:
                 log(f"ℹ️  Componente {component} do IPv6 não encontrado (provavelmente já inativo).")
            else:
                log(f"❌ Falha ao desativar {component}. Erro: {error_message}")
                all_successful = False

    if all_successful:
        log("✅ Operação de desativação de componentes do IPv6 concluída.")

def enable_ipv6():
    log("🔧 Tentando reativar componentes de túnel do IPv6...")
    commands = {
        "Teredo": "netsh interface teredo set state default",
        "6to4": "netsh interface 6to4 set state default",
        "ISATAP": "netsh interface isatap set state default"
    }
    all_successful = True
    for component, command in commands.items():
        try:
            subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            log(f"✅ Componente {component} do IPv6 restaurado para o padrão.")
        except subprocess.CalledProcessError as e:
            error_message = e.stdout.strip() if e.stdout.strip() else e.stderr.strip()
            log(f"❌ Falha ao reativar {component}. Erro: {error_message}")
            all_successful = False
            
    if all_successful:
        log("✅ Operação de reativação de componentes do IPv6 concluída.")

def menu():
    if not is_admin():
        print("⚠️ Este programa deve ser executado como administrador!")
        log("❌ Programa iniciado sem privilégios de administrador.")
        return
    
    while True:
        print("\n===== SISTEMA DE GERENCIAMENTO DE DNS =====")
        print("[1] - Aplicar DNS personalizado (ex: Pi-hole)")
        print("[2] - Restaurar DNS automático")
        print("[3] - Visualizar log")
        print("[4] - Sair")
        choice = int(input("Escolha uma opção: "))

        while choice != 1 and choice != 2 and choice != 3 and choice != 4:
            print("Opção Inválida! Tente novamente: ")
            choice = int(input("Escolha uma opção: "))
        
        if choice == 1:
            ip_dns = input("Digite o IP do servidor DNS: ")
            if not ipv4_isvalid(ip_dns):
                print("❌ IP inválido. Tente novamente.")
                continue
            user_confirm = str(input("Confirmar aplicação do DNS {ip_dns} em todas as interfaces conectadas? [S/N]")).strip().upper()
            if user_confirm == "S":
               apply_dns(ip_dns)
            else:
                print("❌ Operação cancelada.")
        elif choice == 2:
            user_confirm = str(input("⚠️ Confirmar restauração do DNS automático em todas interfaces? [S/N]")).strip().upper()
            if user_confirm == "S":
                restore_dns()
            else:
                print("❌ Operação cancelada.")
        elif choice == 3:
            if os.path.exists(log_file):
                try:
                    with open(log_file, "r", encoding="utf-8") as f:
                        print("\n=== LOGS DE EXECUÇÃO ===")
                        print(f.read())
                except Exception as e:
                    log(f"Não foi possível ler o arquivo de log: {e}")
            else:
                print("Nenhum log encontrado.")
        elif choice == 4:
            print("Saindo...")
            break

if __name__ == "__main__":
    menu()