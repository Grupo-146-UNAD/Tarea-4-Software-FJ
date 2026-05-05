# =========================================================================================================
# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
# =========================================================================================================
# Versión con Interfaz Gráfica Tkinter - Menú Principal y Gestión Completa
# =========================================================================================================
# Integrantes:  
# Yuris Cerguey Reyes Mandón
# Danna Valeria Uribe Santiago
# Jose Daniel Machado Castellanos
# Diego Alejandro Rocha Manzano
# =========================================================================================================
# Curso: Programación
# =========================================================================================================
# Grupo: 146
# =========================================================================================================
# Tutor: Jhon Harold Patiño Pantoja
# =========================================================================================================
# Fecha: Mayo 2026
# =========================================================================================================
# Universidad Nacional Abierta y a Distancia (UNAD)
# =========================================================================================================

# =========================================================================================================
# MÓDULO LOGGER (SINGLETON)
# =========================================================================================================
# Es el proceso de guardar eventos, acciones y errores que ocurren en el programa. 
# Es como una bitácora o diario del sistema.
# Singleton es un patrón de diseño que garantiza que solo exista
# UNA instancia de una clase en todo el programa.

# ==================== IMPORTACIONES ======================================================================
# Cada importación trae funcionalidades específicas de Python
import datetime # Para manejar fechas, horas y realizar operaciones con tiempo
import os # Proporciona funciones para interactuar con el sistema operativo (archivos, directorios, rutas, etc.)
import traceback # Proporciona información detallada de errores (stack trace), mostrando la secuencia de llamadas que llevaron a una excepción

# =========================================================================================================
# CLASE: LoggerSistema
# Registra eventos y errores en un archivo de log.
# Singleton - garantiza que solo exista UNA instancia.
# =========================================================================================================
class LoggerSistema:
    
    _instancia = None
    
    # =====================================================================================================
    # Controla la creación de nuevas instancias (Singleton)
    # =====================================================================================================
    def __new__(cls):
        
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia
    
    # =====================================================================================================
    # Configura el archivo de logs cuando se crea la instancia
    # =====================================================================================================
    def _inicializar(self):
        
        self.archivo_log = "logs.txt"
        if not os.path.exists(self.archivo_log):
            with open(self.archivo_log, 'w', encoding='utf-8') as f:
                f.write(f"{'='*110}\n")
                f.write(f"LOG DEL SISTEMA SOFTWARE FJ - INICIADO {datetime.datetime.now()}\n")
                f.write(f"{'='*110}\n\n")
    
    # =====================================================================================================
    # Escribe un mensaje de EVENTO (con prefijo [EVENTO]) en el archivo de log
    # =====================================================================================================
    def registrar_evento(self, mensaje: str):
        
        with open(self.archivo_log, 'a', encoding='utf-8') as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[EVENTO] {timestamp} - {mensaje}\n")
    
    # =====================================================================================================
    # Escribe un ERROR detallado (con traceback) en el archivo de log
    # =====================================================================================================
    def registrar_error(self, error: Exception, contexto: str = ""):
        
        with open(self.archivo_log, 'a', encoding='utf-8') as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write("-" * 110 + "\n")
            f.write(f"[ERROR] {timestamp} - {contexto}\n")
            f.write(f"Tipo: {type(error).__name__}\n")
            f.write(f"Mensaje: {str(error)}\n")
            f.write(f"Traceback:\n{traceback.format_exc()}\n")
    # =====================================================================================================
    # Escribe una línea TEXTUAL en el archivo de log SIN prefijo [EVENTO]
    # Útil para líneas separadoras como "------------------"
    # =====================================================================================================
    def escribir_linea(self, texto: str = ""):
        
        with open(self.archivo_log, 'a', encoding='utf-8') as f:
            f.write(texto + "\n")