"""
Aplicación de gestión de torneos de fútbol con reloj digital integrado
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from views.tournament_window import TournamentWindow
from views.digital_clock_widget import DigitalClockWidget
from controllers.tournament_controller import TournamentController


def main():
    """Función principal"""
    app = QApplication(sys.argv)
    
    # Establecer información de la organización para QSettings
    app.setOrganizationName("TournamentManager")
    app.setApplicationName("FootballTournament")
    
    # Crear la ventana principal
    tournament_window = TournamentWindow()
    
    # Crear el widget del reloj
    clock_widget = DigitalClockWidget()
    
    # Añadir el reloj a la ventana
    tournament_window.add_clock_widget(clock_widget)
    
    # Crear el controlador
    controller = TournamentController(tournament_window, clock_widget, app)
    
    # Mostrar la ventana
    tournament_window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
