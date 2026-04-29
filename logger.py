# =========================================================================================================
# SISTEMA DE LOGGING (SINGLETON)
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
# Definición de la clase LoggerSistema
# Esta clase se encarga de registrar eventos y errores en un archivo de log
# =========================================================================================================
class LoggerSistema:
    
    # Variable de CLASE (compartida por todas las instancias)
    # Almacena la única instancia que existirá del Logger
    # Inicialmente es None porque aún no se ha creado ninguna instancia
    _instancia = None
    
    # Método __new__: Es un método especial que se ejecuta ANTES que __init__
    # Controla la creación de nuevas instancias de la clase
    # cls se refiere a la clase (LoggerSistema)
    def __new__(cls):
        
        # Condicional: verifica si la variable de clase _instancia es None
        # Si es None, significa que aún no se ha creado ninguna instancia
        if cls._instancia is None:
            
            # super().__new__(cls): Llama al método __new__ de la clase padre (object)
            # Crea una nueva instancia de la clase
            cls._instancia = super().__new__(cls)
            
            # Llama al método privado _inicializar() en la nueva instancia
            # El guion bajo indica que es un método interno (no debe llamarse desde fuera)
            cls._instancia._inicializar()
        
        # Retorna la instancia (ya sea recién creada o la existente)
        # Esto garantiza que siempre se retorne el mismo objeto
        return cls._instancia
    
    # =====================================================================================================
    # Método privado _inicializar: Configura el archivo de log
    # Se ejecuta solo UNA vez, cuando se crea la primera instancia
    # =====================================================================================================
    def _inicializar(self):
        
        # Define el nombre del archivo de log como "logs.txt"
        # Este archivo se creará en la misma carpeta del programa
        self.archivo_log = "logs.txt"
        
        # os.path.exists(): Verifica si el archivo ya existe en el disco
        # El operador 'not' invierte el resultado: True si NO existe, False si existe
        if not os.path.exists(self.archivo_log):
            
            # with open(...): Abre el archivo de forma segura
            # 'w' indica modo escritura (write): crea el archivo, si existe lo SOBRESCRIBE
            # encoding='utf-8' permite guardar caracteres especiales (tildes, ñ, emojis)
            # 'as f' asigna el archivo abierto a la variable 'f'
            with open(self.archivo_log, 'w', encoding='utf-8') as f:
                
                # Escribe una línea de separación con 80 caracteres '='
                # {'='*80} repite el caracter '=' 80 veces
                # \n es el carácter de nueva línea (salto de línea)
                f.write(f"{'='*80}\n")
                
                # datetime.datetime.now(): Obtiene la fecha y hora actual del sistema
                # Se escribe en el archivo como cabecera indicando cuando se inició el log
                f.write(f"LOG DEL SISTEMA SOFTWARE FJ - INICIADO {datetime.datetime.now()}\n")
                
                # Línea de cierre de la cabecera (otra línea de 80 '=')
                f.write(f"{'='*80}\n\n")
                
                # El bloque 'with' cierra automáticamente el archivo al salir
                # No es necesario llamar a f.close() manualmente
    
    # =====================================================================================================
    # Método público: registrar_evento
    # Se usa para escribir EVENTOS normales (no errores) en el log
    # mensaje: str - el texto descriptivo del evento
    # =====================================================================================================
    def registrar_evento(self, mensaje: str):
        
        # 'a' indica modo append (agregar al final, sin borrar lo existente)
        # encoding='utf-8' para soportar caracteres especiales
        with open(self.archivo_log, 'a', encoding='utf-8') as f:
            
            # strftime(): método de datetime que formatea la fecha como string
            # "%Y-%m-%d %H:%M:%S" → Año-Mes-Día Hora:Minuto:Segundo
            # Ejemplo: "2026-04-28 18:04:49"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Escribe la línea con formato: [EVENTO] timestamp - mensaje
            # El formato es consistente para facilitar la lectura
            f.write(f"[EVENTO] {timestamp} - {mensaje}\n")
    
    # =====================================================================================================
    # Método público: registrar_error
    # Se usa para escribir ERRORES detallados en el log
    # error: Exception - el objeto de excepción capturado
    # contexto: str - descripción opcional de dónde ocurrió el error
    # =====================================================================================================
    def registrar_error(self, error: Exception, contexto: str = ""):
        
        # 'a' modo append: agrega al final del archivo sin borrar lo existente
        with open(self.archivo_log, 'a', encoding='utf-8') as f:
            
            # Obtiene la fecha y hora actual formateada
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Escribe la cabecera del error con el contexto proporcionado
            # [ERROR] indica que es un error, no un evento normal
            f.write(f"[ERROR] {timestamp} - {contexto}\n")
            
            # type(error).__name__: Obtiene el nombre de la clase del error
            # Ejemplo: "ClienteInvalidoError", "ValueError", "FileNotFoundError"
            f.write(f"Tipo: {type(error).__name__}\n")
            
            # str(error): Convierte el mensaje de error a string
            # Ejemplo: "Email inválido: test@sinpunto"
            f.write(f"Mensaje: {str(error)}\n")
            
            # traceback.format_exc(): Obtiene el stack trace COMPLETO del error
            # Muestra la secuencia de llamadas: archivo, línea, función donde falló
            # Esto es CRÍTICO para depurar porque muestra exactamente dónde ocurrió
            f.write(f"Traceback:\n{traceback.format_exc()}\n")
            
            # Línea separadora (60 guiones) para distinguir entre diferentes errores
            # Facilita la lectura del archivo de log
            f.write("-" * 60 + "\n")
