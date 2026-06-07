import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime


# Dados do programa
sensores = []
clientes = []

# O Broker guarda os topicos e os clientes inscritos em cada um
broker = {}


def adicionar_sensor():
    nome = entrada_sensor.get().strip()
    tipo = combo_tipo.get()

    try:
        minimo = float(entrada_minimo.get())
        maximo = float(entrada_maximo.get())
    except ValueError:
        messagebox.showerror("Erro", "Os limites devem ser numeros.")
        return

    if not nome:
        messagebox.showerror("Erro", "Informe o ID do sensor.")
        return

    if any(sensor["nome"] == nome for sensor in sensores):
        messagebox.showerror("Erro", "Ja existe um sensor com esse ID.")
        return

    if minimo >= maximo:
        messagebox.showerror("Erro", "O limite minimo deve ser menor que o maximo.")
        return

    topico = f"{tipo.lower()}/{nome}"

    sensor = {
        "nome": nome,
        "tipo": tipo,
        "minimo": minimo,
        "maximo": maximo,
        "valor": 0,
        "topico": topico,
    }

    sensores.append(sensor)
    broker[topico] = []

    tabela_sensores.insert(
        "",
        "end",
        iid=nome,
        values=(nome, tipo, minimo, maximo, 0, topico),
    )

    atualizar_topicos()
    entrada_sensor.delete(0, tk.END)


def alterar_leitura():
    selecionado = tabela_sensores.selection()

    if not selecionado:
        messagebox.showerror("Erro", "Selecione um sensor.")
        return

    try:
        novo_valor = float(entrada_valor.get())
    except ValueError:
        messagebox.showerror("Erro", "Informe um valor numerico.")
        return

    nome = selecionado[0]
    sensor = next(sensor for sensor in sensores if sensor["nome"] == nome)
    sensor["valor"] = novo_valor

    tabela_sensores.item(
        nome,
        values=(
            sensor["nome"],
            sensor["tipo"],
            sensor["minimo"],
            sensor["maximo"],
            sensor["valor"],
            sensor["topico"],
        ),
    )

    # O sensor publica apenas quando atinge um dos limites
    if novo_valor <= sensor["minimo"] or novo_valor >= sensor["maximo"]:
        publicar(sensor)
        status.config(text="Alerta enviado ao Broker!", fg="red")
    else:
        status.config(text="Valor normal. Nenhuma mensagem enviada.", fg="green")


def publicar(sensor):
    if sensor["valor"] <= sensor["minimo"]:
        tipo_alerta = "LIMITE MINIMO ATINGIDO"
        limite = sensor["minimo"]
        comparacao = "abaixo ou igual ao minimo"
    else:
        tipo_alerta = "LIMITE MAXIMO ATINGIDO"
        limite = sensor["maximo"]
        comparacao = "acima ou igual ao maximo"

    mensagem = (
        f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] "
        f"ALERTA: {tipo_alerta} | "
        f"Sensor: {sensor['nome']} | "
        f"Tipo: {sensor['tipo']} | "
        f"Leitura: {sensor['valor']} ({comparacao}) | "
        f"Limite: {limite} | "
        f"Topico: {sensor['topico']}"
    )

    # O Broker entrega a mensagem somente aos clientes inscritos
    for cliente in broker[sensor["topico"]]:
        cliente["mensagens"].append(mensagem)

    mostrar_mensagens()


def adicionar_cliente():
    nome = entrada_cliente.get().strip()

    if not nome:
        messagebox.showerror("Erro", "Informe o ID do cliente.")
        return

    if any(cliente["nome"] == nome for cliente in clientes):
        messagebox.showerror("Erro", "Ja existe um cliente com esse ID.")
        return

    cliente = {"nome": nome, "topicos": [], "mensagens": []}
    clientes.append(cliente)
    lista_clientes.insert(tk.END, nome)
    entrada_cliente.delete(0, tk.END)


def atualizar_topicos():
    lista_topicos.delete(0, tk.END)

    for topico in broker:
        lista_topicos.insert(tk.END, topico)


def assinar_topico():
    cliente_selecionado = lista_clientes.curselection()
    topico_selecionado = lista_topicos.curselection()

    if not cliente_selecionado or not topico_selecionado:
        messagebox.showerror("Erro", "Selecione um cliente e um topico.")
        return

    nome_cliente = lista_clientes.get(cliente_selecionado[0])
    topico = lista_topicos.get(topico_selecionado[0])
    cliente = next(cliente for cliente in clientes if cliente["nome"] == nome_cliente)

    if topico not in cliente["topicos"]:
        cliente["topicos"].append(topico)
        broker[topico].append(cliente)

    mostrar_mensagens()
    messagebox.showinfo("Sucesso", f"{nome_cliente} assinou o topico {topico}.")


def mostrar_mensagens(evento=None):
    selecionado = lista_clientes.curselection()
    caixa_mensagens.delete("1.0", tk.END)

    if not selecionado:
        return

    nome = lista_clientes.get(selecionado[0])
    cliente = next(cliente for cliente in clientes if cliente["nome"] == nome)

    caixa_mensagens.insert(
        tk.END,
        "Topicos assinados: " + ", ".join(cliente["topicos"]) + "\n\n",
    )

    for mensagem in cliente["mensagens"]:
        caixa_mensagens.insert(tk.END, mensagem + "\n")


