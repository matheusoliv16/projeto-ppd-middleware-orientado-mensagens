# Rede de Sensores IoT

Projeto simples de Middleware Orientado a Mensagens para a disciplina de
Programacao Paralela e Distribuida.

## Executar

O programa usa apenas bibliotecas do Python.

```bash
python codigo.py
```

## Como testar

1. Cadastre um sensor informando ID, tipo e limites.
2. Cadastre um cliente.
3. Selecione o cliente e um topico e clique em **Assinar topico**.
4. Selecione o sensor e informe uma nova leitura.
5. Se o valor atingir o limite minimo ou maximo, o cliente recebe a mensagem.

## Funcionamento

O codigo possui tres partes principais:

- **Sensor:** guarda ID, tipo, limites, valor atual e topico.
- **Broker:** e o dicionario `broker`, que relaciona cada topico aos clientes
  inscritos.
- **Cliente:** escolhe os topicos e recebe as mensagens publicadas.

O fluxo e:

```text
Sensor publica -> Broker verifica os inscritos -> Cliente recebe
```

Sensores do mesmo tipo podem ser cadastrados com IDs diferentes. Cada sensor
possui seu proprio topico, por exemplo:

```text
temperatura/sensor1
temperatura/sensor2
```

## Explicacao para a apresentacao

Quando a leitura e alterada, o programa compara o valor com os limites. Se um
limite for atingido, a funcao `publicar` envia a mensagem para o Broker. O
Broker percorre apenas os clientes inscritos naquele topico e adiciona a
mensagem na lista de cada um.

Isso representa o modelo **publish/subscribe**: o sensor publica, o cliente
assina e o Broker faz a intermediacao.
