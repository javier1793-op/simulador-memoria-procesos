"""RESPONSABLE: Miembro 3

Memoria con particiones variables (MVT) y política Best-Fit.
"""
from dataclasses import dataclass

from simulador.config import MEMORIA_SO, MEMORIA_USUARIO, INICIO_USUARIO


@dataclass
class Particion:
    id: int
    inicio: int               # dirección de comienzo (K)
    tamano: int               # (K)
    proceso_id: int | None    # None = hueco libre


class Memoria:
    def __init__(self):
        self.tamano_so = MEMORIA_SO
        # siempre ordenadas por dirección de inicio
        self.particiones: list[Particion] = [Particion(1, INICIO_USUARIO, MEMORIA_USUARIO, None)]
        self.siguiente_id = 2

    def buscar_hueco_best_fit(self, tamano: int) -> Particion | None:
        """Best-Fit: el hueco libre MÁS CHICO cuyo tamaño sea >= tamano.
        Empate: el de menor dirección. Si no hay ninguno, None."""
        huecos_disponibles = [
            p for p in self.particiones 
            if p.proceso_id is None and p.tamano >= tamano
        ]
        
        if not huecos_disponibles:
            return None
        
        # Ordenar por: 1) tamaño ascendente, 2) dirección de inicio ascendente (menor dirección)
        huecos_disponibles.sort(key=lambda p: (p.tamano, p.inicio))
        
        return huecos_disponibles[0]

    def asignar(self, proceso) -> bool:
        """Intenta ubicar al proceso. Si hay hueco:
        lo parte en partición exacta + resto libre, y retorna True. Si no, False."""
        hueco = self.buscar_hueco_best_fit(proceso.tamano)
        if not hueco:
            return False
        
        # Guardamos datos del hueco original
        indice = self.particiones.index(hueco)
        inicio_original = hueco.inicio
        tamano_original = hueco.tamano
        
        # Creamos la nueva partición para el proceso
        nueva_part = Particion(
            id=self.siguiente_id,
            inicio=inicio_original,
            tamano=proceso.tamano,
            proceso_id=proceso.id
        )
        self.siguiente_id += 1
        
        # Actualizamos la lista de particiones
        if tamano_original == proceso.tamano:
            # Encaja exacto, reemplazamos el hueco por la partición
            self.particiones[indice] = nueva_part
        else:
            # Sobra espacio, queda un hueco remanente después de la partición
            resto_hueco = Particion(
                id=self.siguiente_id,
                inicio=inicio_original + proceso.tamano,
                tamano=tamano_original - proceso.tamano,
                proceso_id=None
            )
            self.siguiente_id += 1
            # Reemplazamos el viejo hueco con la nueva partición y el resto libre
            self.particiones[indice:indice+1] = [nueva_part, resto_hueco]
            
        proceso.particion = nueva_part
        return True

    def liberar(self, proceso) -> None:
        """Libera la partición del proceso y fusiona huecos contiguos libres."""
        if not proceso.particion:
            return
        
        # Encontrar la partición del proceso y marcarla como libre
        for p in self.particiones:
            if p.id == proceso.particion.id:
                p.proceso_id = None
                break
                
        proceso.particion = None
        self._fusionar_huecos()

    def _fusionar_huecos(self) -> None:
        """Fusiona los huecos libres que estén contiguos."""
        nuevas_particiones = []
        i = 0
        while i < len(self.particiones):
            actual = self.particiones[i]
            if actual.proceso_id is None:
                # Buscar si hay más huecos libres seguidos y sumarlos
                tamano_acumulado = actual.tamano
                j = i + 1
                while j < len(self.particiones) and self.particiones[j].proceso_id is None:
                    tamano_acumulado += self.particiones[j].tamano
                    j += 1
                
                # Crear el hueco fusionado manteniendo el inicio del primero
                hueco_fusionado = Particion(
                    id=actual.id,
                    inicio=actual.inicio,
                    tamano=tamano_acumulado,
                    proceso_id=None
                )
                nuevas_particiones.append(hueco_fusionado)
                i = j  # Saltamos los huecos ya fusionados
            else:
                nuevas_particiones.append(actual)
                i += 1
        
        self.particiones = nuevas_particiones

   def memoria_libre_total(self) -> int:
        return sum(p.tamano for p in self.particiones if p.proceso_id is None)

    def tabla_particiones(self) -> list[dict]:
        resultado = []
        for p in self.particiones:
            estado = f"P{p.proceso_id}" if p.proceso_id is not None else "libre"
            resultado.append({
                "id": p.id,
                "inicio": p.inicio,
                "tamano": p.tamano,
                "proceso": estado,
                "fragmentacion_interna": 0  # En MVT la interna es siempre 0
            })
        return resultado