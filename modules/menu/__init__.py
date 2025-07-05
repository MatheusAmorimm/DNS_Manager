from modules.log import log, log_file
from modules.adm import is_admin
from modules.ipv4 import ipv4_isvalid
from modules.dns import apply_dns, restore_dns
from modules.ipv6 import enable_ipv6, disable_ipv6
from time import sleep
import os


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