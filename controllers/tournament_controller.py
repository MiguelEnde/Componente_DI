"""
Controlador de la ventana de gestión de torneos
Gestiona la integración del reloj con los partidos
"""
from PySide6.QtCore import QTranslator
from models.clock_model import ClockMode, TimerMode
from models.tournament_model import TournamentModel
from controllers.clock_controller import DigitalClockController
from translations import translate
import os


class TournamentController:
    """Controlador para la gestión de torneos"""
    
    def __init__(self, view, clock_widget, app):
        self.view = view
        self.clock_widget = clock_widget
        self.app = app
        
        # Conectar el controlador con la vista
        self.view.set_controller(self)
        
        # Modelo del torneo
        self.tournament_model = TournamentModel()
        
        # Crear el controlador del reloj
        from models.clock_model import ClockModel
        self.clock_model = ClockModel()
        self.clock_controller = DigitalClockController(self.clock_model, clock_widget)
        
        # Configurar el reloj en modo reloj (mostrará la hora actual)
        self.clock_controller.set_mode(ClockMode.CLOCK)
        
        # Conectar señales del reloj
        self.clock_widget.timerFinished.connect(self.on_match_time_finished)
        self.clock_widget.timeUpdated.connect(self.on_time_updated)
        
        # Sistema de traducciones
        self.translator = QTranslator()
        self.current_language = 'en'
        
        # Variables para el descanso
        self.break_done = False
        self.half_time = 0
        self.match_duration = 0
    
    def start_match(self):
        """Inicia un nuevo partido"""
        match_data = self.view.get_match_data()
        
        # Validar datos
        if not match_data['team1'] or not match_data['team2']:
            self.view.show_error(
                self.view.tr("Error"),
                self.view.tr("Please enter both team names")
            )
            return
        
        try:
            # Crear el partido
            match = self.tournament_model.create_match(
                match_data['team1'],
                match_data['team2'],
                match_data['duration']
            )
            
            # Iniciar el partido
            self.tournament_model.start_current_match()
            
            # Cambiar el reloj a modo temporizador
            self.clock_controller.set_mode(ClockMode.TIMER)
            self.clock_controller.set_timer_mode(TimerMode.REGRESSIVE)
            
            # Configurar el reloj
            duration_seconds = match_data['duration'] * 60
            self.match_duration = duration_seconds
            self.half_time = duration_seconds // 2
            self.break_done = False
            self.clock_controller.set_timer_duration(duration_seconds)
            self.clock_controller.on_reset()  # Asegurar que esté reseteado
            
            # Iniciar el cronómetro
            self.clock_controller.on_start()
            
            # Actualizar la interfaz
            self.view.set_match_controls_enabled(False, True)
            self.view.update_match_status(
                self.view.tr(f"Match in progress: {match.get_match_info()}")
            )
            self.view.clear_log()
            
            # Añadir eventos al log
            for event in match.events:
                self.view.add_log_entry(event)
            
        except ValueError as e:
            self.view.show_error(self.view.tr("Error"), str(e))
    
    def end_match(self):
        """Finaliza el partido actual"""
        if not self.tournament_model.has_active_match():
            return
        
        # Detener el cronómetro
        self.clock_controller.on_reset()
        
        # Cambiar el reloj de vuelta a modo reloj
        self.clock_controller.set_mode(ClockMode.CLOCK)
        
        # Finalizar el partido
        match = self.tournament_model.current_match
        match.add_event(self.view.tr("Match ended manually"))
        self.tournament_model.end_current_match()
        
        # Resetear variables de descanso
        self.break_done = False
        self.half_time = 0
        self.match_duration = 0
        
        # Actualizar la interfaz
        self.view.set_match_controls_enabled(True, False)
        self.view.update_match_status(self.view.tr("No match in progress"))
        self.view.add_log_entry(match.events[-1])
        
        self.view.show_message(
            self.view.tr("Match Ended"),
            self.view.tr("The match has been ended")
        )
    
    def on_match_time_finished(self):
        """Se llama cuando termina el tiempo del partido"""
        if not self.tournament_model.has_active_match():
            return
        
        match = self.tournament_model.current_match
        match.add_event(self.view.tr("⏱️ Full time! Match duration completed"))
        
        # Finalizar el partido
        self.tournament_model.end_current_match()
        
        # Resetear variables de descanso
        self.break_done = False
        self.half_time = 0
        self.match_duration = 0
        
        # Cambiar el reloj de vuelta a modo reloj
        self.clock_controller.set_mode(ClockMode.CLOCK)
        
        # Actualizar la interfaz
        self.view.set_match_controls_enabled(True, False)
        
        # Añadir al log
        self.view.add_log_entry(match.events[-1])
        
        # Mostrar mensaje
        self.view.show_message(
            self.view.tr("Full Time"),
            self.view.tr(f"The match between {match.team1} and {match.team2} has ended!")
        )
        
        self.view.update_match_status(
            self.view.tr(f"Match finished: {match.get_match_info()}")
        )
    
    def on_time_updated(self, time_str: str):
        """Se llama cada vez que se actualiza el tiempo"""
        if self.clock_controller.model.mode == ClockMode.TIMER and not self.break_done:
            remaining = self.parse_time(time_str)
            if remaining <= self.half_time:
                self.break_done = True
                self.pause_for_break()
    
    def change_language(self, language: str):
        """Cambia el idioma de la aplicación"""
        if language == self.current_language:
            return
        
        self.current_language = language
        
        # Retranslate UI
        self.retranslate_ui()
    
    def retranslate_ui(self):
        """Retraduce toda la interfaz"""
        self.view.retranslateUi(self.current_language)
        self.clock_widget.retranslateUi(self.current_language)
    
    def parse_time(self, time_str: str) -> int:
        """Convierte una cadena de tiempo MM:SS o HH:MM:SS a segundos"""
        parts = time_str.split(':')
        if len(parts) == 2:
            m, s = map(int, parts)
            return m * 60 + s
        elif len(parts) == 3:
            h, m, s = map(int, parts)
            return h * 3600 + m * 60 + s
        return 0
    
    def pause_for_break(self):
        """Pausa el partido para el descanso"""
        self.clock_controller.on_pause()
        self.view.show_notification(self.view.tr("Descanso"))
        
        # Añadir al log
        if self.tournament_model.has_active_match():
            match = self.tournament_model.current_match
            match.add_event(self.view.tr("⏸️ Half-time break"))
            self.view.add_log_entry(match.events[-1])
        
        from PySide6.QtCore import QTimer
        QTimer.singleShot(5000, self.resume_match)
    
    def resume_match(self):
        """Reanuda el partido después del descanso"""
        self.clock_controller.on_pause()  # Resume
        self.view.show_notification(self.view.tr("Second half started"))
        
        # Añadir al log
        if self.tournament_model.has_active_match():
            match = self.tournament_model.current_match
            match.add_event(self.view.tr("▶️ Second half started"))
            self.view.add_log_entry(match.events[-1])
