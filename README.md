# Sensor_mofo_MQTT

Descrição do Projeto
O Mofobot é um sistema inovador de monitoramento de IoT que utiliza um dispositivo ESP32 para detectar e alertar sobre as condições ideais para a proliferação de mofo. Este projeto foi concebido para resolver uma preocupação comum em muitos lares e ambientes: o risco de proliferação de mofo.

Em vez de reagir a um problema já existente, o Mofobot detecta as condições ideais para o mofo (alta umidade e gases) e alerta o usuário imediatamente. O objetivo é fornecer uma ferramenta acessível e eficaz que permite a tomada de ações preventivas, protegendo a saúde e a integridade de objetos e estruturas antes que o dano ocorra.

O backend, contido neste repositório, atua como a inteligência central do sistema, recebendo dados via MQTT e aplicando a lógica para o disparo de alertas.

Tecnologias Utilizadas
Python 3
paho-mqtt (Cliente MQTT)
requests (Para requisições HTTP)
python-dotenv (Para gerenciar credenciais de forma segura)

Como Executar o Projeto
Pré-requisitos: Certifique-se de ter o Python 3 instalado em sua máquina.
Clonar o Repositório: Use o comando git clone [URL_DO_SEU_REPOSITORIO] e depois navegue para a pasta com cd [NOME_DA_PASTA_DO_REPOSITORIO].
Configurar o Ambiente Virtual (Recomendado): Use python -m venv venv para criar o ambiente virtual e source venv/bin/activate para ativá-lo (no Windows, use venv\Scripts\activate).
Instalar as Dependências: Execute o comando pip install -r requirements.txt. Crie o arquivo requirements.txt na pasta do projeto com as linhas: paho-mqtt, requests e python-dotenv.

Configurar Credenciais:
Crie um arquivo chamado .env na mesma pasta.
Dentro dele, adicione a sua URL do Webhook do Make.com: ALERTA_MOLD_URL="[SUA_URL_DO_WEBHOOK]".
Adicione o arquivo .env ao seu .gitignore para garantir que a URL não seja exposta publicamente.
Executar o Script: Use o comando python main.py. O script pedirá que você insira os valores limiares de umidade e gás.
