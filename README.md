# VEXSQLi

![Screenshot_20](https://github.com/user-attachments/assets/755ab8a1-04f7-455d-8590-c7dd3afc50cb)

**VEXSQLi** es una herramienta avanzada para la generación de payloads de inyección SQL (SQLi) utilizando procesamiento de lenguaje natural (NLP). Esta herramienta permite crear variantes ofuscadas de payloads SQLi a partir de un conjunto base de payloads, aplicando técnicas de ofuscación para evadir filtros y detección.

## Características

- Generación de payloads SQLi con variaciones de nombres y verbos.
- En busqueda de hacer bypass a los waf he logrado dar en el clavo teniendo exito en caza de recompensas con caracteres cuneiformes.
- Ofuscación de payloads usando técnicas como codificación en Base64, Unicode y caracteres homoglifos.
- Inserción de comentarios SQL y concatenación de cadenas para mayor complejidad.
- Configuración de parámetros de entrada y salida a través de la línea de comandos.

## Instalación

Para usar VEXSQLi, necesitarás instalar las siguientes dependencias:

```bash
pip install spacy colorama
python -m spacy download en_core_web_sm
```

## Uso
Para ejecutar la herramienta, utiliza el siguiente comando:

```bash
python vexsqli.py --payloads <archivo_payloads> --out <archivo_salida>
```

Donde:

- <archivo_payloads> es el archivo que contiene los payloads base (uno por línea).
- <archivo_salida> es el archivo donde se guardarán los payloads generados.

## Ejemplo

Si tienes un archivo payloads.txt con los payloads base y deseas guardar los resultados en payloads_generados.txt, ejecuta:

```bash
python vexsqli.py --payloads payloads.txt --out payloads_generados.txt
```

La herramienta generará los payloads y los guardará en el archivo de salida, esperando 5 segundos entre cada generación.

## Dependencias

- spacy: Para procesamiento de lenguaje natural.
- colorama: Para colores en la consola.
- en_core_web_sm: Modelo de spaCy para el procesamiento del lenguaje.

## Contribuciones

Las contribuciones a VEXSQLi son bienvenidas. Si deseas contribuir, por favor abre un issue o un pull request en el repositorio.

## Licencia

VEXSQLi es un software de código abierto. Puedes utilizarlo bajo los términos de la licencia MIT.
