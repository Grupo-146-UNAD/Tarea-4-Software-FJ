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
# CLASE CLIENTE
# =========================================================================================================
# ==================== IMPORTACIONES ======================================================================
# Cada importación trae funcionalidades específicas de Python
from abc import ABC, abstractmethod
from excepciones import ClienteInvalidoError # Para manejo de errores específicos del sistema
from logger import LoggerSistema # Para registro de eventos y errores
import datetime # Para manejar fechas, horas y realizar operaciones con tiempo

# =========================================================================================================
# Definición de la clase EntidadBase que hereda de ABC (Abstract Base Class)
# ABC permite crear clases abstractas que no pueden ser instanciadas directamente
# =========================================================================================================
class EntidadBase(ABC):
    
    # Clase abstracta base para todas las entidades del sistema"""
    # para todas las entidades del sistema (clientes, servicios, etc.)
    
    # =====================================================================================================
    # Método constructor (__init__) que se ejecuta automáticamente al crear una instancia
    # Recibe id_entidad (int) y nombre (str) como parámetros
    # 'self' hace referencia a la instancia actual de la clase
    # =====================================================================================================
    def __init__(self, id_entidad: int, nombre: str):
        
        # Asigna el parámetro id_entidad al atributo privado _id
        self._id = id_entidad
        
        # Asigna el parámetro nombre al atributo privado _nombre
        self._nombre = nombre
        
        # Crea un atributo privado _fecha_creacion con la fecha y hora actual del sistema
        # datetime.datetime.now() obtiene el momento exacto en que se crea el objeto
        self._fecha_creacion = datetime.datetime.now()
    
    # =====================================================================================================
    # Decorador @abstractmethod: Indica que este método es abstracto
    # Las clases hijas OBLIGATORIAMENTE deben implementar este método
    # =====================================================================================================
    # Método que debe retornar una descripción de la entidad (tipo str)
    # No tiene implementación (solo 'pass') porque es abstracto
    # =====================================================================================================
    @abstractmethod
    def obtener_descripcion(self) -> str:
        pass  # 'pass' es una instrucción que no hace nada (placeholder)
    
    # =====================================================================================================
    # Decorador @property: Convierte un método en una propiedad (getter)
    # Permite acceder al atributo privado _id como si fuera público
    # Ejemplo: se puede usar 'objeto.id' en lugar de 'objeto._id'
    # =====================================================================================================
    # Método que retorna el valor del atributo privado _id
    # El tipo de retorno es int (entero)
    # =====================================================================================================
    @property
    def id(self) -> int:
        # Retorna el ID almacenado en el atributo privado
        return self._id
    
    # =====================================================================================================
    # Decorador @property: Convierte este método en propiedad (getter)
    # Permite leer el nombre de la entidad sin acceder directamente al atributo
    # =====================================================================================================
    # Método que retorna el nombre de la entidad
    # El tipo de retorno es str (cadena de texto)
    # =====================================================================================================
    @property
    def nombre(self) -> str:
        # Retorna el nombre almacenado en el atributo privado
        return self._nombre

