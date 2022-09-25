# *Arcadia Voice Assistant*
## (También conocido como el Trabajo de Fin de Grado: *Asistente Virtual Modular usando APIs libres y de Código Abierto* )

> **Note**
>
> **¡El repositorio está disponible para que hagáis cambios para HacktoberFest!** Abre issues durante el mes de octubre, haz cambios, colabora con el proyecto...
> ¡y consigue tu camiseta*!
>
> (* Sólo PRs válidos entre el 1 y el 31 de Octubre. Consulta las condiciones [aquí](https://hacktoberfest.com/participation/) )

![Logo](Proyecto.png)



Autor: Iván Valero Rodríguez [:octocat: (@IvanitiX)](https://github.com/IvanitiX)

Tutor: Pablo García Sánchez [:octocat: (@fergunet)](https://github.com/fergunet)

(Trabajo defendido el 14 de Julio de 2022, con nota final de 9'7/10)
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

¡Ahora en Docker!

Para ejecutar a Arcadia desde Docker, hay que seguir unos pocos pasos:

1. Instala PortAudio en tu sistema.

> **Note**
>
> Dependiendo del Sistema Operativo, la manera de instalar PortAudio varía:
> - En Windows, consulta http://www.portaudio.com/docs/v19-doxydocs/tutorial_start.html
> - En Linux, mira el paquete portaudio en pkgs.org
> - En Mac, `brew install portaudio`

2. Instala docker y docker-compose si no lo tienes.

> **Note**
>
> Consulta https://docs.docker.com/get-docker/ para más información.

3. En la carpeta del proyecto, ejecuta estos comandos:

```bash
docker-compose build
docker-compose up
```

4. Accede a una shell de Arcadia Client (Se puede apreciar como `arcadia_client` o `tfg_asistente_modular_arcadia_client_1`) y ejecuta `python boot.py`

> **Note**
>
> En Visual Studio Code se puede dar Botón Derecho > Attach Shell.
> Desde la terminal, se puede poner una terminal desde el contenedor apuntando a bash como entrypoint.
> Por ejemplo, `docker run -it --entrypoint bash arcadia_client`
