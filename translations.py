"""
Sistema de traducciones manual para la aplicación
"""

TRANSLATIONS = {
    'es': {
        # Tournament Window
        'Football Tournament Manager': 'Gestor de Torneos de Fútbol',
        'Current Match': 'Partido Actual',
        'Team 1:': 'Equipo 1:',
        'Team 2:': 'Equipo 2:',
        'Match Duration (minutes):': 'Duración del Partido (minutos):',
        'Match Status:': 'Estado del Partido:',
        'Start Match': 'Iniciar Partido',
        'End Match': 'Finalizar Partido',
        'No match in progress': 'No hay partido en curso',
        'Match events will be logged here...': 'Los eventos del partido se registrarán aquí...',
        'Error': 'Error',
        'Please enter both team names': 'Por favor ingrese los nombres de ambos equipos',
        'Match Ended': 'Partido Finalizado',
        'The match has been ended': 'El partido ha finalizado',
        'Full Time': 'Tiempo Completo',
        'Match ended manually': 'Partido finalizado manualmente',
        'Full time! Match duration completed': '¡Tiempo completo! Duración del partido completada',
        'Match in progress: ': 'Partido en progreso: ',
        'Match finished: ': 'Partido finalizado: ',
        'Exit': 'Salir',
        'English': 'English',
        'Español': 'Español',
        
        # Clock Widget
        'Start': 'Iniciar',
        'Pause': 'Pausar',
        'Resume': 'Reanudar',
        'Reset': 'Reiniciar',
        'Ready': 'Listo',
        'Running...': 'En ejecución...',
        'Paused': 'Pausado',
        'Finished!': '¡Finalizado!',
        
        # Main Window
        'Digital Clock Test Application': 'Aplicación de Prueba de Reloj Digital',
        'Clock Configuration': 'Configuración del Reloj',
        'Mode:': 'Modo:',
        'Clock': 'Reloj',
        'Timer': 'Temporizador',
        'Format:': 'Formato:',
        '24 Hours': '24 Horas',
        '12 Hours': '12 Horas',
        'Alarm Active:': 'Alarma Activa:',
        'Enable Alarm': 'Activar Alarma',
        'Alarm Time:': 'Hora de Alarma:',
        'Alarm Message:': 'Mensaje de Alarma:',
        'Timer Duration (sec):': 'Duración del Temporizador (seg):',
        'Apply Configuration': 'Aplicar Configuración',
        'Notifications will appear here': 'Las notificaciones aparecerán aquí',
        'Configuration applied successfully': 'Configuración aplicada exitosamente',
        'Alarm': 'Alarma',
        'Timer finished!': '¡Temporizador finalizado!',
        'The timer has finished!': '¡El temporizador ha finalizado!',
    },
    'en': {
        # Tournament Window
        'Football Tournament Manager': 'Football Tournament Manager',
        'Current Match': 'Current Match',
        'Team 1:': 'Team 1:',
        'Team 2:': 'Team 2:',
        'Match Duration (minutes):': 'Match Duration (minutes):',
        'Match Status:': 'Match Status:',
        'Start Match': 'Start Match',
        'End Match': 'End Match',
        'No match in progress': 'No match in progress',
        'Match events will be logged here...': 'Match events will be logged here...',
        'Error': 'Error',
        'Please enter both team names': 'Please enter both team names',
        'Match Ended': 'Match Ended',
        'The match has been ended': 'The match has been ended',
        'Full Time': 'Full Time',
        'Match ended manually': 'Match ended manually',
        'Full time! Match duration completed': 'Full time! Match duration completed',
        'Match in progress: ': 'Match in progress: ',
        'Match finished: ': 'Match finished: ',
        'Exit': 'Exit',
        'English': 'English',
        'Español': 'Español',
        
        # Clock Widget
        'Start': 'Start',
        'Pause': 'Pause',
        'Resume': 'Resume',
        'Reset': 'Reset',
        'Ready': 'Ready',
        'Running...': 'Running...',
        'Paused': 'Paused',
        'Finished!': 'Finished!',
        
        # Main Window
        'Digital Clock Test Application': 'Digital Clock Test Application',
        'Clock Configuration': 'Clock Configuration',
        'Mode:': 'Mode:',
        'Clock': 'Clock',
        'Timer': 'Timer',
        'Format:': 'Format:',
        '24 Hours': '24 Hours',
        '12 Hours': '12 Hours',
        'Alarm Active:': 'Alarm Active:',
        'Enable Alarm': 'Enable Alarm',
        'Alarm Time:': 'Alarm Time:',
        'Alarm Message:': 'Alarm Message:',
        'Timer Duration (sec):': 'Timer Duration (sec):',
        'Apply Configuration': 'Apply Configuration',
        'Notifications will appear here': 'Notifications will appear here',
        'Configuration applied successfully': 'Configuration applied successfully',
        'Alarm': 'Alarm',
        'Timer finished!': 'Timer finished!',
        'The timer has finished!': 'The timer has finished!',
    }
}

def translate(text: str, language: str = 'es') -> str:
    """
    Traduce un texto al idioma especificado
    
    Args:
        text: Texto a traducir
        language: Idioma ('es' o 'en')
    
    Returns:
        Texto traducido o el original si no se encuentra la traducción
    """
    if language not in TRANSLATIONS:
        return text
    
    return TRANSLATIONS[language].get(text, text)
