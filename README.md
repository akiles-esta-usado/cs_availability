# Prototipo de transmisión de métrica de disponibilidad

Prototipo creado para el ramo "Redes de Sensores".


## Inicialización del sistema

El script `init.sh` configura el sistema y el proyecto para poder realizar las capturas.

~~~bash
# Esto configura y descarga dependencias
./init.sh

# Hay que activar el entorno de programación.
conda activate SENSORES

# Ahora se puede ejecutar el script de captura
python capturar_foto_2.py
~~~



## Credenciales de ThingSpeak

Las credenciales se almacenan en un archivo `credentials.toml` con el siguiente formato:

~~~toml
# credentials.toml
[secrets]
api_key = "LLAVE DE LA API"
~~~
