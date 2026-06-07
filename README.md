# Rede de Sensores IoT

Simulação de uma rede de sensores IoT baseada no modelo de comunicação
publish/subscribe. O sistema permite cadastrar sensores e clientes, assinar
tópicos e distribuir leituras e alertas por meio de um broker.

## Requisitos

- Python 3
- Tkinter

O projeto não utiliza dependências externas. Em algumas distribuições Linux,
o Tkinter precisa ser instalado separadamente.

## Execução

```bash
python codigo.py
```

## Como usar

1. Cadastre um sensor informando ID, tipo, limite mínimo e limite máximo.
2. Cadastre um cliente.
3. Selecione o cliente e um tópico e clique em **Assinar tópico**.
4. Selecione o sensor e informe uma nova leitura.
5. A nova leitura é enviada aos clientes inscritos no tópico.
6. Se o valor atingir ou ultrapassar um dos limites, a mensagem é identificada
   como um alerta.

## Funcionamento

O código possui três partes principais:

- **Sensor:** armazena ID, tipo, limites, valor atual e tópico.
- **Broker:** relaciona cada tópico aos clientes inscritos.
- **Cliente:** assina tópicos e recebe as mensagens publicadas.

O fluxo de comunicação é:

```text
Sensor publica -> Broker identifica os inscritos -> Clientes recebem
```

Cada sensor possui seu próprio tópico, formado pelo tipo e pelo ID:

```text
temperatura/sensor1
temperatura/sensor2
```

O ID precisa ser único apenas entre sensores do mesmo tipo. Por exemplo, um
sensor de umidade e um sensor de velocidade podem utilizar o ID `1`, pois seus
tópicos serão diferentes:

```text
umidade/1
velocidade/1
```

Todas as novas leituras são publicadas. Quando a leitura é menor ou igual ao
limite mínimo, ou maior ou igual ao limite máximo, a mensagem também informa
qual limite foi atingido.

As unidades utilizadas são:

- temperatura em graus Celsius (`°C`);
- umidade em porcentagem (`%`);
- velocidade em quilômetros por hora (`km/h`).

Cada mensagem informa:

- data e hora;
- ID e tipo do sensor;
- valor da leitura e sua unidade;
- tópico da publicação.

Os alertas também apresentam o limite atingido e seu respectivo valor.
