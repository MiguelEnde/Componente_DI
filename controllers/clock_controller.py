"""
Controlador del componente de Reloj Digital
Gestiona la lógica entre el modelo y la vista
"""
from PySide6.QtCore import Signal, QObject
from models.clock_model import ClockModel, ClockMode, TimerMode


class DigitalClockController(QObject):
    """Controlador para el componente de reloj digital"""
    
    chronometerPaused = Signal(int)
    
    def __init__(self, model: ClockModel, view):
        super().__init__()
        self.model = model
        self.view = view
        
        # Conectar el controlador con la vista
        self.view.set_controller(self)
        
        # Inicializar la vista
        self.update_display()
        self.update_controls()
    
    def set_mode(self, mode: ClockMode):
        """Establece el modo de funcionamiento"""
        self.model.mode = mode
        self.update_display()
        self.update_controls()
        
        if mode == ClockMode.CLOCK:
            self.view.start_internal_timer()
        else:
            self.view.stop_internal_timer()
    
    def set_format_24h(self, format_24h: bool):
        """Establece el formato de hora"""
        self.model.format_24h = format_24h
        if self.model.mode == ClockMode.CLOCK:
            self.update_display()
    
    def set_alarm(self, enabled: bool, hour: int = 0, minute: int = 0, message: str = "Alarm!"):
        """Configura la alarma"""
        self.model.alarm_enabled = enabled
        if enabled:
            self.model.alarm_hour = hour
            self.model.alarm_minute = minute
            self.model.alarm_message = message
    
    def set_timer_duration(self, seconds: int):
        """Establece la duración del temporizador"""
        self.model.timer_duration = seconds
        if self.model.mode == ClockMode.TIMER:
            self.update_display()
    
    def set_timer_mode(self, mode: TimerMode):
        """Establece el modo del temporizador (progresivo/regresivo)"""
        self.model.timer_mode = mode
        self.model.reset_timer()
        if self.model.mode == ClockMode.TIMER:
            self.update_display()
    
    def on_start(self):
        """Maneja el inicio del temporizador"""
        if self.model.mode == ClockMode.TIMER:
            if self.model.timer_paused:
                self.model.resume_timer()
            else:
                self.model.start_timer()
            self.view.start_internal_timer()
            self.update_controls()
            self.view.update_status(self.view.tr("Running..."))
    
    def on_pause(self):
        """Maneja la pausa del temporizador"""
        if self.model.mode == ClockMode.TIMER:
            if self.model.timer_paused:
                self.model.resume_timer()
                self.view.update_status(self.view.tr("Running..."))
            else:
                self.model.pause_timer()
                if self.model.timer_mode == TimerMode.PROGRESSIVE and self.model.timer_duration == 0:
                    self.chronometerPaused.emit(self.model.timer_current)
            self.update_controls()
    
    def on_reset(self):
        """Maneja el reinicio del temporizador"""
        if self.model.mode == ClockMode.TIMER:
            self.model.reset_timer()
            self.view.stop_internal_timer()
            self.update_display()
            self.update_controls()
            self.view.update_status(self.view.tr("Ready"))
    
    def on_timer_tick(self):
        """Se llama cada segundo por el timer interno"""
        if self.model.mode == ClockMode.CLOCK:
            # Modo reloj: actualizar hora y verificar alarma
            self.update_display()
            if self.model.check_alarm():
                self.model.mark_alarm_as_triggered()
                self.view.emit_alarm(self.model.alarm_message)
        
        elif self.model.mode == ClockMode.TIMER:
            # Modo temporizador: actualizar tiempo
            if self.model.timer_running and not self.model.timer_paused:
                finished = self.model.update_timer()
                self.update_display()
                
                if finished:
                    self.on_timer_finished()
    
    def on_timer_finished(self):
        """Se llama cuando el temporizador termina"""
        self.view.stop_internal_timer()
        self.model.stop_timer()
        self.update_controls()
        self.view.update_status(self.view.tr("Finished!"))
        self.view.emit_timer_finished()
    
    def update_display(self):
        """Actualiza el display con el tiempo actual"""
        if self.model.mode == ClockMode.CLOCK:
            time_str = self.model.get_current_time_string()
        else:
            time_str = self.model.get_timer_string()
        
        self.view.update_display(time_str)
        self.view.emit_time_updated(time_str)
    
    def update_controls(self):
        """Actualiza el estado de los controles"""
        if self.model.mode == ClockMode.CLOCK:
            # En modo reloj, deshabilitar todos los controles
            self.view.set_controls_enabled(False, False, False)
        else:
            # En modo temporizador
            if self.model.timer_running:
                if self.model.timer_paused:
                    self.view.set_controls_enabled(False, True, True)
                    if hasattr(self.view, 'btnPause'):
                        self.view.btnPause.setText(self.view.tr("Resume"))
                else:
                    self.view.set_controls_enabled(False, True, True)
                    if hasattr(self.view, 'btnPause'):
                        self.view.btnPause.setText(self.view.tr("Pause"))
            else:
                self.view.set_controls_enabled(True, False, True)
    
    def get_current_time_string(self):
        """Obtiene el string del tiempo actual"""
        if self.model.mode == ClockMode.CLOCK:
            return self.model.get_current_time_string()
        else:
            return self.model.get_timer_string()
