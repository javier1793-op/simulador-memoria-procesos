"""Parámetros fijos de la consigna. Todos los módulos leen de acá: nadie hardcodea números."""

MEMORIA_SO = 100              # K reservados al Sistema Operativo (direcciones 0..99)
MEMORIA_USUARIO = 450         # K para procesos de usuario (direcciones 100..549)
INICIO_USUARIO = MEMORIA_SO   # primera dirección disponible para procesos
MAX_PROCESOS = 10             # máximo de procesos que se pueden cargar
GRADO_MULTIPROGRAMACION = 5   # máx. procesos en Ejecución + Listo + Listo/Suspendido
