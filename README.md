# Proyecto de Reloj Digital con PySide6

## Descripción
Este proyecto implementa un componente visual reutilizable de reloj digital que puede funcionar como:
- Reloj digital: Muestra la hora actual con formato de 12 o 24 horas
- Temporizador: Cuenta regresiva desde un tiempo configurado
- Cronómetro: Cuenta progresiva desde cero
- Futbol: Ventana personalizada para la aplicación del torneo.

## Características Principales

### Componente de Reloj Digital (DigitalClockWidget)
- Widget reutilizable e independiente
- Modo reloj con formato 12/24 horas
- Modo temporizador con cuenta regresiva
- Sistema de alarmas configurables
- Señales propias (alarmTriggered, timerFinished, timeUpdated)
- Controles de inicio, pausa y reinicio
- Interfaz cargada desde archivo .ui


### Traducción
- Soporte para múltiples idiomas (inglés y español)
- Sistema de traducciones con QTranslator
- Cambio de idioma en tiempo de ejecución

## Estructura del Proyecto


reloj_digital_proyecto/
│
├── models/                      
│   ├── __init__.py
│   ├── clock_model.py          
│   └── tournament_model.py    
│
├── views/                      
│   ├── __init__.py
│   ├── digital_clock_widget.py 
│   ├── main_window.py          
│   └── tournament_window.py    
│
├── controllers/                 
│   ├── __init__.py
│   ├── clock_controller.py     
│   ├── main_controller.py      
│   └── tournament_controller.py 
│
├── ui_files/                    
│   ├── digital_clock_widget.ui 
│   ├── main_window.ui          
│   └── tournament_window.ui    
│
├── resources/                  
│   └── translations/           
│       ├── app_en.ts          
│       ├── app_en.qm           
│       ├── app_es.ts           
│       └── app_es.qm           
│
├── main.py                    
├── main_test.py                
├── main_tournament.py          
├── main_futbol.py              
├── main_reloj.py               
├── compile_translations.py    
├── build_executables.py        
├── translations.py             
├── requirements.txt            
├── GUIA_USO_COMPONENTE.md      
├── INSTRUCCIONES_ENTREGA.md   
└── README.md                   

## Uso
Esta aplicación permite:
- Modo Reloj: Probar todas las funcionalidades del reloj (cambiar modos, configurar alarmas, temporizadores)
- Modo Fútbol: Gestionar torneos con cronometraje automático y descanso
- Cambiar idioma (inglés/español)

### Funcionalidad de Descanso en Torneos
Cuando se inicia un partido en el modo Fútbol:
- El temporizador cuenta regresivamente la duración configurada
- A la mitad del tiempo, el reloj se pausa automáticamente
- Se muestra "Descanso" en el recuadro de notificaciones
- Después de 5 segundos, el temporizador reanuda automáticamente
- Se registra el evento en el log del partido

### Ejecutar Aplicaciones Individuales
Si prefieres ejecutar las aplicaciones por separado:

Aplicación solo reloj:
Esta solo abrira el reloj totalmente separado. Se puede cambiar de idioma, 
establecer alarma o cambiar de modo (temporizador).

Aplicación solo fútbol:
Esta solo abrirá el reloj del fútbol. Se puede cambiar de idioma, establecer los equipos.
Se iniciara el partido donde se podra finalizar automáticamente.


## Ejemplo de uso

1. Iniciamos la clase main.py
2. Uso del reloj:

Modo predeterminado en reloj
Formato: 24h
(Si deseamos activar una alarma tenemos que pinchar en activar)

Hora de la alarma: 
Ejemplo si la hora es 09:30 probamos la alarma en 09:31.

Establecemos el mensaje de la alarma.

MUY IMPORTANTE tebemos que aplicar la configuracion.

3. Uso del temporizador:

Modo: temporizador
Duración temporizador: 60 segundos.
MUY IMPORTANTE tebemos que aplicar la configuracion.

4. Uso de Fútbol:

Modo: fútbol
MUY IMPORTANTE tebemos que aplicar la configuracion.

(Se nos abre la nueva ventana)
Ingresamos los equipos y establecemos la duración.

Iniciamos el partido...

5. FIN

Nota Traducción: Hay un pequeño error a la hora de traducir ya que tienes que cambiar el idioma varias veces para que funcione.

Ejemplo: Es -> In , In -> Es 
