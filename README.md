# Plataforma de Reservas CEI

*Plataforma para gestionar los préstamos de los artículos y espacios gestionados por el Centro de Alumnos de Ingeniería, para la Facultad de Cs. Físicas y Matemáticas, Universidad de Chile.*



### Dependencias:

- ***Django*** **2.1.3**
- ***Pillow*** **5.3.0**
- ***django-gm2m*** **0.6.1** \*

Todas estas librerías pueden instalarse automáticamente ejecutando `pip install -r requirements.txt`.

La librería ***django-gm2m*** se utiliza para realizar *reservas* y *préstamos* de *artículos* y *espacios* sin tener que crear modelos especiales (Por ejemplo, *ReservaEspacio*, *ReservaArtículo*, etc.).

La documentación de la librería se puede encontrar [aquí](https://django-gm2m.readthedocs.io/en/stable/).

### Modelo de Datos:



### Propuestas a Futuro:

- Implementar vinculación con los GG.OO de Beauchef y sistema de sanciones en caso de que no se devuelvan los artículos o se devuelvan en mal estado.
- Integrar el sistema al Centro de Estudiantes.
