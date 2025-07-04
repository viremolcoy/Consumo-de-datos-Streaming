# Consumo-de-datos-Streaming

Instalaciones:

-Instalar python
-Instalar Ngrok

Instalaciones desde consola:

-pip install flask
-pip install pandas
-pip install streamlit
-pip install plotly 
-pip matplotlib 
-pip install matplotlib seaborn scikit-learn


Pasos para recibir los datos en Streaming.


1- Correr el webhook desde consola de VSCode
python webhook_receiver.py  

2-  Ngrok, Registrarse, Y en la consola correr el puerto donde esta el webhook, código:
ngrok http 5000 

3- Copiar url que nos entrega Ngrok

Algo así 
Forwarding                    https://a8ed-190-163-215-31.ngrok-free.app 
A esa url la añadimos /webhook

https://a8ed-190-163-215-31.ngrok-free.app/webhook

Esta ultima URL la registramos en el sistema que nos envía los datos en streaming, en este caso el sistema de Duoc
https://bdrealtimeescuelait.duoc.cl/
