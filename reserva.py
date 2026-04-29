# =========================================================================================================
# CLASE RESERVA - CON MÉTODOS SOBRECARGADOS
# =========================================================================================================

# ==================== IMPORTACIONES ======================================================================
# Cada importación trae funcionalidades específicas de Python
import datetime # Para manejar fechas, horas y realizar operaciones con tiempo
from excepciones import ReservaInvalidaError, EstadoReservaInvalidoError, ServicioNoDisponibleError # Para manejo de errores específicos del sistema
from logger import LoggerSistema # Para registro de eventos y errores

# =========================================================================================================
# Integra cliente, servicio y gestiona el ciclo de vida de la reserva
# =========================================================================================================
class Reserva:
    
    # Atributo de CLASE (compartido por todas las instancias)
    ESTADOS = ["PENDIENTE", "CONFIRMADA", "CANCELADA", "COMPLETADA"]
    
    
    # =====================================================================================================
    # CONSTRUCTOR: __init__ recibe cliente, servicio, duración y parámetros extra para calcular el costo
    # =====================================================================================================
    def __init__(self, id_reserva: int, cliente, servicio, 
                duracion_horas: float, parametros_extra: dict = None,
                fecha_reserva: datetime.datetime = None):
        
        # Crea una nueva reserva con validaciones
        
        self._id = id_reserva                    # ID único de reserva
        self._cliente = cliente                  # Objeto Cliente (composición)
        self._servicio = servicio                # Objeto Servicio (composición)
        self._duracion_horas = duracion_horas    # Duración en horas
        self._parametros_extra = parametros_extra or {}  # Diccionario vacío si es None
        self._fecha_reserva = fecha_reserva or datetime.datetime.now()  # Fecha actual si no se especifica
        self._estado = "PENDIENTE"               # Estado inicial
        self._costo_total = 0.0                  # Costo inicial (se calculará)
        
        # Llama a métodos privados (con _) para validar y calcular
        self._validar_reserva()
        self._calcular_costo_inicial()
        
        LoggerSistema().registrar_evento(f"Reserva {self._id} creada para {cliente.nombre}")
    
    # =====================================================================================================
    # MÉTODOS PRIVADOS: _validar_reserva y _calcular_costo_inicial se encargan de validar los datos
    # =====================================================================================================
    def _validar_reserva(self):
        # Verifica que todos los datos sean correctos ANTES de crear la reserva
        
        # Validación 1: Cliente activo
        if not self._cliente.activo:
            raise ReservaInvalidaError("El cliente no está activo")
        
        # Validación 2: Servicio disponible
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError("El servicio no está disponible")
        
        # Validación 3: Duración positiva
        if self._duracion_horas <= 0:
            raise ReservaInvalidaError("La duración debe ser mayor a 0 horas")
        
        # Validación 4: Duración máxima de 24 horas
        if self._duracion_horas > 24:
            raise ReservaInvalidaError("No se permiten reservas de más de 24 horas")
    
    # =====================================================================================================
    # MÉTODO PRIVADO: _calcular_costo_inicial utiliza el polimorfismo del servicio
    # para calcular el costo total
    # =====================================================================================================
    def _calcular_costo_inicial(self):
        
        # Calcula el costo usando el polimorfismo del servicio
        
        try:
            # Llama al método calcular_costo del servicio (polimorfismo)
            self._costo_total = self._servicio.calcular_costo(
                self._duracion_horas, 
                **self._parametros_extra  # Desempaqueta el diccionario como argumentos nombrados
            )
        except Exception as e:
            # 'raise ... from e' encadena excepciones (preserva la causa original)
            raise ReservaInvalidaError(f"Error calculando costo: {str(e)}") from e
    
    # ==================== MÉTODOS DE ESTADO ====================
    
    # =====================================================================================================
    # MÉTODOS DE NEGOCIO: confirmar Cambia estado a CONFIRMADA (solo desde PENDIENTE)
    # =====================================================================================================
    def confirmar(self):
        
        # Cambia estado a CONFIRMADA (solo desde PENDIENTE)
        
        # Verifica que el estado actual sea PENDIENTE
        if self._estado != "PENDIENTE":
            raise EstadoReservaInvalidoError(
                f"No se puede confirmar reserva en estado {self._estado}"
            )
        
        # Verifica nuevamente disponibilidad (pudo haber cambiado)
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError("El servicio ya no está disponible")
        
        self._estado = "CONFIRMADA"
        LoggerSistema().registrar_evento(f"Reserva {self._id} confirmada. Costo: ${self._costo_total}")
    
    # =====================================================================================================
    # MÉTODO: cancelar Cambia estado a CANCELADA (desde PENDIENTE o CONFIRMADA) y registra el motivo
    # =====================================================================================================
    def cancelar(self, motivo: str = ""):
        
        # Cancela la reserva (desde PENDIENTE o CONFIRMADA)
        
        # Verifica que no esté ya completada o cancelada
        if self._estado in ["COMPLETADA", "CANCELADA"]:
            raise EstadoReservaInvalidoError(
                f"No se puede cancelar reserva en estado {self._estado}"
            )
        
        self._estado = "CANCELADA"
        LoggerSistema().registrar_evento(
            f"Reserva {self._id} cancelada. Motivo: {motivo or 'No especificado'}"
        )
    
    # =====================================================================================================
    # MÉTODO: completar Cambia estado a COMPLETADA (solo desde CONFIRMADA) y registra el evento
    # =====================================================================================================
    def completar(self):
        
        # Solo desde estado CONFIRMADA
        
        if self._estado != "CONFIRMADA":
            raise EstadoReservaInvalidoError("Solo reservas confirmadas pueden completarse")
        self._estado = "COMPLETADA"
        LoggerSistema().registrar_evento(f"Reserva {self._id} completada")
    
    # =====================================================================================================
    # MÉTODO: aplicar_descuento Aplica un descuento porcentual al costo total y registra el evento
    # =====================================================================================================
    def aplicar_descuento(self, porcentaje: float):
        
        # Aplica un descuento porcentual al costo total
        
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("Porcentaje de descuento inválido")
        
        # Fórmula: costo * (1 - porcentaje/100)
        self._costo_total = round(self._costo_total * (1 - porcentaje/100), 2)
        LoggerSistema().registrar_evento(f"Descuento {porcentaje}% aplicado a reserva {self._id}")
    
    # ==================== MÉTODOS SOBRECARGADOS PARA CÁLCULO DE COSTOS ====================
    # ======================================================================================
    # Métodos sobrecargados con diferentes variantes de cálculo de costos con impuestos,
    # descuentos y parámetros opcionales
    # ======================================================================================
    
    # ---------- SOBRECARGA 1: Parámetros por defecto (forma más pythonica) ----------
    
    # =====================================================================================================
    # MÉTODO: calcular_costo_con_impuesto, calcula el costo total incluyendo impuesto
    # Demuestra sobrecarga con parámetro opcional (impuesto con valor por defecto)
    # =====================================================================================================
    def calcular_costo_con_impuesto(self, impuesto_porcentaje: float = 19) -> float:
        
        # SOBRECARGA 1: Calcula el costo total incluyendo impuesto
        # =========================================================
        # Demuestra sobrecarga con parámetro opcional (impuesto con valor por defecto)
        
        # PARÁMETROS:
        #    impuesto_porcentaje (float): Porcentaje de impuesto (default: 19% IVA)
        
        # RETORNA:
        #    float: Costo total con impuesto incluido
        
        # EJEMPLOS:
        #    >>> reserva.calcular_costo_con_impuesto()      # Usa 19% por defecto
        #    >>> reserva.calcular_costo_con_impuesto(10)    # Usa 10% personalizado
        
        return round(self._costo_total * (1 + impuesto_porcentaje / 100), 2)
    
    # ---------- SOBRECARGA 2: Método con diferentes parámetros ----------
    
    # =====================================================================================================
    # MÉTODO: calcular_costo_con_descuento, calcula el costo total aplicando descuento
    # Demuestra sobrecarga con un método que recibe un parámetro diferente
    # =====================================================================================================
    def calcular_costo_con_descuento(self, porcentaje_descuento: float) -> float:
        # SOBRECARGA 2: Calcula el costo total aplicando descuento
        # ========================================================
        # Demuestra sobrecarga con un método que recibe un parámetro diferente
        
        # PARÁMETROS:
        #    porcentaje_descuento (float): Porcentaje de descuento a aplicar (0-100)
        
        # RETORNA:
        #    float: Costo total con descuento aplicado
        
        # EJEMPLO:
        #     >>> reserva.calcular_costo_con_descuento(15)   # 15% de descuento
        
        if porcentaje_descuento < 0 or porcentaje_descuento > 100:
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100")
        
        return round(self._costo_total * (1 - porcentaje_descuento / 100), 2)
    
    # ---------- SOBRECARGA 3: Múltiples parámetros opcionales ----------
    
    # =====================================================================================================
    # MÉTODO: calcular_costo_con_impuesto_y_descuento, calcula el costo con impuesto y descuento
    #  Demuestra sobrecarga con múltiples parámetros opcionales
    # =====================================================================================================
    def calcular_costo_con_impuesto_y_descuento(self, impuesto: float = 19, descuento: float = 0) -> float:
        
        # SOBRECARGA 3: Calcula el costo con impuesto y descuento
        # ========================================================
        # Demuestra sobrecarga con múltiples parámetros opcionales
        
        # PARÁMETROS:
        #    impuesto (float): Porcentaje de impuesto (default: 19%)
        #    descuento (float): Porcentaje de descuento (default: 0%)
        
        # RETORNA:
        #    float: Costo total con impuesto y descuento
        
        # EJEMPLOS:
        #    >>> reserva.calcular_costo_con_impuesto_y_descuento(19, 10)  # 19% impuesto, 10% descuento
        #    >>> reserva.calcular_costo_con_impuesto_y_descuento(16, 5)    # 16% impuesto, 5% descuento
        
        total = self._costo_total
        total = total * (1 + impuesto / 100)   # Aplicar impuesto
        total = total * (1 - descuento / 100)   # Aplicar descuento
        return round(total, 2)
    
    # ---------- SOBRECARGA 4: Cálculo por persona (útil para salas) ----------
    
    # =====================================================================================================
    # MÉTODO: calcular_costo_por_persona, calcula el costo por persona con opción de incluir impuesto
    # Demuestra sobrecarga con parámetro booleano que cambia el comportamiento
    # =====================================================================================================
    def calcular_costo_por_persona(self, num_personas: int, incluir_impuesto: bool = False) -> dict:
        
        # SOBRECARGA 4: Calcula el costo por persona con opción de incluir impuesto
        # ==========================================================================
        # Demuestra sobrecarga con parámetro booleano que cambia el comportamiento
        
        # PARÁMETROS:
        #    num_personas (int): Número de personas que pagan
        #    incluir_impuesto (bool): Si True, incluye 19% de impuesto
        
        # RETORNA:
        #    dict: Diccionario con desglose del cálculo por persona
        
        # EJEMPLO:
        #     >>> reserva.calcular_costo_por_persona(10)           # Sin impuesto
        #    >>> reserva.calcular_costo_por_persona(10, True)     # Con impuesto
        
        if num_personas <= 0:
            raise ValueError("El número de personas debe ser mayor a 0")
        
        costo_base_por_persona = self._costo_total / num_personas
        
        if incluir_impuesto:
            costo_final_por_persona = costo_base_por_persona * 1.19
            impuesto_aplicado = costo_final_por_persona - costo_base_por_persona
        else:
            costo_final_por_persona = costo_base_por_persona
            impuesto_aplicado = 0
        
        return {
            "costo_total_reserva": round(self._costo_total, 2),
            "num_personas": num_personas,
            "costo_por_persona_sin_impuesto": round(costo_base_por_persona, 2),
            "impuesto_por_persona": round(impuesto_aplicado, 2),
            "costo_por_persona_final": round(costo_final_por_persona, 2)
        }
    
    # ---------- SOBRECARGA 5: Parámetros flexibles con **kwargs ----------
    
    # =====================================================================================================
    # MÉTODO: calcular_costo_personalizado, calcula costo con parámetros flexibles usando **kwargs
    # Demuestra sobrecarga donde se pueden pasar múltiples parámetros opcionales
    # =====================================================================================================
    def calcular_costo_personalizado(self, **kwargs) -> dict:
        
        # SOBRECARGA 5: Calcula costo con parámetros flexibles usando **kwargs
        # =====================================================================
        # Demuestra sobrecarga donde se pueden pasar múltiples parámetros opcionales
        
        # PARÁMETROS POSIBLES en kwargs:
        #    - impuesto: porcentaje de impuesto
        #    - descuento: porcentaje de descuento
        #    - recargo_fijo: valor fijo adicional
        #    - motivo_recargo: texto explicativo del recargo
        #    - membresa: tipo de membresía (basica, premium, gold)
        
        # RETORNA:
        #    dict: Diccionario completo con desglose del cálculo
        
        # EJEMPLOS:
        #    >>> reserva.calcular_costo_personalizado(impuesto=19)
        #    >>> reserva.calcular_costo_personalizado(descuento=10)
        #    >>> reserva.calcular_costo_personalizado(impuesto=19, descuento=10, recargo_fijo=5000)
        #    >>> reserva.calcular_costo_personalizado(membresia="premium")
        
        total = self._costo_total
        aplicaciones = []
        
        # Diccionario de descuentos por tipo de membresía
        descuentos_membresia = {
            "basica": 0,
            "premium": 10,
            "gold": 15
        }
        
        # Aplicar descuento por membresía
        if 'membresia' in kwargs and kwargs['membresia'].lower() in descuentos_membresia:
            desc_membresia = descuentos_membresia[kwargs['membresia'].lower()]
            if desc_membresia > 0:
                valor_descuento = total * desc_membresia / 100
                total -= valor_descuento
                aplicaciones.append({
                    "concepto": f"Descuento membresía {kwargs['membresia']}",
                    "porcentaje": desc_membresia,
                    "valor": round(valor_descuento, 2)
                })
        
        # Aplicar impuesto
        if 'impuesto' in kwargs and kwargs['impuesto'] > 0:
            valor_impuesto = total * kwargs['impuesto'] / 100
            total += valor_impuesto
            aplicaciones.append({
                "concepto": "Impuesto",
                "porcentaje": kwargs['impuesto'],
                "valor": round(valor_impuesto, 2)
            })
        
        # Aplicar descuento adicional
        if 'descuento' in kwargs and kwargs['descuento'] > 0:
            valor_descuento = total * kwargs['descuento'] / 100
            total -= valor_descuento
            aplicaciones.append({
                "concepto": "Descuento adicional",
                "porcentaje": kwargs['descuento'],
                "valor": round(valor_descuento, 2)
            })
        
        # Aplicar recargo fijo
        if 'recargo_fijo' in kwargs and kwargs['recargo_fijo'] > 0:
            total += kwargs['recargo_fijo']
            aplicaciones.append({
                "concepto": kwargs.get('motivo_recargo', 'Recargo fijo'),
                "porcentaje": None,
                "valor": round(kwargs['recargo_fijo'], 2)
            })
        
        return {
            "costo_original": round(self._costo_total, 2),
            "aplicaciones": aplicaciones,
            "costo_final": round(total, 2),
            "ahorro_total": round(self._costo_total - total, 2) if total < self._costo_total else 0,
            "recargo_total": round(total - self._costo_total, 2) if total > self._costo_total else 0
        }
    
    # ---------- SOBRECARGA 6: Suma de múltiples costos (*args) ----------
    
    # =====================================================================================================
    # MÉTODO: calcular_costo_acumulado, suma el costo de la reserva con costos adicionales
    # Demuestra sobrecarga usando *args (número variable de argumentos)
    # =====================================================================================================
    def calcular_costo_acumulado(self, *costos_adicionales) -> float:
        
        # SOBRECARGA 6: Suma el costo de la reserva con costos adicionales
        # ================================================================
        # Demuestra sobrecarga usando *args (número variable de argumentos)
        
        # PARÁMETROS:
        #    *costos_adicionales: Uno o más costos adicionales para sumar
        
        # RETORNA:
        # float: Suma total incluyendo la reserva y todos los costos adicionales
        
        # EJEMPLOS:
        #    >>> reserva.calcular_costo_acumulado(5000)                        # +1 costo adicional
        #    >>> reserva.calcular_costo_acumulado(5000, 3000, 2000)            # +3 costos adicionales
        
        total = self._costo_total
        for costo in costos_adicionales:
            total += costo
        return round(total, 2)
    
    # ---------- SOBRECARGA 7: Con tipo de cliente (sobrecarga por comportamiento) ----------
    
    # =====================================================================================================
    # MÉTODO: calcular_costo_por_tipo_cliente, calcula costo según el tipo de cliente
    # Demuestra sobrecarga donde el comportamiento cambia según el tipo de parámetro
    # =====================================================================================================
    def calcular_costo_por_tipo_cliente(self, tipo_cliente: str, incluir_impuesto: bool = True) -> dict:
        
        # SOBRECARGA 7: Calcula costo según el tipo de cliente
        # =====================================================
        # Demuestra sobrecarga donde el comportamiento cambia según el tipo de parámetro
        
        # TIPOS DE CLIENTE:
        #    - "regular": Sin descuento
        #    - "frecuente": 5% descuento
        #    - "vip": 10% descuento
        #    - "corporativo": 15% descuento
        
        # PARÁMETROS:
        #    tipo_cliente (str): Tipo de cliente (regular, frecuente, vip, corporativo)
        #    incluir_impuesto (bool): Si True, incluye 19% de impuesto
        
        # RETORNA:
        #    dict: Diccionario con desglose completo
        
        #EJEMPLO:
        #    >>> reserva.calcular_costo_por_tipo_cliente("vip")
        
        descuentos = {
            "regular": 0,
            "frecuente": 5,
            "vip": 10,
            "corporativo": 15
        }
        
        tipo = tipo_cliente.lower()
        if tipo not in descuentos:
            raise ValueError(f"Tipo de cliente inválido: {tipo_cliente}. Opciones: regular, frecuente, vip, corporativo")
        
        descuento = descuentos[tipo]
        total = self._costo_total * (1 - descuento / 100)
        
        if incluir_impuesto:
            total = total * 1.19
            impuesto_aplicado = total - (self._costo_total * (1 - descuento / 100))
        else:
            impuesto_aplicado = 0
        
        return {
            "tipo_cliente": tipo,
            "costo_original": round(self._costo_total, 2),
            "descuento_aplicado": descuento,
            "valor_descuento": round(self._costo_total * descuento / 100, 2),
            "costo_con_descuento": round(self._costo_total * (1 - descuento / 100), 2),
            "impuesto_incluido": incluir_impuesto,
            "valor_impuesto": round(impuesto_aplicado, 2) if incluir_impuesto else 0,
            "costo_final": round(total, 2)
        }
    
    # ==================== MÉTODO DEMOSTRATIVO ====================
    
    # =====================================================================================================
    # MÉTODO: demostrar_todas_sobrecargas, muestra ejemplos de todas las sobrecargas
    # Útil para verificar que todos los métodos sobrecargados funcionan correctamente
    # =====================================================================================================
    def demostrar_todas_sobrecargas(self) -> str:
        
        resultados = []
        resultados.append("=" * 70)
        resultados.append("📚 DEMOSTRACIÓN DE MÉTODOS SOBRECARGADOS")
        resultados.append("=" * 70)
        resultados.append(f"\n💰 COSTO ORIGINAL DE LA RESERVA: ${self._costo_total:,.2f}")
        
        # 1. Parámetros por defecto
        resultados.append("\n🔹 1. calcular_costo_con_impuesto()")
        resultados.append(f"    - Con impuesto 19%: ${self.calcular_costo_con_impuesto():,.2f}")
        resultados.append(f"    - Con impuesto 10%: ${self.calcular_costo_con_impuesto(10):,.2f}")
        
        # 2. Descuento
        resultados.append("\n🔹 2. calcular_costo_con_descuento()")
        resultados.append(f"    - Con 10% descuento: ${self.calcular_costo_con_descuento(10):,.2f}")
        resultados.append(f"    - Con 20% descuento: ${self.calcular_costo_con_descuento(20):,.2f}")
        
        # 3. Impuesto y descuento
        resultados.append("\n🔹 3. calcular_costo_con_impuesto_y_descuento()")
        resultados.append(f"    - 19% impuesto, 10% descuento: ${self.calcular_costo_con_impuesto_y_descuento(19, 10):,.2f}")
        resultados.append(f"    - 10% impuesto, 5% descuento: ${self.calcular_costo_con_impuesto_y_descuento(10, 5):,.2f}")
        
        # 4. Costo por persona
        resultados.append("\n🔹 4. calcular_costo_por_persona()")
        persona_result = self.calcular_costo_por_persona(5)
        resultados.append(f"    - Para 5 personas: ${persona_result['costo_por_persona_final']:,.2f} c/u")
        
        # 5. Personalizado con kwargs
        resultados.append("\n🔹 5. calcular_costo_personalizado()")
        custom = self.calcular_costo_personalizado(impuesto=19, descuento=10, membresia="vip")
        resultados.append(f"    - Con membresía VIP + 19% impuesto - 10% desc: ${custom['costo_final']:,.2f}")
        
        # 6. Costo acumulado
        resultados.append("\n🔹 6. calcular_costo_acumulado()")
        resultados.append(f"    - +$5,000 adicional: ${self.calcular_costo_acumulado(5000):,.2f}")
        resultados.append(f"    - +$5,000 + $3,000: ${self.calcular_costo_acumulado(5000, 3000):,.2f}")
        
        # 7. Por tipo de cliente
        resultados.append("\n🔹 7. calcular_costo_por_tipo_cliente()")
        vip_result = self.calcular_costo_por_tipo_cliente("vip", True)
        resultados.append(f"    - Cliente VIP: ${vip_result['costo_final']:,.2f}")
        corporativo_result = self.calcular_costo_por_tipo_cliente("corporativo", True)
        resultados.append(f"    - Cliente Corporativo: ${corporativo_result['costo_final']:,.2f}")
        
        resultados.append("\n" + "=" * 70)
        
        return "\n".join(resultados)
    
    # ==================== MÉTODOS DE INFORMACIÓN =========================================================
    
    # =====================================================================================================
    # MÉTODO: obtener_info Retorna un diccionario con toda la información de la reserva
    # =====================================================================================================
    def obtener_info(self) -> dict:
        
        # Retorna un DICCIONARIO con toda la información de la reserva
        # RETORNA: dict {clave: valor}
        
        return {
            "id": self._id,
            "cliente": self._cliente.nombre,
            "cliente_id": self._cliente.id,
            "servicio": self._servicio.nombre,
            "servicio_id": self._servicio.id,
            "duracion": self._duracion_horas,
            "estado": self._estado,
            "costo": self._costo_total,
            "fecha": self._fecha_reserva.strftime("%Y-%m-%d %H:%M"),
            "fecha_obj": self._fecha_reserva
        }
    
    # ==================== PROPERTIES =====================================================================
    
    # =====================================================================================================
    # PROPERTIES (getters)
    # Permiten acceder a los atributos privados de forma controlada, sin exponerlos directamente.
    # =====================================================================================================
    
    # Getter para acceder al ID
    @property
    def id(self) -> int:
        return self._id
    
    # Getter para acceder al estado
    @property
    def estado(self) -> str:
        return self._estado
    
    # Getter para acceder a la fecha
    @property
    def fecha_reserva(self) -> datetime.datetime:
        return self._fecha_reserva
    
    # Getter para acceder a la duración de horas
    @property
    def duracion_horas(self) -> float:
        return self._duracion_horas
    
    # Getter para acceder al tipo de servicio
    @property
    def servicio_id(self) -> int:
        return self._servicio.id
    
    # Getter para acceder al costo total
    @property
    def costo_total(self) -> float:
        
        return self._costo_total