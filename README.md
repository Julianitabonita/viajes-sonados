# Viajes soñados

Aplicación web en Django para organizar los destinos que una persona sueña visitar. Cada usuario ve y gestiona únicamente sus propios viajes.

## Funcionalidades

- CRUD completo: listar, ver detalle, crear, editar y eliminar viajes.
- Paginación (3 viajes por página) y filtros por país y estado, compatibles entre sí.
- Panel de estadísticas, cuenta regresiva de días para cada viaje pendiente y mensajes de confirmación.
- Panel de administración con el modelo registrado.

## Modelo `ViajeSonado`

| Campo | Tipo | Descripción |
|---|---|---|
| usuario | ForeignKey a User | Dueño del viaje |
| destino | CharField | Ciudad o lugar |
| pais | CharField | País del destino |
| notas | TextField (opcional) | Detalles del viaje |
| presupuesto | DecimalField | Costo estimado |
| fecha_tentativa | DateField | Fecha planeada o de la visita |
| visitado | BooleanField | Si ya se realizó el viaje |

## Justificación de las decisiones

- **Relación con el usuario:** cada viaje pertenece a una persona mediante una `ForeignKey` a `User`. Se usa `on_delete=CASCADE` porque un viaje no tiene sentido sin su dueño. Las vistas filtran por `request.user`, de modo que nadie puede ver o modificar viajes ajenos.
- **Tipos de campo:** `destino`, `pais` y `notas` son texto. `presupuesto` usa `DecimalField` y no `FloatField`, porque el dinero necesita precisión exacta. `fecha_tentativa` es una fecha y `visitado` un booleano que distingue entre viajes cumplidos y pendientes.
- **Validación 1 (un solo campo):** el presupuesto debe ser mayor que cero, porque un viaje con costo nulo o negativo no es coherente.
- **Validación 2 (varios campos):** definida en `clean()`. Un viaje pendiente no puede tener una fecha pasada, y uno visitado no puede tener una fecha futura. Se hizo en `clean()` porque depende de dos campos a la vez.
- **Formulario:** se usa un `ModelForm` para reutilizar las validaciones del modelo. El campo `usuario` se excluye del formulario y se asigna en la vista, para que nadie pueda crear viajes a nombre de otra persona.
- **Eliminar con confirmación por POST:** evita borrados accidentales por abrir un enlace.
- **Paginación y filtros:** los filtros se aplican antes de paginar, y los enlaces de página conservan los filtros activos.

## Cómo ejecutarlo

1. Crear y activar un entorno virtual: `python -m venv venv` y `venv\Scripts\activate`
2. Instalar Django: `python -m pip install Django==6.1.1`
3. Aplicar migraciones: `python manage.py migrate`
4. Iniciar el servidor: `python manage.py runserver`
5. Abrir `http://127.0.0.1:8000/` e iniciar sesión con el usuario `admin` (contraseña `admin`).