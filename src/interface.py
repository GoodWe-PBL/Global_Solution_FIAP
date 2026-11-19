import tkinter as tk
from functools import partial
from tkinter import ttk, messagebox
import webbrowser

FUNDO = "#15151C"
PAINEL = "#24242F"
ROSA = "#FF528D"
TEXTO = "#FAF8FC"
SUAVE = "#C7C3CF"
FONTE = "Segoe UI"


class Interface:
    def __init__(self, sistema, janela):
        self.sistema = sistema
        self.janela = janela
        self.historico = []
        self.modelo = "A"
        self.pergunta = tk.StringVar(janela)
        janela.title("Citizen Assist AI · Guia de serviços")
        janela.geometry("900x710")
        janela.minsize(420, 430)
        janela.configure(bg=FUNDO)

        barra = tk.Frame(janela, bg=FUNDO, padx=22, pady=12)
        barra.pack(fill="x")
        marca = tk.Canvas(barra, width=32, height=32, bg=FUNDO, highlightthickness=0)
        marca.pack(side="left")
        marca.create_polygon(3, 4, 28, 4, 28, 23, 14, 23, 6, 29, 6, 23, 3, 23, fill=ROSA)
        marca.create_line(9, 12, 22, 12, fill=FUNDO, width=2)
        tk.Label(barra, text="Citizen Assist AI", bg=FUNDO, fg=TEXTO,
                 font=(FONTE, 15, "bold")).pack(side="left", padx=8)
        self.voltar = self.botao(barra, "←  Voltar", self.anterior)
        tk.Frame(janela, bg=PAINEL, height=1).pack(fill="x")
        tk.Label(janela, text="Projeto acadêmico FIAP  ·  Orientação não oficial",
                 bg=FUNDO, fg=SUAVE, pady=9, font=(FONTE, 9)).pack(side="bottom")

        self.tela = tk.Canvas(janela, bg=FUNDO, highlightthickness=0)
        rolagem = ttk.Scrollbar(janela, command=self.tela.yview)
        rolagem.pack(side="right", fill="y")
        self.tela.configure(yscrollcommand=rolagem.set)
        self.tela.pack(fill="both", expand=True)
        self.pagina = tk.Frame(self.tela, bg=FUNDO, padx=16, pady=18)
        self.area = self.tela.create_window(0, 0, anchor="n", window=self.pagina)
        self.tela.bind("<Configure>", self.ajustar)
        self.pagina.bind("<Configure>", self.ajustar_rolagem)
        janela.bind("<MouseWheel>", lambda e: self.tela.yview_scroll(-int(e.delta / 120), "units"))
        janela.bind("<Escape>", lambda e: self.anterior())
        janela.bind("<FocusIn>", self.mostrar_foco)
        self.ir(self.inicio)

    def mostrar_foco(self, evento):
        item = evento.widget
        if item.winfo_class() not in ("Button", "Entry") or not str(item).startswith(str(self.pagina)):
            return
        topo = item.winfo_rooty() - self.pagina.winfo_rooty()
        visivel = self.tela.canvasy(0)
        if topo < visivel or topo + item.winfo_height() > visivel + self.tela.winfo_height():
            self.tela.yview_moveto(max(0, topo - 8) / max(1, self.pagina.winfo_height()))

    def ajustar_rolagem(self, evento=None):
        altura = max(self.tela.winfo_height(), self.pagina.winfo_height())
        self.tela.configure(scrollregion=(0, 0, self.tela.winfo_width(), altura))

    def ajustar(self, evento):
        largura = min(evento.width, 730)
        self.ajustar_rolagem()
        self.tela.coords(self.area, evento.width / 2, 0)
        self.tela.itemconfigure(self.area, width=largura)
        for item in self.pagina.winfo_children():
            if item.winfo_class() in ("Label", "Button"):
                item.configure(wraplength=max(180, largura - 82))

    def ir(self, pagina, *dados):
        self.historico.append((pagina, dados))
        self.desenhar()

    def anterior(self):
        if len(self.historico) > 1:
            self.historico.pop()
            self.desenhar()

    def recomecar(self):
        self.pergunta.set("")
        self.historico.clear()
        self.ir(self.inicio)

    def desenhar(self):
        for item in self.pagina.winfo_children():
            item.destroy()
        self.voltar.pack_forget()
        if len(self.historico) > 1:
            self.voltar.pack(side="right")
        pagina, dados = self.historico[-1]
        pagina(*dados)
        self.janela.update_idletasks()
        self.tela.yview_moveto(0)
        for item in self.pagina.winfo_children():
            if item.winfo_class() in ("Entry", "Button"):
                item.focus_set()
                break

    def texto(self, texto, tamanho=12, cor=TEXTO, negrito=False):
        largura = max(290, min(730, self.tela.winfo_width()) - 82)
        item = tk.Label(self.pagina, text=texto, wraplength=largura, justify="left", anchor="w",
                        bg=FUNDO, fg=cor, font=(FONTE, tamanho, "bold" if negrito else "normal"))
        item.pack(fill="x", pady=(2, 9))
        return item

    def botao(self, pai, texto, acao, principal=False):
        return tk.Button(pai, text=texto, command=acao, wraplength=600,
                         anchor="w", justify="left", padx=16, pady=10, font=(FONTE, 11, "bold"),
                         bg=ROSA if principal else PAINEL, fg=FUNDO if principal else TEXTO,
                         activebackground="#FF82AA" if principal else "#393745", activeforeground=FUNDO if principal else TEXTO,
                         relief="flat", bd=0, highlightthickness=2, highlightbackground=FUNDO,
                         highlightcolor=TEXTO, cursor="hand2")

    def opcao(self, texto, acao, principal=False):
        escolha = self.botao(self.pagina, texto, acao, principal)
        escolha.configure(wraplength=max(290, min(730, self.tela.winfo_width()) - 82))
        escolha.pack(fill="x", pady=3)

    def titulo(self, etapa, titulo):
        self.texto(etapa, 10, ROSA, True)
        self.texto(titulo, 23, negrito=True)

    def inicio(self):
        desenho = tk.Canvas(self.pagina, height=84, bg=FUNDO, highlightthickness=0)
        desenho.pack(fill="x", pady=(12, 6))
        desenho.create_oval(2, 1, 80, 79, fill="#382531", outline="")
        desenho.create_polygon(24, 15, 50, 15, 60, 25, 60, 60, 24, 60,
                               fill=PAINEL, outline=SUAVE, width=2)
        desenho.create_line(49, 15, 49, 26, 60, 26, fill=SUAVE, width=2)
        desenho.create_line(31, 34, 50, 34, fill=SUAVE, width=2)
        desenho.create_oval(42, 40, 60, 58, fill=FUNDO, outline=ROSA, width=3)
        desenho.create_line(58, 56, 68, 66, fill=ROSA, width=4)
        self.titulo("Guia de serviços", "Como podemos ajudar?")
        self.texto("Encontre orientações sobre documentos, serviços públicos e direitos.", cor=SUAVE)
        self.opcao("Escrever minha pergunta   →", partial(self.ir, self.consulta), True)
        self.opcao("Escolher um tema   →", partial(self.ir, self.temas))

    def consulta(self):
        self.titulo("Sua pergunta", "O que você precisa saber?")
        self.texto("Por exemplo, “Como tirar o título de eleitor?”. Escreva apenas a dúvida, sem dados pessoais.", cor=SUAVE)
        campo = tk.Entry(self.pagina, textvariable=self.pergunta, bg=PAINEL, fg=TEXTO, insertbackground=TEXTO,
                         font=(FONTE, 14), relief="flat", highlightthickness=2, highlightcolor=ROSA)
        campo.pack(fill="x", ipady=9, pady=6)
        campo.bind("<Return>", lambda e: self.buscar())
        self.opcao("Encontrar orientação", self.buscar, True)
        self.aviso = self.texto("", cor=ROSA)

    def buscar(self):
        resultado = self.sistema.buscar(self.pergunta.get())
        if resultado.status == "vazia":
            self.aviso.configure(text="Escreva sua dúvida para continuar.")
        elif resultado.status == "encontrado":
            self.ir(self.orientacao, resultado.ids[0])
        else:
            self.ir(self.resultados, resultado.ids, "Sua busca")

    def resultados(self, ids, origem):
        if ids:
            self.titulo(origem, "Qual destas dúvidas é a sua?")
            self.escolhas(ids)
        else:
            self.titulo("Sua busca", "Ainda não temos essa orientação")
            self.texto("Tente escrever de outro jeito ou veja os temas disponíveis.", cor=SUAVE)
            self.opcao("Editar minha pergunta", self.anterior, True)
            self.opcao("Ver os temas", partial(self.ir, self.temas))

    def temas(self):
        self.titulo("Por tema", "Sobre o que é sua dúvida?")
        for chave, tema in self.sistema.base["temas"].items():
            self.opcao(tema["nome"], partial(self.ir, self.subtemas, chave))

    def subtemas(self, chave):
        tema = self.sistema.base["temas"][chave]
        self.titulo(tema["nome"], "Qual assunto você procura?")
        for subtema, nome in tema["subtemas"].items():
            ids = self.sistema.por_subtema[(chave, subtema)]
            if len(ids) == 1:
                self.opcao(nome, partial(self.ir, self.orientacao, ids[0]))
            elif ids:
                self.opcao(nome, partial(self.ir, self.resultados, ids, nome))

    def escolhas(self, ids):
        for codigo in ids:
            pergunta = self.sistema.por_id[codigo]["pergunta"]
            self.opcao(pergunta, partial(self.ir, self.orientacao, codigo))

    def orientacao(self, codigo):
        registro = self.sistema.por_id[codigo]
        self.titulo("Sua orientação", registro["pergunta"])
        for trecho in self.sistema.trechos(codigo, self.modelo):
            self.texto(trecho)
        if registro["requer_confirmacao"]:
            self.texto("Confirme as regras atuais no canal indicado.", 11, ROSA, True)
        self.texto(f"{registro['fonte']}  ·  Verificada em {registro['data_verificacao']}", 10, SUAVE)
        self.opcao("Consultar a fonte  ↗", partial(self.abrir_fonte, registro["referencia"]), True)
        self.opcao("Ler por partes" if self.modelo == "A" else "Ler em texto corrido", self.trocar_modelo)
        if registro["relacionados"]:
            self.opcao("Ver assuntos relacionados", partial(self.ir, self.relacionados, codigo))
        self.opcao("Fazer outra consulta", self.recomecar)

    def abrir_fonte(self, link):
        if not webbrowser.open(link):
            messagebox.showinfo("Fonte da orientação", link)

    def trocar_modelo(self):
        self.modelo = "B" if self.modelo == "A" else "A"
        self.desenhar()

    def relacionados(self, codigo):
        self.titulo("Assuntos relacionados", "Quer continuar por onde?")
        self.escolhas(self.sistema.por_id[codigo]["relacionados"])


def executar_interface(sistema):
    janela = tk.Tk()
    Interface(sistema, janela)
    janela.mainloop()
