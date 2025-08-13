import paho.mqtt.client as mqtt
import json
import requests
import os
import time

# Configurações do broker MQTT
MQTT_BROKER_HOST = "test.mosquitto.org"

# Tópicos que o ESP32 PUBLICA (o script vai ASSINAR)
MQTT_TOPIC_UMIDADE_ATUAL = "sensor_mofo/umidadeatual"
MQTT_TOPIC_GASES_ATUAL = "sensor_mofo/gasesatual"
MQTT_TOPIC_ALERTA_SITUACAO = "sensor_mofo/alertasituacao"
# Tópicos que o script PUBLICA (o ESP32 vai ASSINAR)
MQTT_TOPIC_LIMIAR_UMIDADE = "sensor_mofo/limiar_umidade"
MQTT_TOPIC_LIMIAR_GASES = "sensor_mofo/limiar_gases"

# URL do Webhook do Make.com para o alerta
ALERTA_MOLD_URL = "https://hook.us2.make.com/frgo9zwo1p0e9hi2qeueqcv2qy4gvl2d"

# Variável de estado para controlar o tempo entre alertas
last_alert_time = 0 
COOLDOWN_MINUTES = 1440 # 24 horas

# Variáveis globais para armazenar as últimas leituras
last_umidade = -1.0
last_gas_raw = -1

def set_thresholds(client):
    """Solicita e publica os novos valores de limiar para o ESP32."""
    try:
        limiar_umidade = float(input("Digite o limiar de umidade (ex: 65.0): "))
        limiar_gas = int(input("Digite o limiar de gás (ex: 400): "))
        
        client.publish(MQTT_TOPIC_LIMIAR_UMIDADE, str(limiar_umidade), qos=1)
        client.publish(MQTT_TOPIC_LIMIAR_GASES, str(limiar_gas), qos=1)
        print("Novos limiares publicados com sucesso! O ESP32 foi notificado.")
        
    except ValueError:
        print("Erro: Por favor, digite um número válido.")

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Conectado ao broker MQTT com sucesso!")
        client.subscribe(MQTT_TOPIC_UMIDADE_ATUAL)
        client.subscribe(MQTT_TOPIC_GASES_ATUAL)
        client.subscribe(MQTT_TOPIC_ALERTA_SITUACAO)
        
        set_thresholds(client)
    else:
        print(f"Falha na conexão, código de retorno: {rc}")

def on_message(client, userdata, msg):
    global last_umidade, last_gas_raw, last_alert_time
    try:
        payload_str = msg.payload.decode()
        current_time = time.time()

        if msg.topic == MQTT_TOPIC_UMIDADE_ATUAL:
            data = json.loads(payload_str)
            last_umidade = data.get("umidade", -1.0)
        elif msg.topic == MQTT_TOPIC_GASES_ATUAL:
            data = json.loads(payload_str)
            last_gas_raw = data.get("mq135_raw", -1)

        if msg.topic == MQTT_TOPIC_ALERTA_SITUACAO:
            data = json.loads(payload_str)
            status_ambiente = data.get("status")

            if status_ambiente == "Alerta de Mofo!" and (last_alert_time == 0 or (current_time - last_alert_time) > (COOLDOWN_MINUTES * 60)):
                if last_umidade != -1.0 and last_gas_raw != -1:
                    print("------------------------------------------")
                    print(f"*** ALERTA DETECTADO! Enviando notificação para o Make.com.")
                    payload_make = {
                        "value1": "Alerta_Mofo!",
                        "value2": last_umidade,
                        "value4": last_gas_raw,
                    }
                    requests.post(ALERTA_MOLD_URL, json=payload_make)
                    last_alert_time = current_time
                    print(f"Tempo do último alerta atualizado para: {time.ctime(last_alert_time)}")
                else:
                    print("Alerta detectado, mas aguardando dados dos sensores. Nenhuma notificação enviada.")

            elif status_ambiente == "Ambiente seguro!":
                print("Ambiente seguro detectado. Cooldown ativo.")

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

# Inicializa o cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_BROKER_HOST, 1883, 60)
    client.loop_forever()
except Exception as e:
    print(f"Não foi possível conectar ao broker MQTT: {e}")