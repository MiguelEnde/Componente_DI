"""
Aplicación principal de prueba del componente de reloj digital
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from views.main_window import MainWindow
from views.digital_clock_widget import DigitalClockWidget
from controllers.main_controller import MainWindowController


def main():
    """Función principal"""
    app = QApplication(sys.argv)
    
    # Establecer información de la organización para QSettings
    app.setOrganizationName("DigitalClock")
    app.setApplicationName("DigitalClockTest")
    
    # Crear la ventana principal
    main_window = MainWindow()
    
    # Crear el widget del reloj
    clock_widget = DigitalClockWidget()
    
    # Añadir el reloj a la ventana
    main_window.add_clock_widget(clock_widget)
    
    # Crear el controlador
    controller = MainWindowController(main_window, clock_widget, app)
    
    # Mostrar la ventana
    main_window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
