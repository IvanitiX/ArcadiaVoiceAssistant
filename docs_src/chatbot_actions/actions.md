
## **actions** 


Archivo de acciones en Rasa para Arcadia Voice Assistant.
Contiene varias clases en Python que simbolizan nuestras acciones personalizadas. 

El archivo fue originalmente generado por el sistema de Rasa. Consulta la documentación en  <https://rasa.com/docs/rasa/custom-actions>

 --- 
 
### Lista de clases

[ActionsSettings](#ActionsSettings)
[ActionLightPrice](#ActionLightPrice)
[ActionTellTime](#ActionTellTime)
[ActionTellWeather](#ActionTellWeather)
[ActionThrowDice](#ActionThrowDice)

 --- 
 
### Clase **ActionLightPrice**
(hereda de [rasa\_sdk.interfaces.Action](https://rasa.com/docs/rasa/custom-actions))
      Clase para la acción de decir el precio de la luz  



#### Métodos
**name**(self) 
 Declaración de la acción
**Devuelve** string Nombre de la acción
**run**(self, dispatcher, tracker, domain)Ejecución de la acción.
Extrae de Internet, de la API de preciodelaluz.com, los valores máximos, mínimos
y actuales del precio de la luz.
**Devuelve a Arcadia** Devuelve la cadena explicando los valores anteriormente descritos.

  
 --- 
 
### Clase **ActionTellTime**
(hereda de [rasa\_sdk.interfaces.Action](https://rasa.com/docs/rasa/custom-actions))
      Clase para la acción de decir la hora  

#### Métodos
**name**(self)
Declaración de la acción
**Devuelve** string Nombre de la acción

**run**(self, dispatcher, tracker, domain)
Ejecución de la acción.
Extrae el datetime de este instante y extrae la hora
**Devuelve a Arcadia**: La hora en formato HH y MM (15:30 -> Son las 15 horas y 30 minutos)

 --- 
 
### Clase **ActionTellWeather**
(hereda de [rasa\_sdk.interfaces.Action](https://rasa.com/docs/rasa/custom-actions))
      Clase para la acción de decir el tiempo en una localidad  

#### Métodos
**name**(self)
Declaración de la acción
**Devuelve** string Nombre de la acción
**run**(self, dispatcher, tracker, domain)
Ejecución de la acción.
Extrae de la API de OpenWeatherMap a través de Internet y fabrica el reporte del tiempo en la ciudad pasada como entidad.
**Devuelve a Arcadia** Devuelve el reporte del tiempo para la ciudad.
**weather\_report\_sky** (self, code): Método que asocia el código con el mensaje que debería añadir
**Devuelve** weather\_report Mensaje a añadir al reporte


 --- 
 
### Clase **ActionThrowDice**
(hereda de [rasa\_sdk.interfaces.Action](https://rasa.com/docs/rasa/custom-actions)) 
      Clase para la acción de tirar el dado  

#### Métodos
**name**(self)
Declaración de la acción
**Devuelve** string Nombre de la acción
**run**(self, dispatcher, tracker, domain)
Ejecución de la acción.
Genera un número aleatorio entre 1 y 6
**Devuelve a Arcadia** Devuelve una cadena con el valor generado entre 1 y 6

 --- 
 
### Clase **ActionsSettings**
      Clase para la configuración de variables necesarias en las acciones  

#### Atributos

**NO\_CONNECTION\_TO\_INTERNET** : Frase para comunicar que no hay Internet
**OPENWEATHERMAP\_API\_KEY** : Clave API de OpenWeatherMap (https://openweathermap.org/api)







