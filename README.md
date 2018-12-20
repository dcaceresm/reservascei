# Plataforma de Reservas CEI

*Plataforma para gestionar los préstamos de los artículos y espacios gestionados por el Centro de Alumnos de Ingeniería, para la Facultad de Cs. Físicas y Matemáticas, Universidad de Chile.*

### Sobre el Proyecto:
Debido a un robo ocurrido en la casa del ***CEI*** el año 2017, perdió la base de datos con los artículos y espacios, además del sistema para realizar préstamos de los mismos. Para compensar esta pérdida, el primer semestre de 2018 se les propuso a los alumnos del curso **CC4401 Ingeniería de Software** implementar un nuevo sistema, a modo de ejercicio pedagógico.

Aunque en esta implementación se produjo mucho código y diversas soluciones de calidad, los requerimientos apuntados estaban lejos de asemejarse a las reales necesidades de este sistema. Así, durante el transcurso del segundo semestre, se retomó este trabajo, se obtuvieron nuevos requerimientos y se realizaron modificaciones al sistema para acercarlo a la realidad.

Cabe notar que actualmente las reservas se realizan por correo, por lo que llevar esta plataforma a los estudiantes permitiría ordenar los pedidos y mantener una base de datos persistente para los fines que el ***CEI*** estime conveniente; entre ellos se tiene como posibles uso el realizar estadísticas sobre los artículos pedidos, mantener un registro de sanciones en caso de pérdidas o maltrato de las existencias, etc.

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

### Nueva Información Obtenida:
A partir de las reuniones desarrolladas, se obtuvo la siguiente información sobre lo que se debe desarrollar en el sistema:
- La plataforma desarrollada en **CC4401** sólo permite prestar 1 artículo a la vez. Esto no es consistente con las necesidades reales del sistema puesto que se piden varios artículos partiendo de una sola reserva (Por ejemplo, se piden 20 toldos para un evento, caso en el que no tiene sentido hacer 20 reservas).
- Se debe limitar las reservas al horario en el que se encuentra abierta la *casa CEI*, esto es, de 9:00 AM a 17:45 PM, con el fin de que se alcancen a devolver los artículos en este intervalo de tiempo.
- Por el momento sólo se puede reservar la *Sala de Reuniones 1*. El *Quincho* y la *Sala de Reuniones 2* se encuentran en reparaciones.
- Cuando el *Quincho* se encuentre habilitado, se debe pedir con una semana (como mínimo) de anticipación. 2 días antes se debe firmar una carta de compromiso y realizar el pago de garantía.
- El sistema de administración desarrollado en **CC4401** resulta demasiado complejo para el usuario final que administrará las reservas, por lo que se debe realizar un sistema más simple con las funciones justas y necesarias.
- Aprovechando la persistencia de los datos generados, se debe pensar en un sistema para sancionar a los alumnos que inclumplan las normas de uso de los artículos o los entreguen en mal estado. Esto incluye las peticiones por parte de Grupos Organizados, donde se propone sancionar al grupo completo.

### Modificaciones Realizadas:
- Se toma como base la solución implementada por el *Grupo 6* de **CC4401** para la primera iteración de desarrollo. Aunque no implementa todos los requisitos entregados durante el desarrollo del curso, la forma en que está organizado el modelo de datos y como está estructurado el código lo convierten en el candidato ideal para comenzar el desarrollo de este sistema.
- La primera modificación realizada corresponde a la corrección de todos los *bugs* del sistema: No era posible hacer login y algunas vistas no eran accesibles. Además se agregó un archivo `requirements.txt` para facilitar la instalación de dependencias.
- Se modificó el esquema de la base de datos. Para esto, se creó el modelo **InstanciaArtículo**; luego, para poder generar reservas de múltiples artículos a la vez, se utilizó la librería `django-gm2m`. Esta librería permite generar relaciones ManyToMany sin especificar el modelo con el que se genera la relación. Esto permite guardar en un mismo campo de las Reservas/Préstamos el espacio o los múltiples artículos a reservar. Uno de los beneficios de utilizar esta librería es que los objetos creados en **Python** son iterables, por lo que se pueden acceder en las vistas y en los templates.
- Se creó una vista simplificada enfocada únicamente en la aceptación de Reservas y la recepción de Préstamos, con el fin de recrear las acciones que hoy en día se realizan por correo dentro de la plataforma.
- Se implementaron las reservas de artículos. Se verifica en tiempo real (haciendo una petición AJAX) el horario ingresado por el usuario para su reserva, con tal de no interferir con el resto, mostrándole la cantidad efectiva de instancias que puede reservar; las que además no se escogen a mano: sólo se pregunta cuántas instancias se quieren reservar.
- Se implementaron las reservas de espacios tomando como base la librería [FullCalendar](https://fullcalendar.io/). Se utilizó una vista de semana completa, y se verifica que no haya colisiones de horario al reservar.
### Propuestas a Futuro:

- Implementar vinculación con los GG.OO de Beauchef y sistema de sanciones en caso de que no se devuelvan los artículos o se devuelvan en mal estado.

- Implementar un sistema de verificación de que los alumnos realmente pertenecen a la facultad. Para esto, se propone hablar con la SAE durante enero para obtener a principio del siguiente ciclo una lista con los alumnos regulares de la facultad para autorizar sus cuentas.

- Integrar el sistema al Centro de Estudiantes, haciendo las gestiones con el nuevo CEI 2019 para subir la plataforma a un servidor y otorgarle un dominio, para comenzar con las pruebas del sistema.
