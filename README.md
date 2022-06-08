# Trabajo de Fin de Grado: *Asistente Virtual Modular usando APIs libres y de Código Abierto* 
## (también conocido como *Arcadia Voice Assistant*)

### Autor: Iván Valero Rodríguez
### Tutor: Pablo García Sánchez
___

## Generación de la documentación

La documentación de este proyecto está realizada con `LaTeX`, por lo
tanto para generar el archivo PDF necesitaremos instalar `TeXLive` en
nuestra distribución.

Una vez instalada, tan solo deberemos situarnos en el directorio `doc` y ejecutar:

`
$ pdflatex proyecto.tex
`

Seguido por

    bibtex proyecto
    
y de nuevo

    pdflatex proyecto.tex

O directamente

    make
    

---

## Uso de Arcadia

Para poder usar a Arcadia, necesitaremos hacer unos cuantos pasos.

> **Warning**
> Las acciones de la instalación se harán en la carpeta `src`

1. Instalar NanoTTS. Para ello, hay que seguir los pasos de su repositorio original: https://github.com/gmn/nanotts

> **Note**
> Posiblemente necesites añadir al `PATH` la ubicación de la carpeta de NanoTTS usando `export PATH=<ubicacion-NanoTTS>:$PATH`. Esto tendrás que poner cada vez que se ejecute un bash o escribiendo en `./.bashrc~` este comando para ahorrarte la repetición

2. Activar el Entorno Virtual con `source venv/bin/activate`. Este entorno dispone de Python 3.9 y las dependencias necesarias para pdoer ejecutar el sistema.

3. Ejecutar `python boot.py`