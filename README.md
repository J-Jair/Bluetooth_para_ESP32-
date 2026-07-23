# Bluetooth para ESP32

¡Bienvenido! En este código encontrarás todo lo necesario para montar un sistema de comunicación inalámbrica modular en tu ESP32 usando MicroPython. 


## 1. ⚡ Descripción

Esta plantilla reutilizable para ESP32 con MicroPython simplifica la comunicación inalámbrica al aislar el protocolo **Bluetooth Low Energy**  mediante el perfil *Nordic UART Service (NUS)*  de la lógica principal del sistema. 

El código opera de forma asíncrona mediante interrupciones (`irq`), evitando bucles de espera y permitiendo una comunicación bidireccional eficiente con tu teléfono móvil.


## 2. 🛠️ Requerimientos de Hardware

Para poner en marcha este proyecto de manera física, se requiere:

*   **Microcontrolador ESP32:** Tarjeta de desarrollo basada en ESP32 con soporte nativo para Bluetooth 4.2 y Wi-Fi.
*   **Cable USB:** Para conectar el ESP32 al ordenador, realizar el flasheo de MicroPython y transferir los archivos del proyecto.
*   **Indicador de Estado (Opcional):** Un LED integrado o externo conectado al **Pin GPIO 2** (el cual viene configurado por defecto en el código para encenderse automáticamente al establecerse una conexión Bluetooth exitosa).

---

## 3. 💻 Requerimientos de Software

*   **Firmware:** MicroPython oficial para ESP32 instalado en la placa.
*   **Entorno de Desarrollo (IDE):** Thonny IDE (Recomendado) o VS Code con la extensión MicroPico.
*   **Librerías requeridas:**
    *   `machine`, `bluetooth`, `utime`, `struct`, `io`, `os`: Vienen nativas en el firmware de MicroPython para ESP32. **No requieren instalación externa**.
    *   `bt_service.py`: Módulo de control de bajo nivel. No es una librería externa ni nativa; se incluye dentro de la carpeta `libraries/` de este repositorio y **es totalmente indispensable, ya que sin este archivo el sistema no puede funcionar**.
*   **Aplicación móvil para control:** *Adafruit Bluefruit Connect* (Disponible gratis en Google Play Store y Apple App Store).

### Aplicación Móvil Requerida

Para visualizar, conectar y enviar datos o comandos por Bluetooth al ESP32, es necesario utilizar una aplicación en el teléfono celular que sea compatible con el perfil estándar **Nordic UART Service (NUS)**:

*   **Serial Bluetooth Terminal (de Kai Morich):** Una herramienta excelente y altamente configurable para Android que permite enviar cadenas de texto y comandos personalizados en formato de terminal serial. Puedes encontrarla en la [Google Play Store para Serial Bluetooth Terminal](https://play.google.com/store/apps/details?id=de.kai_morich.serial_bluetooth_terminal).
*   **Adafruit Bluefruit LE:** Una aplicación multiplataforma (disponible tanto para Android como para iOS) desarrollada por Adafruit que incluye controladores gráficos y modos UART dedicados para depurar conexiones BLE. Está disponible en la [App Store de Apple para iOS](https://apps.apple.com/app/adafruit-bluefruit-le-connect/id930368179) y en la [Google Play Store para Android](https://play.google.com/store/apps/details?id=com.adafruit.bluefruit.le.connect).


## 4. 🚀 Cómo Obtener el Proyecto

Puedes integrar este proyecto a tu entorno local de dos formas:

### Opción 1: Clonar el Repositorio (Recomendado)
Si tienes **Git** instalado en tu computadora, abre la terminal en la carpeta donde deseas guardar el proyecto y ejecuta:

```bash
git clone https://github.com/J-Jair/Bluetooth_para_ESP32-.git
```

### Opción 2: Descarga Directa (Sin Git)
Si no utilizas Git, puedes descargar todo el contenido directamente:
1. Haz clic en el botón verde **"Code"** situado en la parte superior derecha de esta página.
2. Selecciona la opción **"Download ZIP"**.
3. Extrae el archivo `.zip` descargado en tu computadora y abre los archivos `.py` en tu IDE favorito (como Thonny).



## 📲 Configuración de la App Móvil
Para interactuar con el dispositivo de manera correcta, sigue estos pasos en **Adafruit Bluefruit Connect**:
1. Abre la aplicación y activa el Bluetooth en tu smartphone.
2. Busca el dispositivo con el nombre que colocaste en el archivo main, en este caso es **"Nombre_Bluetooth"** y presiona **Connect**.
3. Selecciona el módulo **UART**.
4. **Muy Importante:** Entra a los ajustes de la consola UART en la app y configura el *End of Line* (Fin de línea o EoL) en **CR+LF (`\r\n`)**. Sin esto, el ESP32 no procesará los comandos correctamente.


## 4. 🗂️ Distribución de Carpetas del Proyecto

El repositorio en GitHub debe estructurarse limpiamente respetando la siguiente jerarquía de directorios para que el ESP32 reconozca los módulos de forma portable:

```text
Bluetooth_para_ESP32/
│
├── libraries/
│   └── bt_service.py      # Controlador de bajo nivel.
│
├── models/
│   └── controller.py      # Lógica de negocio y procesamiento de comandos.
│
├── main/
    └── main.py            # Script principal de arranque y orquestación.

```


## 🤝 Colaboración y Aprendizaje

💡 Este repositorio es un proyecto en constante evolución, enfocado en conectar sistemas embebidos como el **ESP32** mediante arquitecturas modulares y comunicación inalámbrica **Bluetooth Low Energy (BLE)** en MicroPython. 

Si encuentras algún detalle por mejorar, tienes una idea o quieres aportar una nueva función para optimizar el código, ¡siempre hay espacio para sumar! Puedes abrir un *Issue* o proponer mejoras. 

## ¡La mejora continua y el rigor técnico son los pilares de la ingeniería! 🤝🛠️