import tkinter as tk
import os
import threading

os.chdir(os.path.dirname(os.path.abspath(__file__))) #abrir arquivo window.py na mesma pasta dos arquivos de imagem


"""Módulos do api_client.py"""
from api_client import Sistema
import operations_interface

class TelaLoginUsuario(tk.Tk):
    """Responsável pela criação da tela de login"""
    def __init__(self):
        super().__init__()
        self.title('Login - VirtuBank')
        self.iconbitmap('VirtuBanck_icone-removebg-preview.ico')
        self.geometry("330x390")
        self.configure(bg = "#ffffff")

        self.canvas = tk.Canvas(
            bg = "#252121",
            height = 390,
            width = 330,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"tela_login_usuario/background.png")
        self.background = self.canvas.create_image(
            164.5, 75.5,
            image=self.background_img)

        self.criar_widgets()
        self.resizable(False, False)
        self.mainloop()
    
    def criar_widgets(self):

        #Entrada de texto - Número da agência
        self.entry_agencia_img = tk.PhotoImage(file = f"tela_login_usuario/img_textBox0.png")
        self.entry_agencia_bg = self.canvas.create_image(
            164.5, 163.0,
            image = self.entry_agencia_img)

        self.entry_agencia = tk.Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        self.entry_agencia.place(
            x = 72, y = 150,
            width = 185,
            height = 24)

        self.entry_agencia.insert(0, 'Número da agência') ################
        self.entry_agencia.config(fg = 'grey')

        self.entry_agencia.bind('<FocusIn>', self.entry_agencia_focusin) #Liga o evento de foco para limpar o texto
        self.entry_agencia.bind('<FocusOut>', self.entry_agencia_focusout) #Liga o evento de perda de foco para repor o texto padrão

        #Entrada de texto - Número da Conta Corrente
        self.entry_contacorrente_img = tk.PhotoImage(file = f"tela_login_usuario/img_textBox1.png")
        self.entry_contacorrente_bg = self.canvas.create_image(
            164.5, 211.0,
            image = self.entry_contacorrente_img)
        
        self.entry_contacorrente = tk.Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        self.entry_contacorrente.place(
            x = 72, y = 198,
            width = 185,
            height = 24)

        self.entry_contacorrente.insert(0, 'Número da conta corrente')
        self.entry_contacorrente.config(fg = 'grey')

        self.entry_contacorrente.bind('<FocusIn>', self.entry_contacorrente_focusin) #liga o evento de foco para limpar o texto
        self.entry_contacorrente.bind('<FocusOut>', self.entry_contacorrente_focusout) #liga o evento de perda de foco para repor o texto padrão

        #Entrada de texto - Senha do Usuário
        self.entry_senha_img = tk.PhotoImage(file = f"tela_login_usuario/img_textBox2.png")
        self.entry_senha_bg = self.canvas.create_image(
            164.5, 259.0,
            image = self.entry_senha_img)

        self.entry_senha = tk.Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        self.entry_senha.place(
            x = 72, y = 246,
            width = 185,
            height = 24)

        self.entry_senha.insert(0, 'Senha')
        self.entry_senha.config(fg = 'grey')

        self.entry_senha.bind('<FocusIn>', self.entry_senha_focusin) #Liga o evento de foco para limpar o texto
        self.entry_senha.bind('<FocusOut>', self.entry_senha_focusout) #Liga o evento de perda de foco para repor o texto padrão
    
        #Botão - Entrar
        self.img0_botao_entrar = tk.PhotoImage(file = f"tela_login_usuario/img0.png")
        self.button_entrar = tk.Button(
            image = self.img0_botao_entrar,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.button_entrar,
            relief = "flat")

        self.button_entrar.place(
            x = 109, y = 294,
            width = 111,
            height = 30)
        
        self.label_erro_login = self.canvas.create_text(
            164.5, 346.0,
            text = "",
            fill = "#ff0000",
            font = ("None", int(9.0)))

    """Funções de Callback"""

    def entry_agencia_focusin(self, event):
        """Função chamada quando o 'self.entry_agencia' é clicado"""
        #Se o texto atual é igual ao texto padrão, limpa o Entry
        if self.entry_agencia.get() == 'Número da agência':
            self.entry_agencia.delete(0, tk.END)
            self.entry_agencia.insert(0, '') #Remove o texto padrão
            self.entry_agencia.config(fg = 'black') #Muda a cor do texto para preto
        

    def entry_agencia_focusout(self, event):
        """Função chamada quando o 'self.entry_agencia' perde o foco"""
        if self.entry_agencia.get() == '':
            self.entry_agencia.insert(0, 'Número da agência')
            self.entry_agencia.config(fg = 'grey')

    def entry_contacorrente_focusin(self, event):
        "Função chamada quando o entry_contacorrente é clicado"
        if self.entry_contacorrente.get() == 'Número da conta corrente':
            self.entry_contacorrente.delete(0, tk.END)
            self.entry_contacorrente.insert(0, '') #Remove o texto padrão
            self.entry_contacorrente.config(fg = 'black') #Muda a cor do texto para preto

    def entry_contacorrente_focusout(self, event):
        "Função chamada quando o entry_contacorrente perde o foco"
        if self.entry_contacorrente.get() == '':
            self.entry_contacorrente.insert(0, 'Número da conta corrente')
            self.entry_contacorrente.config(fg = 'grey')

    def entry_senha_focusin(self, event):
        if self.entry_senha.get() == 'Senha':
            self.entry_senha.delete(0, tk.END)
            self.entry_senha.insert(0, '') #Remove o texto padrão
            self.entry_senha.config(fg = 'black', show = '*') #Muda a cor do texto para preto

    def entry_senha_focusout(self, event):
        if self.entry_senha.get() == '':
            self.entry_senha.insert(0, 'Senha')
            self.entry_senha.config(fg = 'grey', show = '')
    
    def button_entrar_atualizar_UI(self, resposta: dict):
        "Responsável po realizar a atualização da UI na thread principal"
        if resposta['status_code'] == 400:
            texto = 'Credenciais incorretas!'
            self.canvas.itemconfig(self.label_erro_login, text = texto)
        elif resposta['status_code'] == 200:
            # Esconde a tela de login
            self.destroy()
            #Abre a janela de operações
            operations_interface.TelaOperacoes(id_conta = resposta['id_conta'],
                                            agencia_id = resposta['agencia_id'],
                                            senha = resposta['senha'],
                                            token = resposta['token'],
                                            refresh_token = resposta['refresh_token'])
        elif resposta['status_code'] == 500:
            texto = 'Não foi possível acessar o sistema.'
            self.canvas.itemconfig(self.label_erro_login, text = texto)
        elif resposta['status_code'] == 503:
            texto = 'Sistema indisponível no momento.'
            self.canvas.itemconfig(self.label_erro_login, text = texto)

    def button_entrar_thread(self, agencia_id, id_conta, senha):
        "Responsável por executar a operação de login em uma thread secundária"
        sistema = Sistema()
        check_status = sistema.check_status()
        if check_status:
            request_token = sistema.get_token(id_conta, agencia_id, senha)
            status_code = request_token['cod_resp']
            if status_code == 200:
                resposta = {'status_code': status_code, 
                            'token': request_token['token'], 
                            'refresh_token': request_token['refresh_token'],
                            'agencia_id': agencia_id,
                            'id_conta': id_conta,
                            'senha': senha
                            }
                self.after(0, self.button_entrar_atualizar_UI, resposta)
            elif status_code == 400:
                resposta = {'status_code': status_code}
                self.after(0, self.button_entrar_atualizar_UI, resposta)
            elif status_code == 500:
                resposta = {'status_code': status_code}
                self.after(0, self.button_entrar_atualizar_UI, resposta)
        else: 
            resposta = {'status_code': 503}
            self.after(0, self.button_entrar_atualizar_UI, resposta)
    
    def button_entrar(self):
        """Responsável pela autenticação do usuário""" 
        self.canvas.itemconfig(self.label_erro_login, text = '') #Limpa a caixa de avisos
        agencia = self.entry_agencia.get()
        if agencia == 'Número da agência' or agencia == '':
            aviso = 'Falha no login! Forneça o número da agência.'
            self.canvas.itemconfig(self.label_erro_login, text = aviso)
            return
        conta_corrente = self.entry_contacorrente.get()
        if conta_corrente == 'Número da conta corrente' or conta_corrente == '':
            aviso = 'Falha no login! Forneça o número da conta corrente.'
            self.canvas.itemconfig(self.label_erro_login, text = aviso)
            return
        senha = self.entry_senha.get()
        if senha == 'Senha' or senha == '':
            aviso = 'Falha no login! Forneça a senha.'
            self.canvas.itemconfig(self.label_erro_login, text = aviso)
            return
        thread = threading.Thread(target = self.button_entrar_thread, args = (agencia, conta_corrente, senha))
        thread.start()

if __name__ == "__main__":
    app = TelaLoginUsuario()