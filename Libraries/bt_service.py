# ==============================================================================
# MÓDULO BLE UART PARA ESP32 (MicroPython)
# Permite comunicación serial inalámbrica a través de Bluetooth Low Energy (BLE).
# Compatible con aplicaciones móviles como Adafruit Bluefruit o Serial Bluetooth Terminal.
# ==============================================================================

import bluetooth
import io
import os
import micropython
import machine
from micropython import const
import struct
import time
from machine import Pin

# Configuración del pin indicador de conexión física (LED o pin de estado)
pbt = Pin(2, Pin.OUT)
pbt.off() 

# Constantes para la gestión de eventos de interrupción (IRQ) del Bluetooth
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

# Indicadores de permisos para las características de BLE
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

# Definición de UUIDs estándar para el perfil Nordic UART Service (NUS)
_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)

_ADV_APPEARANCE_GENERIC_COMPUTER = const(128)


class BLEUART:
    """Clase principal para gestionar la conexión UART por Bluetooth Low Energy."""
    
    def __init__(self, ble, name, rxbuf=1000):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        
        # Registrar los servicios GATT de UART en la pila Bluetooth
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((_UART_SERVICE,))
        
        # Ampliar el tamaño del búfer de recepción y activar el modo de adjuntar datos
        self._ble.gatts_set_buffer(self._rx_handle, rxbuf, True)
        
        self._connections = set()
        self._rx_buffer = bytearray()
        self._handler = None
        
        # Generar el paquete de publicidad (nombre visible del dispositivo)
        self._payload = advertising_payload(
            name=name, appearance=_ADV_APPEARANCE_GENERIC_COMPUTER)
        self._advertise()

    def irq(self, handler):
        """Asigna la función que se ejecutará al recibir datos."""
        self._handler = handler

    def _irq(self, event, data):
        """Controlador de eventos (interrupciones) de la conexión BLE."""
        # Detectar cuando un teléfono u otro dispositivo se conecta
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("Dispositivo Bluetooth Conectado")
            pbt.on() # Enciende el indicador físico
            self._connections.add(conn_handle)
            
        # Detectar cuando se pierde la conexión
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            pbt.off() # Apaga el indicador físico
            print('Dispositivo Bluetooth Desconectado')
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            # Volver a iniciar la publicidad para permitir nuevas conexiones
            self._advertise()
            
        # Detectar cuando el teléfono envía datos hacia el ESP32
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            if conn_handle in self._connections and value_handle == self._rx_handle:
                self._rx_buffer += self._ble.gatts_read(self._rx_handle)
                if self._handler:
                    self._handler()

    def any(self):
        """Devuelve la cantidad de bytes pendientes por leer en el búfer."""
        return len(self._rx_buffer)

    def read(self, sz=None):
        """Lee los datos almacenados en el búfer de recepción."""
        if not sz:
            sz = len(self._rx_buffer)
        result = self._rx_buffer[0:sz]
        self._rx_buffer = self._rx_buffer[sz:]
        return result

    def write(self, data):
        """Envía datos (texto o bytes) de regreso hacia el teléfono."""
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx_handle, data)

    def close(self):
        """Cierra todas las conexiones activas."""
        for conn_handle in self._connections:
            self._ble.gap_disconnect(conn_handle)
        self._connections.clear()

    def _advertise(self, interval_us=500000):
        """Inicia el proceso de difusión (Advertising) para ser visible en el celular."""
        self._ble.gap_advertise(interval_us, adv_data=self._payload)


# Constantes para la estructura de los paquetes de publicidad (Advertising Payloads)
_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)


def advertising_payload(limited_disc=False, br_edr=False, name=None, services=None, appearance=0):
    """Genera la estructura de datos que se empaqueta en la señal de Bluetooth."""
    payload = bytearray()

    def _append(adv_type, value):
        nonlocal payload
        payload += struct.pack("BB", len(value) + 1, adv_type) + value

    _append(
        _ADV_TYPE_FLAGS,
        struct.pack("B", (0x01 if limited_disc else 0x02) +
                         (0x18 if br_edr else 0x04)),
    )

    if name:
        _append(_ADV_TYPE_NAME, name)

    if services:
        for uuid in services:
            b = bytes(uuid)
            if len(b) == 2:
                _append(_ADV_TYPE_UUID16_COMPLETE, b)
            elif len(b) == 4:
                _append(_ADV_TYPE_UUID32_COMPLETE, b)
            elif len(b) == 16:
                _append(_ADV_TYPE_UUID128_COMPLETE, b)

    if appearance:
        _append(_ADV_TYPE_APPEARANCE, struct.pack("<h", appearance))

    return payload


def demo():
    """Función de prueba local para el módulo."""
    print("Módulo bt_service cargado correctamente")  


if __name__ == "__main__":
    demo()