# Interface grafica
janela = tk.Tk()
janela.title("Rede de Sensores IoT")
janela.geometry("1050x720")
janela.minsize(900, 650)
janela.configure(bg="#eef2f7")

AZUL = "#2457a6"
AZUL_ESCURO = "#173b70"
FUNDO = "#eef2f7"
BRANCO = "#ffffff"
TEXTO = "#263238"

estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure(
    "Treeview",
    background=BRANCO,
    fieldbackground=BRANCO,
    foreground=TEXTO,
    rowheight=28,
    font=("Segoe UI", 10),
)
estilo.configure(
    "Treeview.Heading",
    background=AZUL,
    foreground=BRANCO,
    font=("Segoe UI", 10, "bold"),
    padding=7,
)
estilo.map(
    "Treeview",
    background=[("selected", "#b8d4ff")],
    foreground=[("selected", "#000000")],
)
estilo.configure(
    "TNotebook",
    background=FUNDO,
    borderwidth=0,
)
estilo.configure(
    "TNotebook.Tab",
    font=("Segoe UI", 11, "bold"),
    padding=(22, 10),
    background="#dbe4f0",
    foreground=AZUL_ESCURO,
)
estilo.map(
    "TNotebook.Tab",
    background=[("selected", BRANCO)],
    foreground=[("selected", AZUL)],
)

cabecalho = tk.Frame(janela, bg=AZUL_ESCURO)
cabecalho.pack(fill="x")

tk.Label(
    cabecalho,
    text="Rede de Sensores IoT",
    font=("Segoe UI", 21, "bold"),
    bg=AZUL_ESCURO,
    fg=BRANCO,
).pack(anchor="w", padx=22, pady=(13, 0))

tk.Label(
    cabecalho,
    text="Middleware orientado a mensagens",
    font=("Segoe UI", 10),
    bg=AZUL_ESCURO,
    fg="#cbdaf0",
).pack(anchor="w", padx=24, pady=(0, 13))

abas = ttk.Notebook(janela)
abas.pack(fill="both", expand=True, padx=18, pady=14)

aba_sensores = tk.Frame(abas, bg=FUNDO)
aba_clientes = tk.Frame(abas, bg=FUNDO)
abas.add(aba_sensores, text="Sensores")
abas.add(aba_clientes, text="Clientes")

# Area dos sensores
frame_sensor = tk.LabelFrame(
    aba_sensores,
    text="  Cadastro e leitura dos sensores  ",
    font=("Segoe UI", 11, "bold"),
    bg=BRANCO,
    fg=AZUL_ESCURO,
    padx=14,
    pady=12,
    bd=1,
    relief="solid",
)
frame_sensor.pack(fill="both", expand=True, padx=8, pady=8)

tk.Label(frame_sensor, text="ID", bg=BRANCO, fg=TEXTO).grid(
    row=0, column=0, sticky="w"
)
entrada_sensor = tk.Entry(frame_sensor, width=13, relief="solid", bd=1)
entrada_sensor.grid(row=1, column=0, padx=(0, 10), pady=(3, 8), ipady=4)

tk.Label(frame_sensor, text="Tipo", bg=BRANCO, fg=TEXTO).grid(
    row=0, column=1, sticky="w"
)
combo_tipo = ttk.Combobox(
    frame_sensor,
    values=["Temperatura", "Umidade", "Velocidade"],
    state="readonly",
    width=16,
)
combo_tipo.current(0)
combo_tipo.grid(row=1, column=1, padx=(0, 10), pady=(3, 8), ipady=3)

tk.Label(frame_sensor, text="Limite minimo", bg=BRANCO, fg=TEXTO).grid(
    row=0, column=2, sticky="w"
)
entrada_minimo = tk.Entry(frame_sensor, width=13, relief="solid", bd=1)
entrada_minimo.grid(row=1, column=2, padx=(0, 10), pady=(3, 8), ipady=4)

tk.Label(frame_sensor, text="Limite maximo", bg=BRANCO, fg=TEXTO).grid(
    row=0, column=3, sticky="w"
)
entrada_maximo = tk.Entry(frame_sensor, width=13, relief="solid", bd=1)
entrada_maximo.grid(row=1, column=3, padx=(0, 10), pady=(3, 8), ipady=4)

tk.Button(
    frame_sensor,
    text="Adicionar sensor",
    command=adicionar_sensor,
    bg=AZUL,
    fg=BRANCO,
    activebackground=AZUL_ESCURO,
    activeforeground=BRANCO,
    relief="flat",
    padx=14,
    pady=5,
    cursor="hand2",
).grid(
    row=1, column=4, padx=5, pady=(3, 8)
)

colunas = ("id", "tipo", "minimo", "maximo", "valor", "topico")
tabela_sensores = ttk.Treeview(
    frame_sensor, columns=colunas, show="headings", height=14
)

