"""
Modelo del Reloj Digital
Define las enumeraciones y la lógica de datos del componente
"""
from enum import Enum
from datetime import datetime, time


class ClockMode(Enum):
    """Modo de funcionamiento del reloj"""
    CLOCK = "clock"
    TIMER = "timer"


class TimerMode(Enum):
    """Modo del temporizador"""
    PROGRESSIVE = "progressive"  # Cuenta hacia adelante
    REGRESSIVE = "regressive"    # Cuenta hacia atrás


class ClockModel:
    """Modelo de datos para el componente de reloj digital"""
    
    def __init__(self):
        # Modo de funcionamiento
        self._mode = ClockMode.CLOCK
        
        # Configuración de formato
        self._format_24h = True
        
        # Configuración de alarma
        self._alarm_enabled = False
        self._alarm_hour = 0
        self._alarm_minute = 0
        self._alarm_message = "Mensaje para la alarma!!"
        self._alarm_triggered = False
        
        # Configuración de temporizador
        self._timer_mode = TimerMode.REGRESSIVE
        self._timer_duration = 60  # En segundos
        self._timer_current = 0
        self._timer_running = False
        self._timer_paused = False
        
    # Propiedades de modo
    @property
    def mode(self):
        return self._mode
    
    @mode.setter
    def mode(self, value: ClockMode):
        if isinstance(value, ClockMode):
            self._mode = value
            self.reset_timer()
    
    # Propiedades de formato
    @property
    def format_24h(self):
        return self._format_24h
    
    @format_24h.setter
    def format_24h(self, value: bool):
        self._format_24h = value
    
    # Propiedades de alarma
    @property
    def alarm_enabled(self):
        return self._alarm_enabled
    
    @alarm_enabled.setter
    def alarm_enabled(self, value: bool):
        self._alarm_enabled = value
        if value:
            self._alarm_triggered = False
    
    @property
    def alarm_hour(self):
        return self._alarm_hour
    
    @alarm_hour.setter
    def alarm_hour(self, value: int):
        if 0 <= value <= 23:
            self._alarm_hour = value
            self._alarm_triggered = False
    
    @property
    def alarm_minute(self):
        return self._alarm_minute
    
    @alarm_minute.setter
    def alarm_minute(self, value: int):
        if 0 <= value <= 59:
            self._alarm_minute = value
            self._alarm_triggered = False
    
    @property
    def alarm_message(self):
        return self._alarm_message
    
    @alarm_message.setter
    def alarm_message(self, value: str):
        self._alarm_message = value
    
    @property
    def alarm_triggered(self):
        return self._alarm_triggered
    
    def mark_alarm_as_triggered(self):
        """Marca la alarma como disparada para evitar repeticiones"""
        self._alarm_triggered = True
    
    # Propiedades de temporizador
    @property
    def timer_mode(self):
        return self._timer_mode
    
    @timer_mode.setter
    def timer_mode(self, value: TimerMode):
        if isinstance(value, TimerMode):
            self._timer_mode = value
    
    @property
    def timer_duration(self):
        return self._timer_duration
    
    @timer_duration.setter
    def timer_duration(self, value: int):
        if value >= 0:
            self._timer_duration = value
            if not self._timer_running:
                self._timer_current = 0 if self._timer_mode == TimerMode.PROGRESSIVE else value
    
    @property
    def timer_current(self):
        return self._timer_current
    
    @property
    def timer_running(self):
        return self._timer_running
    
    @property
    def timer_paused(self):
        return self._timer_paused
    
    # Métodos de temporizador
    def start_timer(self):
        """Inicia el temporizador"""
        if not self._timer_running:
            self._timer_running = True
            self._timer_paused = False
    
    def pause_timer(self):
        """Pausa el temporizador"""
        if self._timer_running:
            self._timer_paused = True
    
    def resume_timer(self):
        """Reanuda el temporizador"""
        if self._timer_running and self._timer_paused:
            self._timer_paused = False
    
    def stop_timer(self):
        """Detiene el temporizador"""
        self._timer_running = False
        self._timer_paused = False
    
    def reset_timer(self):
        """Reinicia el temporizador"""
        self._timer_running = False
        self._timer_paused = False
        if self._timer_mode == TimerMode.PROGRESSIVE:
            self._timer_current = 0
        else:
            self._timer_current = self._timer_duration
    
    def update_timer(self):
        """Actualiza el tiempo del temporizador (llamado cada segundo)"""
        if not self._timer_running or self._timer_paused:
            return False
        
        if self._timer_mode == TimerMode.PROGRESSIVE:
            self._timer_current += 1
            # En modo progresivo, continúa indefinidamente sin límite
            return False
        else:  # REGRESSIVE
            self._timer_current -= 1
            if self._timer_current <= 0:
                self._timer_current = 0
                return True  # Timer finished
        
        return False
    
    def check_alarm(self):
        """Verifica si debe dispararse la alarma"""
        if not self._alarm_enabled or self._alarm_triggered:
            return False
        
        now = datetime.now()
        if now.hour == self._alarm_hour and now.minute == self._alarm_minute:
            return True
        
        return False
    
    def get_current_time_string(self):
        """Obtiene la hora actual como string formateado"""
        now = datetime.now()
        if self._format_24h:
            return now.strftime("%H:%M:%S")
        else:
            return now.strftime("%I:%M:%S %p")
    
    def get_timer_string(self):
        """Obtiene el tiempo del temporizador como string formateado"""
        hours = self._timer_current // 3600
        minutes = (self._timer_current % 3600) // 60
        seconds = self._timer_current % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
