# ==============================================================================
# SCRIPT PRINCIPAL DE ARRANQUE (main.py)
# Limpio y modular: solo inicializa el sistema y enlaza los módulos.
# ==============================================================================

import sys
import bluetooth

# Añadir las carpetas al path de MicroPython para que encuentre los archivos
sys.path.append('/libraries')
sys.path.append('/models')

# Importar los módulos externos
from bt_service import BLEUART
from controller import AppLogic

# Configuración inicial
NOMBRE_DISPOSITIVO = "Nombre_Bluetooth"
print(f"Iniciando dispositivo: {NOMBRE_DISPOSITIVO}")

# Inicializar Bluetooth y la lógica de la aplicación
ble = bluetooth.BLE()
uart = BLEUART(ble, NOMBRE_DISPOSITIVO)
app = AppLogic(uart)

# Vincular la interrupción de recepción directamente al método del módulo lógico
uart.irq(handler=app.procesar_comando)

print("Sistema listo y modularizado. Esperando conexión...")