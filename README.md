# **Whale**

## indice

* [Requisitos](#Requisitos "ir a requisitos de instalacion")
* [Instalacion](#Instalacion "ir a la guia de instalacion")
	+ [Clonar el repositorio](#Clonando-el-repositorio "ir a guia de clonacion")
	+ [Configurar el entorno de desarrollo](#configurar-el-entorno-de-desarrollo "ir a guia de configuracion para desarrollo") (opcional)
		- [Configurar VS code](#configurando-visual-studio-code "guia de vscode") (opcional)
		- [Configurar PyCharm](#configurando-pycharm "guia de pycharm") (opcional)
	+ [Instalar dependencias](#instalar-dependencias "instalando dependencias")
* [Uso de los Scripts](#ejecutar-los-scripts "ir a guia uso")
* [notas adicionales](#notas-importantes "ver las notas adicionales")

## Requisitos

* [**Visual Studio Code**](https://code.visualstudio.com/): (opcional) editor de texto con soporte de python y multiples extensiones.
* [**JetBrains**](https://www.jetbrains.com/es-es/pycharm/): (opcional, recomendado) IDE diseñado para python.
* [**git**](https://git-scm.com/): nescesario para clonar los repositorios.
* [**python 3**](https://www.python.org/downloads/): Interprete oficial de python,tambien se puede usar otra distribucion como anaconda.
* [**WSL 2(Windows)**](https://docs.microsoft.com/en-us/windows/wsl/compare-versions#whats-new-in-wsl-2) subsistema de windows para linux.

## Instalacion

## Clonando el repositorio

mediante la terminal preferida clonar la direccion de este repositorio, ejemplo:

```bash
git clone https://github.com/pyloguna/qr_id.git
```

`nota: esto clonara el repositorio en una subcarpeta en el directorio actual, por lo que es importante conocer donde se clona el proyecto`

## configurar el entorno de desarrollo

## configurando visual studio code

una vez instalado en la categoria de extensiones podemos instalar la extension del idioma [español](https://marketplace.visualstudio.com/items?itemName=MS-CEINTL.vscode-language-pack-es)(opcional) y la extension de [python](https://marketplace.visualstudio.com/items?itemName=ms-python.python), cada una provee su propia guia de uso extendida de ser nescesario

## configurando pycharm

pycharm provee su propia guia de instalacion inicial, simplemente basta con escoger el entorno de python y el folder deseado

## instalar dependencias

mediante el interprete de python en la carpeta destino(carpeta de login) ejecutar en una linea de comandos

```bash
python -m pip install -r requirements.txt
```

si el comando `pip` reporta errores de instalacion, puede que se requieran permisos elevados, se puede solucionar agregando el parametro `--user` al final del comando, o ejecutandolo con permisos elevados.

>*`si los paquetes no se muestran a pesar de estar instalados verifique que se ejecutan como modulo de python, sino se usara el pip del python incluido en el path.`*
>si se desea conocer mas sobre el uso del gestor de paquetes se puede visitar su enlace : [**pip**](https://pypi.org/project/pip/)

## ejecutar los scripts

en una linea de comandos en el folder del proyecto realice las siguientes acciones:

```bash
cd whale
python manage.py migrate
python manage.py runserver
```

Si todo va bien, notara una salida como esta:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
September 29, 2020 - 19:11:49
Django version 3.0.8, using settings 'portal.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

opcionalmente se dispone de un archivo docker compose por si desea usar docker y no la guia anterior

## Notas Importantes

---

## Autenticacion OAuth2 con Google

`nota: actualmente se encuentra deshabilitado el soporte para oauth,
a pesar de esto se planea rehabilitar con social auth:
https://python-social-auth.readthedocs.io/en/latest/configuration/django.html`

Para el soporte de login mediante google se requiere en las variables de entorno GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET
Sin un cliente y secreto oauth2, no se registran en la base de datos ni podran autenticarse los usuarios mediante google
aunque se pueden agregar, tambien una vez registrados su contraseña por defecto es 1234,
y el email es el mismo usado en el login de google, aunque pueden seguir usuando el login de google si así lo desean.  
para mas información ver la [Documentacion de Google](https://developers.google.com/identity/protocols/oauth2 "Oauth2 Google")
