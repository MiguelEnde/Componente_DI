"""
Controlador de la ventana principal de prueba
Gestiona la integración del reloj con la ventana de prueba
"""
from PySide6.QtCore import QCoreApplication, QTranslator, QLocale
from models.clock_model import ClockMode, TimerMode
from controllers.clock_controller import DigitalClockController
from translations import translate
import os


class MainWindowController:
    """Controlador para la ventana principal de prueba"""
    
    def __init__(self, view, clock_widget, app):
        self.view = view
        self.clock_widget = clock_widget
        self.app = app
        
        # Conectar el controlador con la vista
        self.view.set_controller(self)
        
        # Crear el controlador del reloj
        from models.clock_model import ClockModel
        self.clock_model = ClockModel()
        self.clock_controller = DigitalClockController(self.clock_model, clock_widget)
        
        # Conectar señales del reloj
        self.clock_widget.alarmTriggered.connect(self.on_alarm_triggered)
        self.clock_widget.timerFinished.connect(self.on_timer_finished)
        self.clock_controller.chronometerPaused.connect(self.on_timer_paused)
        
        # Sistema de traducciones
        self.translator = QTranslator()
        self.current_language = 'en'
        
        # Aplicar configuración inicial
        self.apply_configuration()
    
    def apply_configuration(self):
        """Aplica la configuración desde los controles de la ventana"""
        config = self.view.get_configuration()
        
        # Modo
        if config['mode'] == 0:
            self.clock_controller.set_mode(ClockMode.CLOCK)
            if hasattr(self.view, 'spinTimerDuration'):
                self.view.spinTimerDuration.setEnabled(False)
            if hasattr(self.view, 'lblTimerDuration'):
                self.view.lblTimerDuration.setText(translate("No aplica (reloj)", self.current_language))
        elif config['mode'] == 1:
            self.clock_controller.set_mode(ClockMode.TIMER)
            self.clock_controller.set_timer_mode(TimerMode.REGRESSIVE)
            if hasattr(self.view, 'spinTimerDuration'):
                self.view.spinTimerDuration.setEnabled(True)
            if hasattr(self.view, 'lblTimerDuration'):
                self.view.lblTimerDuration.setText(translate("Timer Duration (sec):", self.current_language))
        elif config['mode'] == 2:
            self.open_tournament()
            if hasattr(self.view, 'spinTimerDuration'):
                self.view.spinTimerDuration.setEnabled(False)
            if hasattr(self.view, 'lblTimerDuration'):
                self.view.lblTimerDuration.setText(translate("No aplica (fútbol)", self.current_language))
            return  # No aplicar otras configuraciones para este modo
        elif config['mode'] == 3:
            self.clock_controller.set_mode(ClockMode.TIMER)
            self.clock_controller.set_timer_mode(TimerMode.PROGRESSIVE)
            self.clock_controller.set_timer_duration(0)  # Sin límite para cronómetro
            self.clock_controller.on_reset()  # Resetear para empezar desde 0
            self.clock_controller.update_display()  # Forzar actualización del display
            # Deshabilitar el spin para cronómetro
            if hasattr(self.view, 'spinTimerDuration'):
                self.view.spinTimerDuration.setEnabled(False)
                self.view.spinTimerDuration.setValue(0)  # Poner 0 para claridad
            if hasattr(self.view, 'lblTimerDuration'):
                self.view.lblTimerDuration.setText(translate("No aplica (cronómetro)", self.current_language))
        
        # Formato
        self.clock_controller.set_format_24h(config['format_24h'])
        
        # Alarma
        alarm_time = config['alarm_time']
        self.clock_controller.set_alarm(
            config['alarm_enabled'],
            alarm_time.hour(),
            alarm_time.minute(),
            config['alarm_message']
        )
        
        # Duración del temporizador
        self.clock_controller.set_timer_duration(config['timer_duration'])
        
        self.view.show_notification(self.view.tr("Configuration applied successfully"))
    
    def on_alarm_triggered(self, message: str):
        """Maneja el evento de alarma"""
        self.view.show_notification(f"⏰ {message}")
        self.view.show_message_box(self.view.tr("Alarm"), message)
    
    def on_timer_finished(self):
        """Maneja el evento de temporizador finalizado"""
        self.view.show_notification(self.view.tr("⏱️ Timer finished!"))
        self.view.show_message_box(
            self.view.tr("Timer"), 
            self.view.tr("The timer has finished!")
        )
    
    def on_timer_paused(self):
        """Maneja cuando se pausa el temporizador"""
        if self.clock_controller.model.timer_mode == TimerMode.PROGRESSIVE:
            elapsed = self.clock_controller.model.timer_current
            hours, remainder = divmod(elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.view.show_notification(f"Se ha realizado un tiempo de {time_str}")
            self.view.show_message_box("Cronómetro", f"Se ha realizado un tiempo de {time_str}")
    
    def change_language(self, language: str):
        """Cambia el idioma de la aplicación"""
        if language == self.current_language:
            return
        
        # Remover traductor anterior
        self.app.removeTranslator(self.translator)
        
        # Cargar nuevo traductor
        translations_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'resources',
            'translations'
        )
        
        if language == 'es':
            translation_file = os.path.join(translations_path, 'app_es.qm')
        else:
            translation_file = os.path.join(translations_path, 'app_en.qm')
        
        if os.path.exists(translation_file):
            if self.translator.load(translation_file):
                self.app.installTranslator(self.translator)
                self.current_language = language
                
                # Retranslate UI
                self.retranslate_ui()
                
                self.view.show_notification(
                    self.view.tr(f"Language changed to {language}")
                )
        else:
            # Si no existe el archivo de traducción, seguir en inglés
            self.current_language = 'en'
    
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
    
    def open_tournament(self):
        """Abre la ventana de gestión de torneos"""
        if hasattr(self, 'tournament_window') and self.tournament_window.isVisible():
            self.tournament_window.raise_()
            return
        
        from views.tournament_window import TournamentWindow
        from views.digital_clock_widget import DigitalClockWidget
        from controllers.tournament_controller import TournamentController
        
        self.tournament_window = TournamentWindow()
        clock_widget = DigitalClockWidget()
        self.tournament_window.add_clock_widget(clock_widget)
        self.tournament_controller = TournamentController(self.tournament_window, clock_widget, self.app)
        self.tournament_window.show()
