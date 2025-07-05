import subprocess
from modules.log import log

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
                interface_name = line[44:].strip()
                log(f"🔎 Interface conectada detectada: '{interface_name}'")
                connected_interfaces.append(interface_name)
            except Exception as e:
                log(f"❌ Erro ao processar linha: '{line}' -> {e}")
    
    return connected_interfaces