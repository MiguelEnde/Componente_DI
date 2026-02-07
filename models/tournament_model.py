"""
Modelo para la gestión de torneos de fútbol
"""
from datetime import datetime


class Match:
    """Representa un partido de fútbol"""
    
    def __init__(self, team1: str, team2: str, duration_minutes: int):
        self.team1 = team1
        self.team2 = team2
        self.duration_minutes = duration_minutes
        self.duration_seconds = duration_minutes * 60
        self.start_time = None
        self.end_time = None
        self.events = []
        self.in_progress = False
    
    def start(self):
        """Inicia el partido"""
        self.start_time = datetime.now()
        self.in_progress = True
        self.add_event(f"El partido ha comenzado: {self.team1} vs {self.team2}")
    
    def end(self):
        """Finaliza el partido"""
        self.end_time = datetime.now()
        self.in_progress = False
        self.add_event(f"Match ended")
    
    def add_event(self, event: str):
        """Añade un evento al registro del partido"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.events.append(f"[{timestamp}] {event}")
    
    def get_match_info(self):
        """Obtiene información del partido"""
        return f"{self.team1} vs {self.team2} ({self.duration_minutes} min)"


class TournamentModel:
    """Modelo para gestionar el torneo"""
    
    def __init__(self):
        self.current_match = None
        self.match_history = []
    
    def create_match(self, team1: str, team2: str, duration_minutes: int):
        """Crea un nuevo partido"""
        if self.current_match and self.current_match.in_progress:
            raise ValueError("Ya hay un partido en progreso")
        
        self.current_match = Match(team1, team2, duration_minutes)
        return self.current_match
    
    def start_current_match(self):
        """Inicia el partido actual"""
        if not self.current_match:
            raise ValueError("No hay partido para iniciar")
        
        self.current_match.start()
    
    def end_current_match(self):
        """Finaliza el partido actual"""
        if not self.current_match:
            raise ValueError("No hay partido para finalizar")
        
        self.current_match.end()
        self.match_history.append(self.current_match)
    
    def has_active_match(self):
        """Verifica si hay un partido activo"""
        return self.current_match is not None and self.current_match.in_progress
