# ==============================================================================
# MÓDULO DE LÓGICA DE APLICACIÓN (models/app_logic.py)
# Maneja el comportamiento del ESP32 según los comandos recibidos por Bluetooth.
# ==============================================================================

class AppLogic:
    def __init__(self, uart_service):
        self.uart = uart_service

    def procesar_comando(self):
        """Procesa los datos recibidos desde la aplicación móvil."""
        if self.uart.any():
            recibe = self.uart.read().decode().strip()
            print(f"Comando recibido: {recibe}")
            
            # Responder al teléfono
            self.uart.write(f"ESP32 OK -> {recibe}\n")
            
            # ==========================================================
            # ZONA DE TUS FUTUROS PROYECTOS (Agrega aquí tus condiciones)
            # ==========================================================
            if recibe == "TEST":
                self.accion_de_prueba()
            else:
                print("Comando sin acción asignada.")

    def accion_de_prueba(self):
        print("Ejecutando rutina de prueba interna...")