for coluna, texto in zip(
    colunas, ["ID", "Tipo", "Minimo", "Maximo", "Valor", "Topico"]
):
    tabela_sensores.heading(coluna, text=texto)
    largura = 220 if coluna == "topico" else 105
    tabela_sensores.column(coluna, width=largura, anchor="center")

tabela_sensores.grid(
    row=2, column=0, columnspan=5, pady=(4, 12), sticky="nsew"
)

tk.Label(frame_sensor, text="Nova leitura:", bg=BRANCO, fg=TEXTO).grid(
    row=3, column=0, sticky="e"
)
entrada_valor = tk.Entry(frame_sensor, width=13, relief="solid", bd=1)
entrada_valor.grid(row=3, column=1, sticky="w", padx=8, ipady=4)
tk.Button(
    frame_sensor,
    text="Atualizar leitura",
    command=alterar_leitura,
    bg="#e8eef8",
    fg=AZUL_ESCURO,
    activebackground="#d5e2f5",
    relief="flat",
    padx=12,
    pady=5,
    cursor="hand2",
).grid(row=3, column=2, sticky="w")
status = tk.Label(
    frame_sensor,
    text="Selecione um sensor e altere sua leitura.",
    bg=BRANCO,
    fg="#607080",
    font=("Segoe UI", 9, "italic"),
)
status.grid(row=3, column=3, columnspan=2, sticky="w", padx=10)
frame_sensor.columnconfigure(4, weight=1)
frame_sensor.rowconfigure(2, weight=1)

# Area dos clientes
frame_cliente = tk.LabelFrame(
    aba_clientes,
    text="  Clientes e mensagens recebidas  ",
    font=("Segoe UI", 11, "bold"),
    bg=BRANCO,
    fg=AZUL_ESCURO,
    padx=14,
    pady=12,
    bd=1,
    relief="solid",
)
frame_cliente.pack(fill="both", expand=True, padx=8, pady=8)

tk.Label(frame_cliente, text="ID do cliente:", bg=BRANCO, fg=TEXTO).grid(
    row=0, column=0, sticky="w"
)
entrada_cliente = tk.Entry(frame_cliente, width=18, relief="solid", bd=1)
entrada_cliente.grid(row=0, column=1, padx=8, ipady=4, sticky="w")
tk.Button(
    frame_cliente,
    text="Adicionar cliente",
    command=adicionar_cliente,
    bg=AZUL,
    fg=BRANCO,
    activebackground=AZUL_ESCURO,
    activeforeground=BRANCO,
    relief="flat",
    padx=12,
    pady=5,
    cursor="hand2",
).grid(
    row=0, column=2, sticky="w"
)

tk.Label(
    frame_cliente,
    text="Clientes",
    font=("Segoe UI", 10, "bold"),
    bg=BRANCO,
    fg=TEXTO,
).grid(row=1, column=0, columnspan=2, pady=(14, 5), sticky="w")
lista_clientes = tk.Listbox(
    frame_cliente,
    height=16,
    exportselection=False,
    relief="solid",
    bd=1,
    selectbackground=AZUL,
    selectforeground=BRANCO,
    font=("Segoe UI", 10),
)
lista_clientes.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=(0, 10))
lista_clientes.bind("<<ListboxSelect>>", mostrar_mensagens)

tk.Label(
    frame_cliente,
    text="Topicos disponiveis",
    font=("Segoe UI", 10, "bold"),
    bg=BRANCO,
    fg=TEXTO,
).grid(
    row=1, column=2, pady=(14, 5), sticky="w"
)
lista_topicos = tk.Listbox(
    frame_cliente,
    height=16,
    exportselection=False,
    relief="solid",
    bd=1,
    selectbackground=AZUL,
    selectforeground=BRANCO,
    font=("Segoe UI", 10),
)
lista_topicos.grid(row=2, column=2, sticky="nsew", padx=(0, 10))

tk.Button(
    frame_cliente,
    text="Assinar topico",
    command=assinar_topico,
    bg="#e8eef8",
    fg=AZUL_ESCURO,
    activebackground="#d5e2f5",
    relief="flat",
    padx=12,
    pady=5,
    cursor="hand2",
).grid(
    row=3, column=2, pady=(7, 0), sticky="w"
)

tk.Label(
    frame_cliente,
    text="Mensagens recebidas",
    font=("Segoe UI", 10, "bold"),
    bg=BRANCO,
    fg=TEXTO,
).grid(
    row=1, column=4, pady=(14, 5), sticky="w"
)
caixa_mensagens = tk.Text(
    frame_cliente,
    width=55,
    height=20,
    bg="#f7f9fc",
    fg=TEXTO,
    relief="solid",
    bd=1,
    padx=10,
    pady=8,
    font=("Consolas", 9),
    wrap="word",
)
caixa_mensagens.grid(row=2, column=4, rowspan=2, sticky="nsew")

frame_cliente.columnconfigure(0, weight=1)
frame_cliente.columnconfigure(1, weight=1)
frame_cliente.columnconfigure(2, weight=2)
frame_cliente.columnconfigure(4, weight=4)
frame_cliente.rowconfigure(2, weight=1)

janela.mainloop()