# =========================================================================================================
# Definición de la clase Cliente que hereda de EntidadBase
# =========================================================================================================
class Cliente(EntidadBase):
    
    # Representa a los clientes del sistema con validaciones específicas
    
    # =====================================================================================================
    # Método constructor que se ejecuta al crear un nuevo cliente
    # Recibe: id_cliente (int), nombre (str), email (str), telefono (str), cedula (str)
    # =====================================================================================================
    def __init__(self, id_cliente: int, nombre: str, email: str, telefono: str, cedula: str):
        
        # super() llama al constructor de la clase padre (EntidadBase)
        # Le pasa id_cliente y nombre para que los procese la clase base
        super().__init__(id_cliente, nombre)
        
        # Inicializa el atributo privado _email como None (valor nulo)
        # Se asignará después mediante el setter para validarlo
        self._email = None
        
        # Inicializa el atributo privado _telefono como None
        # Se asignará después mediante el setter para validarlo
        self._telefono = None
        
        # Inicializa el atributo privado _cedula como None
        # Se asignará después mediante el setter para validarlo
        self._cedula = None
        
        # Inicializa el atributo privado _activo como True (cliente activo por defecto)
        # Un cliente activo puede hacer reservas, uno inactivo no
        self._activo = True
        
        # Llama al setter de email para validar y asignar el valor
        # Esto ejecutará el método email.setter que valida el formato
        self.email = email
        
        # Llama al setter de telefono para validar y asignar el valor
        # Esto ejecutará el método telefono.setter que valida longitud y dígitos
        self.telefono = telefono
        
        # Llama al setter de cedula para validar y asignar el valor
        # Esto ejecutará el método cedula.setter que valida longitud mínima
        self.cedula = cedula
        
        # Obtiene la instancia única del Logger (Singleton) y registra el evento
        # Registra que se ha creado un nuevo cliente con su nombre
        LoggerSistema().registrar_evento(f"Cliente creado: {self._nombre}")
    
    # =====================================================================================================
    # Decorador @property: Convierte el método en getter de email
    # Permite acceder al email como cliente.email en lugar de cliente._email
    # =====================================================================================================
    # Getter de email: retorna el valor del atributo privado _email
    # El tipo de retorno es str (cadena de texto)
    # =====================================================================================================
    @property
    def email(self) -> str:
        # Retorna el email almacenado
        return self._email
    
    # =====================================================================================================
    # Decorador @email.setter: Define el setter para el email
    # Se ejecuta cuando se asigna un valor a cliente.email = "algo"
    # =====================================================================================================
    # Setter de email: recibe el valor a asignar
    # =====================================================================================================
    @email.setter
    def email(self, valor: str):
        
        # Validación: si el valor está vacío O no contiene @ O no contiene punto (.)
        if not valor or "@" not in valor or "." not in valor:
            # Lanza una excepción personalizada ClienteInvalidoError
            # Interrumpe la ejecución y muestra el error
            raise ClienteInvalidoError(f"Email inválido: {valor}")
        
        # Si pasa la validación, asigna el valor al atributo privado _email
        self._email = valor
    
    # =====================================================================================================
    # Decorador @property: Convierte el método en getter de teléfono
    # =====================================================================================================
    # Getter de teléfono: retorna el atributo privado _telefono
    # =====================================================================================================
    @property
    def telefono(self) -> str:
        return self._telefono
    
    # =====================================================================================================
    # Decorador @telefono.setter: Define el setter para el teléfono
    # =====================================================================================================
    # Setter de teléfono: recibe el valor a asignar
    # =====================================================================================================
    @telefono.setter
    def telefono(self, valor: str):
        
        # Validación: si está vacío O tiene menos de 7 caracteres O no son solo dígitos
        # isdigit() retorna True solo si todos los caracteres son números (0-9)
        if not valor or len(valor) < 7 or not valor.isdigit():
            # Lanza excepción si el teléfono no es válido
            raise ClienteInvalidoError(f"Teléfono inválido: {valor}")
        
        # Si pasa la validación, asigna el valor al atributo privado _telefono
        self._telefono = valor
    
    # =====================================================================================================
    # Decorador @property: Convierte el método en getter de cédula
    # =====================================================================================================
    # Getter de cédula: retorna el atributo privado _cedula
    # =====================================================================================================
    @property
    def cedula(self) -> str:
        return self._cedula
    
    # =====================================================================================================
    # Decorador @cedula.setter: Define el setter para la cédula
    # =====================================================================================================
    # Setter de cédula: recibe el valor a asignar
    # =====================================================================================================
    @cedula.setter
    def cedula(self, valor: str):
        
        # Validación: si está vacía O tiene menos de 5 caracteres
        if not valor or len(valor) < 5:
            # Lanza excepción si la cédula no es válida
            raise ClienteInvalidoError(f"Cédula inválida: {valor}")
        
        # Si pasa la validación, asigna el valor al atributo privado _cedula
        self._cedula = valor
    
    # =====================================================================================================
    # Decorador @property: Convierte el método en getter de activo
    # No tiene setter público porque el estado se modifica con activar()/desactivar()
    # =====================================================================================================
    # Getter de activo: retorna el estado del cliente (True=activo, False=inactivo)
    # El tipo de retorno es bool (booleano: True o False)
    # =====================================================================================================
    @property
    def activo(self) -> bool:
        return self._activo
    
    # =====================================================================================================
    # Método para desactivar el cliente
    # Cambia el estado a False (inactivo)
    # =====================================================================================================
    def desactivar(self):
        # Cambia el atributo _activo de True a False
        self._activo = False
        
        # Registra en el log que el cliente ha sido desactivado
        LoggerSistema().registrar_evento(f"Cliente {self._nombre} desactivado")
    
    # =====================================================================================================
    # Método para activar el cliente
    # Cambia el estado a True (activo)
    # =====================================================================================================
    def activar(self):
        # Cambia el atributo _activo de False a True
        self._activo = True
        
        # Registra en el log que el cliente ha sido activado
        LoggerSistema().registrar_evento(f"Cliente {self._nombre} activado")
    
    # =====================================================================================================
    # Implementación del método abstracto obtener_descripcion
    # La clase padre EntidadBase lo declaró como abstracto, por lo que es obligatorio
    # Retorna una cadena con la información resumida del cliente
    # =====================================================================================================
    def obtener_descripcion(self) -> str:
        # Formato: "nombre | email | teléfono"
        # Utiliza f-string para insertar los valores directamente
        return f"{self._nombre} | {self._email} | {self._telefono}"