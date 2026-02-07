"""
Vista de la ventana principal de prueba
Carga su interfaz desde un archivo .ui
"""
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox
from PySide6.QtGui import QAction
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from translations import translate
import os


class MainWindow(QMainWindow):
    """Ventana principal para probar el componente de reloj"""
    
    def __init__(self):
        super().__init__()
        
        # Cargar la interfaz desde el archivo .ui
        self.load_ui()
        
        # Referencias a widgets
        self.setup_widget_references()
        
        # Placeholder para el reloj digital
        self.clock_widget = None
        
        # Aplicar traducciones iniciales (en español por defecto)
        self.retranslateUi('es')
        
    def load_ui(self):
        """Carga la interfaz desde el archivo .ui"""
        ui_file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'ui_files',
            'main_window.ui'
        )
        
        ui_file = QFile(ui_file_path)
        if not ui_file.open(QIODevice.ReadOnly):
            raise RuntimeError(f"Cannot open UI file: {ui_file_path}")
        
        loader = QUiLoader()
        # Cargar sin pasar self como parent para evitar problemas con QMainWindow
        self.ui = loader.load(ui_file)
        ui_file.close()
        
        # Copiar propiedades de la ventana cargada
        if self.ui:
            self.setCentralWidget(self.ui.findChild(QWidget, "centralwidget"))
            menubar = self.ui.findChild(QWidget, "menubar")
            if menubar:
                self.setMenuBar(menubar)
            statusbar = self.ui.findChild(QWidget, "statusbar")
            if statusbar:
                self.setStatusBar(statusbar)
            self.setWindowTitle(self.ui.windowTitle())
            self.resize(self.ui.size())
        
    def setup_widget_references(self):
        """Configura referencias a los widgets del UI"""
        self.groupBoxConfig = self.findChild(QWidget, "groupBoxConfig")
        self.comboMode = self.findChild(QWidget, "comboMode")
        self.comboFormat = self.findChild(QWidget, "comboFormat")
        self.checkAlarmActive = self.findChild(QWidget, "checkAlarmActive")
        self.timeAlarm = self.findChild(QWidget, "timeAlarm")
        self.txtAlarmMessage = self.findChild(QWidget, "txtAlarmMessage")
        self.spinTimerDuration = self.findChild(QWidget, "spinTimerDuration")
        self.btnApplyConfig = self.findChild(QWidget, "btnApplyConfig")
        self.lblNotification = self.findChild(QWidget, "lblNotification")
        
        # Acciones del menú - buscar en self.ui como QAction
        if self.ui:
            self.actionEnglish = self.ui.findChild(QAction, "actionEnglish")
            self.actionSpanish = self.ui.findChild(QAction, "actionSpanish")
        else:
            self.actionEnglish = None
            self.actionSpanish = None
    
    def add_clock_widget(self, clock_widget):
        """Añade el widget del reloj a la interfaz"""
        self.clock_widget = clock_widget
        
        # Insertar el reloj antes del grupo de configuración
        central_widget = self.centralWidget()
        layout = central_widget.layout()
        layout.insertWidget(0, clock_widget)
    
    def set_controller(self, controller):
        """Establece el controlador"""
        self.controller = controller
        
        # Conectar señales
        if self.btnApplyConfig:
            self.btnApplyConfig.clicked.connect(controller.apply_configuration)
        if self.actionEnglish:
            self.actionEnglish.triggered.connect(lambda: controller.change_language('en'))
        if self.actionSpanish:
            self.actionSpanish.triggered.connect(lambda: controller.change_language('es'))
        
        # Conectar cambio de modo para aplicar automáticamente
        if self.comboMode:
            self.comboMode.currentIndexChanged.connect(controller.apply_configuration)
    
    def get_configuration(self):
        """Obtiene la configuración actual de los controles"""
        config = {
            'mode': self.comboMode.currentIndex(),
            'format_24h': self.comboFormat.currentIndex() == 0,
            'alarm_enabled': self.checkAlarmActive.isChecked(),
            'alarm_time': self.timeAlarm.time(),
            'alarm_message': self.txtAlarmMessage.text(),
            'timer_duration': self.spinTimerDuration.value()
        }
        return config
    
    def show_notification(self, message: str):
        """Muestra una notificación en la etiqueta"""
        if self.lblNotification:
            self.lblNotification.setText(message)
    
    def show_message_box(self, title: str, message: str):
        """Muestra un cuadro de mensaje"""
        QMessageBox.information(self, title, message)
    
    def retranslateUi(self):
        """Retraduce los textos del UI"""
        self.setWindowTitle(self.tr("Digital Clock Test Application"))
        
        if self.groupBoxConfig:
            self.groupBoxConfig.setTitle(self.tr("Clock Configuration"))
        
        if self.comboMode:
            self.comboMode.setItemText(0, self.tr("Clock"))
            self.comboMode.setItemText(1, self.tr("Timer"))
        
        if self.comboFormat:
            self.comboFormat.setItemText(0, self.tr("24 Hours"))
            self.comboFormat.setItemText(1, self.tr("12 Hours"))
        
        if self.checkAlarmActive:
            self.checkAlarmActive.setText(self.tr("Enable Alarm"))
        
        if self.btnApplyConfig:
            self.btnApplyConfig.setText(self.tr("Apply Configuration"))
        
        if self.lblNotification:
            current_text = self.lblNotification.text()
            if "Notifications will appear here" in current_text or "Las notificaciones aparecerán aquí" in current_text:
                self.lblNotification.setText(self.tr("Notifications will appear here"))
        
        # Retranslate labels
        for label_name in ["lblMode", "lblFormat", "lblAlarm", "lblAlarmTime", 
                          "lblAlarmMessage", "lblTimerDuration"]:
            label = self.findChild(QWidget, label_name)
            if label and hasattr(label, 'text'):
                # Map English to translation keys
                text_map = {
                    "Mode:": self.tr("Mode:"),
                    "Format:": self.tr("Format:"),
                    "Alarm Active:": self.tr("Alarm Active:"),
                    "Alarm Time:": self.tr("Alarm Time:"),
                    "Alarm Message:": self.tr("Alarm Message:"),
                    "Timer Duration (sec):": self.tr("Timer Duration (sec):")
                }
                current = label.text()
                for eng, trans in text_map.items():
                    if eng in current or trans == current:
                        label.setText(trans)
    
    def retranslateUi(self, language: str = 'es'):
        """Retraduce los textos del UI"""
        self.setWindowTitle(translate('Digital Clock Test Application', language))
        
        if self.groupBoxConfig:
            self.groupBoxConfig.setTitle(translate('Clock Configuration', language))
        
        if self.btnApplyConfig:
            self.btnApplyConfig.setText(translate('Apply Configuration', language))
        
        # Retranslate labels
        label_translations = {
            "lblMode": "Mode:",
            "lblFormat": "Format:",
            "lblAlarm": "Alarm Active:",
            "lblAlarmTime": "Alarm Time:",
            "lblAlarmMessage": "Alarm Message:",
            "lblTimerDuration": "Timer Duration (sec):",
            "lblNotification": "Notifications will appear here",
        }
        
        for label_name, text in label_translations.items():
            label = self.findChild(QWidget, label_name)
            if label and hasattr(label, 'setText'):
                label.setText(translate(text, language))
        
        # Retranslate combo box options
        if self.comboMode:
            self.comboMode.clear()
            self.comboMode.addItem(translate('Clock', language))
            self.comboMode.addItem(translate('Timer', language))
            self.comboMode.addItem(translate('Fútbol', language))
            self.comboMode.addItem(translate('Cronómetro', language))
        
        if self.comboFormat:
            self.comboFormat.clear()
            self.comboFormat.addItem(translate('24 Hours', language))
            self.comboFormat.addItem(translate('12 Hours', language))
        
        if self.checkAlarmActive:
            self.checkAlarmActive.setText(translate('Enable Alarm', language))
        
        # Forzar actualización visual
        self.update()
