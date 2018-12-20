# Plataforma de Reservas CEI

*Plataforma para gestionar los préstamos de los artículos y espacios gestionados por el Centro de Alumnos de Ingeniería, para la Facultad de Cs. Físicas y Matemáticas, Universidad de Chile.*

### Sobre el Proyecto:
- Debido a un robo ocurrido en la casa del ***CEI*** el año 2017, perdió la base de datos con los artículos y espacios y el sistema para realizar préstamos de los mismos. Para compensar esta pérdida, el primer semestre de 2018 se les propuso a los alumnos del curso **CC4401 Ingeniería de Software** implementar un nuevo sistema, a modo de ejercicio pedagógico. Aunque en esta implementación se produjo mucho código y diversas soluciones de calidad, los requerimientos apuntados estaban lejos de asemejarse a las reales necesidades de este sistema. Así, durante el transcurso del segundo semestre, se retomó este trabajo, se obtuvieron nuevos requerimientos y se realizaron modificaciones al sistema para acercarlo a la realidad.

### Dependencias:

- ***Django*** **2.1.3**
- ***Pillow*** **5.3.0**
- ***django-gm2m*** **0.6.1** \*

Todas estas librerías pueden instalarse automáticamente ejecutando `pip install -r requirements.txt`.

\* La librería ***django-gm2m*** se utiliza para realizar *reservas* y *préstamos* de *artículos* y *espacios* sin tener que crear modelos especiales (Por ejemplo, *ReservaEspacio*, *ReservaArtículo*, etc.). Su documentación se puede encontrar [aquí](https://django-gm2m.readthedocs.io/en/stable/).


### Modelo de Datos:

El ***CEI*** dispone de diversos artículos y espacios para la utilización de los estudiantes dentro de la facultad. Los estudiantes pueden reservar *artículos* (entre los que se encuentran toldos, micrófonos, alargadores, etc.) y además pueden solicitar el uso de *espacios* que el ***CEI*** tiene a disposición: Salas de Reuniones y un Quincho.

El modelo de datos de la aplicación está compuesto por las siguientes instancias:

- **Profile**: Instancia para manejar los  perfiles de los usuarios de la plataforma:
  - `user`: Relación 1-a-1 con un `User` de *Django*.
  - `rut`: Rut del perfil.
  - `mail`
  - `isAdmin`: Indica si es administrador del sistema.
  - `hab`: Indica si está habilitado para ingresar al sistema.
##
- **Espacio**:
  - `nombre`
  - `descripcion`
  - `image`: Para guardar una imagen representativa del espacio
  - `estado`: Indica si el espacio está prestado, se encuentra en reparación o está disponible.
  - `capacidad`
##
- **Artículo**:
  - `nombre`
  - `image`: Guarda una imagen representativa del artículo.
  - `descripcion`
  - `lista_tags`: *Tags* para facilitar la búsqueda del artículo por parte de los estudiantes.
##
- **InstanciaArtículo**:
  - `articulo`: relaciona cada instancia con su artículo respectivo.
  - `num_articulo`: un identificador para cada artículo entregado por el **CEI**.
  - `estado`: análogo al estado de los *Espacios*. Opciones disponibles: Disponible, En préstamo, En reparación y Perdido.
##
- **Reserva**:
  - `profile`: Perfil del usuario que hizo la reserva.
  - `fh_reserva`: Marca la hora en la que se creó la instancia de reserva.
  - `fh_ini_reserva`
  - `fh_fin_reserva`
  - `estado_reserva`: Indica si la reserva aún está Pendiente, está Aceptada o está Rechazada.
  - `tipo`: Indica si se trata de la reserva de artículos o de un espacio.
  - `related`: campo que establece una relación *ManyToMany* entre la reserva y los artículos/el espacio reservado. Utiliza la librería `django-gm2m`.
##
- **Prestamo**:
  Análogo a las reservas, cambiando `fh_xxx_reserva` por `fh_xxx_préstamo`, además
  ahora los posibles `estado_prestamo` son: Vigente, Caducado, Perdido y Recibido.  
##

### Nuevos Requisitos Obtenidos:

### Modificaciones Realizadas:


### Propuestas a Futuro:

- Implementar vinculación con los GG.OO de Beauchef y sistema de sanciones en caso de que no se devuelvan los artículos o se devuelvan en mal estado.

- Implementar un sistema de verificación de que los alumnos realmente pertenecen a la facultad. Para esto, se propone hablar con la SAE durante enero para obtener a principio del siguiente ciclo una lista con los alumnos regulares de la facultad para autorizar sus cuentas.

- Integrar el sistema al Centro de Estudiantes, haciendo las gestiones con el nuevo CEI 2019 para subir la plataforma a un servidor y otorgarle un dominio, para comenzar con las pruebas del sistema.
