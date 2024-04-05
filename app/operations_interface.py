import tkinter as tk
import os
from tkcalendar import DateEntry
from api_client import Sistema_Bancario
import threading
from api_client import Sistema

os.chdir(os.path.dirname(os.path.abspath(__file__))) #abrir arquivo window.py na mesma pasta dos arquivos de imagem


class TelaOperacoes(tk.Tk):
    """Tela responsável pela criação da janela principal"""

    def __init__(self, id_conta, agencia_id, senha, token, refresh_token):
        """Cria a janela principal e inicializa os widgets e frames"""
        super().__init__()

        self.id_conta = id_conta
        self.agencia_id = agencia_id
        self.senha = senha
        self.token = token
        self.refresh_token = refresh_token

        self.operacao_em_andamento = False #Sinaliza quando alguma operação está em andamento

        self.geometry("804x509")
        self.configure(bg = "#252121")
        self.title('Operações Bancárias - VirtuBank')

        self.canvas = tk.Canvas(
            bg = "#252121",
            height = 509,
            width = 804,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"tela_operacoes/background.png")
        self.background = self.canvas.create_image(
            345.5, 253.0,
            image=self.background_img)
        
        self.criar_widgets()
        self.iconbitmap('VirtuBanck_icone-removebg-preview.ico')
        self.resizable(False, False)
        self.mainloop()
        
    def criar_widgets(self):
        """Cria os widgets da janela principal"""

        self.conta_bancaria = Sistema_Bancario()

        #Botão - 'Saque'
        "Cria o botão 'Saque'"
        self.img2_saque = tk.PhotoImage(file = f"tela_operacoes/img2.png")
        self.button_saque = tk.Button(
            image = self.img2_saque,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.frame_saque_mostrar,
            relief = "flat")

        self.button_saque.place(
            x = 53, y = 226,
            width = 133,
            height = 48)
        
        #Botão - 'Minha Conta'
        "Cria o botão 'Minha Conta'"
        self.img3_minhaconta = tk.PhotoImage(file = f"tela_operacoes/img3.png")
        self.button_minhaconta = tk.Button(
            image = self.img3_minhaconta,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.exibir_info_conta,
            relief = "flat")

        self.button_minhaconta.place(
            x = 53, y = 339,
            width = 133,
            height = 48)
        
        #Botão - 'Ver Saldo'
        "Cria o botão 'Ver Saldo'"
        self.img4_versaldo = tk.PhotoImage(file = f"tela_operacoes/img4.png")
        self.button_versaldo = tk.Button(
            image = self.img4_versaldo,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.exibir_info_saldo,
            relief = "flat")

        self.button_versaldo.place(
            x = 210, y = 339,
            width = 133,
            height = 48)
        
        #Botão - 'Ver Extrato'
        "Cria o botão 'Ver Extrato'"
        self.img5_verextrato = tk.PhotoImage(file = f"tela_operacoes/img5.png")
        self.button_verextrato = tk.Button(
            image = self.img5_verextrato,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.frame_extrato_mostrar,
            relief = "flat")

        self.button_verextrato.place(
            x = 367, y = 339,
            width = 133,
            height = 48)
        
        #Botão - 'Depósito' 
        self.img6_deposito = tk.PhotoImage(file = f"tela_operacoes/img6.png")
        self.button_deposito = tk.Button(
            image = self.img6_deposito,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.frame_deposito_mostrar,
            relief = "flat")

        self.button_deposito.place(
            x = 210, y = 226,
            width = 133,
            height = 48)
        
        #Botão - 'Transferência'
        self.img7_transferencia = tk.PhotoImage(file = f"tela_operacoes/img7.png")
        self.button_transferencia = tk.Button(
            image = self.img7_transferencia,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.frame_transferencia_mostrar,
            relief = "flat")

        self.button_transferencia.place(
            x = 367, y = 226,
            width = 133,
            height = 48)
        
        #Label - Limite por Saque
        self.limite_por_saque = self.canvas.create_text(
            701.5, 83.5,
            text = "R$5000,00",
            fill = "#d3d3d3",
            font = ("Inter-SemiBold", int(10.0)))
        
        #Label - Saques diários
        self.saques_diarios = self.canvas.create_text(
            701.5, 62.5,
            text = f"{str(self.conta_bancaria.numero_saques_diarios()['saques_hoje'])} / 3",
            fill = "#d3d3d3",
            font = ("Inter-SemiBold", int(10.0)))

        #Label - Limite disponível
        self.limite_disponível = self.canvas.create_text(
            701.5, 105.5,
            text = "R$15000,00",
            fill = "#d3d3d3",
            font = ("Inter-SemiBold", int(10.0)))

        #Label - porcentagem (balanço entre saques, depósitos e transferências)
        self.balanco_mensal = self.canvas.create_text(
            410.5, 150.0,
            text = "----",
            fill = "#000000",
            font = ("Inter-ExtraBold", int(13.0)))

        #Label - Situação da conta bancária

        self.status_conta = self.canvas.create_text(
            310.0, 150.0,
            text = f"{self.conta_bancaria.consultar_conta()['status_conta']}",
            fill = "#000000",
            font = ("Inter-ExtraBold", int(13.0)))

        #Label - Saldo Atual
        self.saldo_atual = self.canvas.create_text(
            396.0, 96.0,
            text = f"R$ {self.conta_bancaria.consultar_saldo()['saldo']}",
            fill = "#000000",
            font = ("Inter-SemiBold", int(25.0)))
        
        #Labels de informações do cartão

        dados_cartao = self.conta_bancaria.consultar_info_cartao()
        final_cartao = dados_cartao['num_cartao']
        validade_cartao = dados_cartao['val_cartao']
        cvv_cartao = dados_cartao['cod_cvv']
        
        #Label - final do cartão
        self.final_cartao = self.canvas.create_text(
            86, 139.5,
            text = final_cartao,
            fill = "#000000",
            font = ("Inter-Light", int(10.0)))

        #Label - validade do cartão
        self.validade_cartao = self.canvas.create_text(
            149.0, 139.5,
            text = validade_cartao,
            fill = "#000000",
            font = ("Inter-Light", int(10.0)))

        #Label - código CVV do cartão
        self.cvv_cartao = self.canvas.create_text(
            203.0, 139.5,
            text = cvv_cartao,
            fill = "#000000",
            font = ("Inter-Light", int(10.0)))
        
        #Caixa de texto do terminal
        self.entry_terminal_img = tk.PhotoImage(file = f"tela_operacoes/img_textBox1.png")
        self.entry_terminal_bg = self.canvas.create_image(
            659.0, 400.5,
            image = self.entry_terminal_img)

        self.entry_terminal = tk.Text(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0,
            wrap = tk.WORD)

        self.entry_terminal.place(
            x = 547, y = 313,
            width = 224,
            height = 173)

        self.entry_terminal.delete("1.0", "end")  # Remove todo o texto atual
        self.entry_terminal.insert("1.0", "")  # Insere novo texto

        """---------------------- FRAME SAQUE --------------------------"""
        
        self.frame_saque = tk.Frame(bg = 'black')
        self.frame_saque.place(x = 547, y = 130, width=240, height=178)
        self.frame_saque.place_forget()

        self.canvas_frame_saque = tk.Canvas(
            self.frame_saque,
            bg = "#252121",
            height = 178,
            width = 240,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas_frame_saque.place(x = 0, y = 0)

        #Label - 'Realizar Saque'
        self.canvas_frame_saque.create_text(
            56.0, 10.5,
            text = "Realizar Saque",
            fill = "#ffffff",
            font = ("Inter-Bold", int(12.0)))

        #Entrada de texto - valor do saque
        self.entry_valor_frame_saque_img = tk.PhotoImage(file = f"tela_operacoes/img_textBox0.png")
        self.entry_valor_frame_saque_bg = self.canvas_frame_saque.create_image(
            660.0, 177.0,
            image = self.entry_valor_frame_saque_img)

        self.entry_valor_frame_saque = tk.Entry(
            self.frame_saque,
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        self.entry_valor_frame_saque.place(
            x = 3, y = 36,
            width = 220,
            height = 20)
        
        self.entry_valor_frame_saque.insert(0, 'Digite o valor') ################
        self.entry_valor_frame_saque.config(fg = 'grey')

        self.entry_valor_frame_saque.bind('<FocusIn>', self.entry_valor_frame_saque_focusin) #Liga o evento de foco para limpar o texto
        self.entry_valor_frame_saque.bind('<FocusOut>', self.entry_valor_frame_saque_focusout) #Liga o evento de perda de foco para repor o texto padrão
        
        #Botão - 'Ok': Frame Saque 
        self.img_frame_saque = tk.PhotoImage(file = f"tela_operacoes/img0.png")
        self.button_ok_framesaque = tk.Button(
            self.frame_saque,
            image = self.img_frame_saque,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.ok_sacar,
            relief = "flat")

        self.button_ok_framesaque.place(
            x = 51 , y = 74,
            width = 58,
            height = 17)

        #Botão - 'Cancelar': Frame Saque 
        self.img1_frame_saque = tk.PhotoImage(file = f"tela_operacoes/img1.png")
        self.button_cancelar_frame_saque = tk.Button(
            self.frame_saque,
            image = self.img1_frame_saque,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.cancelar_operacao,
            relief = "flat")

        self.button_cancelar_frame_saque.place(
            x = 134, y = 75,
            width = 58,
            height = 17)
        
        """---------------------- FRAME DEPÓSITO ---------------------------"""

        self.frame_deposito = tk.Frame(bg = 'black')
        self.frame_deposito.place(x = 547, y = 130, width=240, height=178)
        self.frame_deposito.place_forget()

        self.canvas_frame_deposito = tk.Canvas(
            self.frame_deposito,
            bg = "#252121",
            height = 178,
            width = 240,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas_frame_deposito.place(x = 0, y = 0)

        #Label - 'Realizar Depósito': Frame Depósito
        self.canvas_frame_deposito.create_text(
            65.0, 10.5,
            text = "Realizar Depósito",
            fill = "#ffffff",
            font = ("Inter-Bold", int(12.0)))

        #Entrada de texto - valor de depósito: Frame Depósito
        self.entry0_frame_deposito_img = tk.PhotoImage(file = f"tela_operacoes/img_textBox0.png")
        self.entry0_frame_deposito_bg = self.canvas_frame_deposito.create_image(
            660.0, 177.0,
            image = self.entry0_frame_deposito_img)

        self.entry0_frame_deposito = tk.Entry(
            self.frame_deposito,
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        self.entry0_frame_deposito.place(
            x = 3, y = 36,
            width = 220,
            height = 20)
        
        self.entry0_frame_deposito.insert(0, 'Digite o valor') ################
        self.entry0_frame_deposito.config(fg = 'grey')

        self.entry0_frame_deposito.bind('<FocusIn>', self.entry0_frame_deposito_focusin) #Liga o evento de foco para limpar o texto
        self.entry0_frame_deposito.bind('<FocusOut>', self.entry0_frame_deposito_focusout) #Liga o evento de perda de foco para repor o texto padrão

        #Botão - 'Ok': Frame Depósito
        self.img0_frame_deposito = tk.PhotoImage(file = f"tela_operacoes/img0.png")
        self.button_ok_frame_deposito = tk.Button(
            self.frame_deposito,
            image = self.img0_frame_deposito,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.ok_depositar,
            relief = "flat")

        self.button_ok_frame_deposito.place(
            x = 51 , y = 74,
            width = 58,
            height = 17)

        #Botão - 'Cancelar': Frame Depósito 
        self.img1_frame_deposito = tk.PhotoImage(file = f"tela_operacoes/img1.png")
        self.button_cancelar_frame_deposito = tk.Button(
            self.frame_deposito,
            image = self.img1_frame_deposito,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.cancelar_operacao,
            relief = "flat")

        self.button_cancelar_frame_deposito.place(
            x = 134, y = 75,
            width = 58,
            height = 17)
        
        """--------------------- FRAME TRANSFERÊNCIA ----------------------"""

        self.frame_transferencia = tk.Frame(bg = 'black')
        self.frame_transferencia.place(x = 547, y = 130, width=240, height=178)
        self.frame_transferencia.place_forget()

        self.canvas_frame_transferencia = tk.Canvas(
            self.frame_transferencia,
            bg = "#252121",
            height = 178,
            width = 240,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas_frame_transferencia.place(x = 0, y = 0)

        #Label - Realizar Transferência: Frame Transferência
        self.canvas_frame_transferencia.create_text(
            81.0, 10.5,
            text = "Realizar Transferência",
            fill = "#ffffff",
            font = ("Inter-Bold", int(12.0)))

        #Caixa de texto - número da agência destino: Frame Transferência
        self.entry0_frame_transferencia_img = tk.PhotoImage(file = f"tela_operacoes/img_textBox0_transferencia.png")
        self.entry0_frame_transferencia_bg = self.canvas_frame_transferencia.create_image(
            660.0, 177.0,
            image = self.entry0_frame_transferencia_img)

        self.entry0_frame_transferencia = tk.Entry(
            self.frame_transferencia,
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        self.entry0_frame_transferencia.place(
            x = 3, y = 36,
            width = 220,
            height = 20)
        
        self.entry0_frame_transferencia.insert(0, 'Número da Agência Destino') ################
        self.entry0_frame_transferencia.config(fg = 'grey')

        self.entry0_frame_transferencia.bind('<FocusIn>', self.entry0_frame_transferencia_focusin) #Liga o evento de foco para limpar o texto
        self.entry0_frame_transferencia.bind('<FocusOut>', self.entry0_frame_transferencia_focusout) #Liga o evento de perda de foco para repor o texto padrão

        #Caixa de texto - conta corrente destino: Frame Transferência
        self.entry1_frame_transferencia_img = tk.PhotoImage(file = f"tela_operacoes/img_textBox0_transferencia.png")
        self.entry1_frame_transferencia_bg = self.canvas_frame_transferencia.create_image(
            660.0, 207.0,
            image = self.entry1_frame_transferencia_img)

        self.entry1_frame_transferencia = tk.Entry(
            self.frame_transferencia,
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        self.entry1_frame_transferencia.place(
            x = 3, y = 66,
            width = 220,
            height = 20)
        
        self.entry1_frame_transferencia.insert(0, 'Número da Conta Corrente Destino') ################
        self.entry1_frame_transferencia.config(fg = 'grey')

        self.entry1_frame_transferencia.bind('<FocusIn>', self.entry1_frame_transferencia_focusin) #Liga o evento de foco para limpar o texto
        self.entry1_frame_transferencia.bind('<FocusOut>', self.entry1_frame_transferencia_focusout) #Liga o evento de perda de foco para repor o texto padrão

        #Caixa de texto - valor da transferência: Frame Transferência
        self.entry2_frame_transferencia_img = tk.PhotoImage(file = f"tela_operacoes/img_textBox0_transferencia.png")
        self.entry2_frame_transferencia_bg = self.canvas_frame_transferencia.create_image(
            660.0, 237.0,
            image = self.entry2_frame_transferencia_img)

        self.entry2_frame_transferencia = tk.Entry(
            self.frame_transferencia,
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        self.entry2_frame_transferencia.place(
            x = 3, y = 96,
            width = 220,
            height = 20)
        
        self.entry2_frame_transferencia.insert(0, 'Valor da Transferência') ################
        self.entry2_frame_transferencia.config(fg = 'grey')

        self.entry2_frame_transferencia.bind('<FocusIn>', self.entry2_frame_transferencia_focusin) #Liga o evento de foco para limpar o texto
        self.entry2_frame_transferencia.bind('<FocusOut>', self.entry2_frame_transferencia_focusout) #Liga o evento de perda de foco para repor o texto padrão

        #Botão - 'Ok': Frame Transferência
        self.img_ok_frame_transferencia = tk.PhotoImage(file = f"tela_operacoes/img0.png")
        self.button_ok_frame_transferencia = tk.Button(
            self.frame_transferencia,
            image = self.img_ok_frame_transferencia,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.ok_transferir,
            relief = "flat")

        self.button_ok_frame_transferencia.place(
            x = 51, y = 129,
            width = 58,
            height = 17)

        #Botão - 'Cancelar': Frame Transferência
        self.img_cancelar_frame_transferencia = tk.PhotoImage(file = f"tela_operacoes/img1.png")
        self.button_cancelar_frame_transferencia = tk.Button(
            self.frame_transferencia,
            image = self.img_cancelar_frame_transferencia,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.cancelar_operacao,
            relief = "flat")

        self.button_cancelar_frame_transferencia.place(
            x = 134, y = 129,
            width = 58,
            height = 17)
        
        """---------------------------- FRAME EXTRATO  ----------------------------"""
        
        self.frame_extrato = tk.Frame(bg = 'black')
        self.frame_extrato.place(x = 547, y = 130, width=240, height=178)
        self.frame_extrato.place_forget()

        self.canvas_frame_extrato = tk.Canvas(
            self.frame_extrato,
            bg = "#252121",
            height = 178,
            width = 240,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas_frame_extrato.place(x = 0, y = 0)

        #Label - 'Consultar Extrato': Frame Extrato
        self.canvas_frame_extrato.create_text(
            62.0, 10.5,
            text = "Consultar Extrato",
            fill = "#ffffff",
            font = ("Inter-Bold", int(12.0)))

        #Entrada de texto - data da consulta: Frame Extrato
        self.entry_valor_frame_extrato_img = tk.PhotoImage(file = f"tela_operacoes/img_textBox0.png")
        self.entry_valor_frame_extrato_bg = self.canvas_frame_extrato.create_image(
            660.0, 177.0,
            image = self.entry_valor_frame_extrato_img)

        self.entry_valor_frame_extrato = DateEntry(
            self.frame_extrato,
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0,
            date_pattern='dd/mm/yyyy')

        self.entry_valor_frame_extrato.place(
            x = 3, y = 36,
            width = 220,
            height = 20)
        
        #Botão - 'Ok': Frame Extrato
        self.img_frame_extrato = tk.PhotoImage(file = f"tela_operacoes/img0.png")
        self.button_ok_frameextrato = tk.Button(
            self.frame_extrato,
            image = self.img_frame_extrato,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.exibir_extrato,
            relief = "flat")

        self.button_ok_frameextrato.place(
            x = 51 , y = 74,
            width = 58,
            height = 17)

        #Botão - 'Cancelar': Frame Extrato
        self.img1_frame_extrato = tk.PhotoImage(file = f"tela_operacoes/img1.png")
        self.button_cancelar_frame_extrato = tk.Button(
            self.frame_extrato,
            image = self.img1_frame_extrato,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.cancelar_operacao,
            relief = "flat")

        self.button_cancelar_frame_extrato.place(
            x = 134, y = 75,
            width = 58,
            height = 17)        

    """----------------------- Funções de callback -------------------------------"""
    def exibir_info_saldo_atualizar_UI(self, text):
        "Responsável por atualizar a UI na thread principal"
        self.entry_terminal.delete("1.0", "end")  # Remove todo o texto atual
        self.entry_terminal.insert("1.0", text)  # Insere novo texto
        self.operacao_em_andamento = False
    
    def exibir_info_saldo_thread(self):
        "Responsável por realizar a operação demorada de consulta em uma thread secundária"
        dados = self.conta_bancaria.consultar_saldo()
        if dados['status_code'] == 200:
            text = (
                f"\nINFORMAÇÕES DE SALDO \n\n"
                f"Cliente: {dados['nome']}\n\n"
                f"Conta: {dados['id_conta']}\n\n"
                f"Agência: {dados['agencia_id']}\n\n"
                f"Saldo: {dados['saldo']}"
            )
            self.after(0, self.exibir_info_saldo_atualizar_UI, text)
        elif dados['status_code'] == 500:
            text = dados['text_resp']
            self.after(0, self.exibir_info_saldo_atualizar_UI, text)
        elif dados['status_code'] == 503:
            text = dados['text_resp']
            self.after(0, self.exibir_info_saldo_atualizar_UI, text)

    def exibir_info_saldo(self):
        """Responsável por exibir as informações de saldo"""
        if not self.operacao_em_andamento:
            self.operacao_em_andamento = True
            self.frame_saque.place_forget() #Esconder frame saque
            self.frame_deposito.place_forget() #Esconder frame saque depósito
            self.frame_transferencia.place_forget() #Esconder frame de transferência
            self.frame_extrato.place_forget() #Esconder frame de extrato
            
            #Iniciar a operação demorada em uma nova thread
            thread = threading.Thread(target = self.exibir_info_saldo_thread)
            thread.start()

    def exibir_info_conta_atualizar_UI(self, text):
        "Responsável por atualizar a UI na thread principal"
        self.entry_terminal.delete("1.0", "end")  # Remove todo o texto atual
        self.entry_terminal.insert("1.0", text)  # Insere novo texto
        self.operacao_em_andamento = False

    def exibir_info_conta_thread(self):
        "Método que executa a operação em uma thread separada"
        conta_bancaria = Sistema_Bancario()
        dados = conta_bancaria.consultar_conta()
        if dados['status_code'] == 200:
            text = (
                f"\nINFORMAÇÕES DA CONTA \n\n"
                f"Cliente: {dados['nome_cliente']}\n\n"
                f"Conta: {dados['id_conta']}\n\n"
                f"Agência: {dados['agencia_id']}\n\n"
                f"Tipo: {dados['tipo_conta']}\n\n"
                f"Status: {dados['status_conta']}\n\n"
                f"Data criação: {dados['data_criacao']}\n\n"
                f"Data fechamento: {dados['data_fechamento'] if dados['data_fechamento'] is not None else '--/--/----'}"
            )
            self.after(0, self.exibir_info_conta_atualizar_UI, text)
        elif dados['status_code'] == 500:
            text = dados['text_resp']
            self.after(0, self.exibir_info_conta_atualizar_UI, text)
        elif dados['status_code'] == 503:
            text = dados['text_resp']
            self.after(0, self.exibir_info_conta_atualizar_UI, text)
    
    def exibir_info_conta(self):
        """Responsável por exibir as informações da conta bancária"""
        if not self.operacao_em_andamento:
            self.operacao_em_andamento = True
            self.frame_saque.place_forget() #Esconder frame saque
            self.frame_deposito.place_forget() #Esconder frame depósito
            self.frame_transferencia.place_forget() #Esconder frame transferência
            self.frame_extrato.place_forget() #Esconder frame de extrato
            #Iniciar a operação demorada em uma nova thread
            thread = threading.Thread(target = self.exibir_info_conta_thread)
            thread.start()
        
    #Botão - 'Cancelar': Acessível por todos os frames
    def cancelar_operacao(self):
        "Retorna a tela inicial"
        self.frame_saque.place_forget() #Esconder o frame saque
        self.frame_deposito.place_forget() #Esconder o frame depósito
        self.frame_transferencia.place_forget() #Esconder o frame transferência
        self.frame_extrato.place_forget() #Esconder o frame extrato

    #FRAME SAQUE ----------------------------------------------------------------------------------
    def frame_saque_mostrar(self):
        "Exibe o frame de saque (self.frame_saque)"
        self.frame_transferencia.place_forget()
        self.frame_deposito.place_forget()
        self.frame_extrato.place_forget()
        if self.frame_saque.winfo_viewable():
            self.frame_saque.place_forget()
        else:
            self.frame_saque.place(x = 547, y = 130, width = 240, height = 178)

    def entry_valor_frame_saque_focusin(self, event):
        """Função chamada quando o 'self.entry_valor_frame_saque' é clicado"""
        #Se o texto atual é igual ao texto padrão, limpa o Entry
        if self.entry_valor_frame_saque.get() == 'Digite o valor':
            self.entry_valor_frame_saque.delete(0, tk.END)
            self.entry_valor_frame_saque.insert(0, '') #Remove o texto padrão
            self.entry_valor_frame_saque.config(fg = 'black') #Muda a cor do texto para preto
        

    def entry_valor_frame_saque_focusout(self, event):
        """Função chamada quando o 'self.entry_valor_frame_saque' perde o foco"""
        if self.entry_valor_frame_saque.get() == '':
            self.entry_valor_frame_saque.insert(0, 'Digite o valor')
            self.entry_valor_frame_saque.config(fg = 'grey')

    #Botão 'Ok': Frame Saque
    def ok_sacar_atualizar_UI(self, dados: dict):
        "Responsável por atualizar a UI na thread principal"
        #Verifica se a operação foi bem-sucedida
        if dados['status_code'] == 200:
            self.entry_terminal.delete("1.0", "end")  # Remove todo o texto atual
            self.entry_terminal.insert("1.0", dados['text_resp'])  # Insere novo texto
            if dados['saques_diarios'] is not None and dados['saldo_atual'] is not None:
                self.canvas.itemconfig(self.saques_diarios, text = f"{str(dados['saques_diarios'])} / 3")
                self.canvas.itemconfig(self.saldo_atual, text = f"R$ {dados['saldo_atual']}")
            self.operacao_em_andamento = False
        elif dados['status_code'] == 500:
            self.entry_terminal.delete("1.0", "end")  # Remove todo o texto atual
            self.entry_terminal.insert("1.0", dados['text_resp'])  # Insere novo texto
            self.operacao_em_andamento = False
        elif dados['status_code'] == 503:
            self.entry_terminal.delete("1.0", "end")  # Remove todo o texto atual
            self.entry_terminal.insert("1.0", dados['text_resp'])  # Insere novo texto
            self.operacao_em_andamento = False

    def ok_sacar_thread(self, valor_saque):
        "Responsável por executar as operações demoradas em uma thread secundária"
        dados = self.conta_bancaria.sacar(valor_saque)
        #Agendar a atualização da UI na thread principal
        self.after(0, self.ok_sacar_atualizar_UI, dados)

    def ok_sacar(self):
        "Executa a operação de saque. Coleta o valor a ser sacado e realiza o CRUD"
        if not self.operacao_em_andamento:
            self.operacao_em_andamento = True
            valor_saque = self.entry_valor_frame_saque.get().strip() #Obtém e remove espaços em branco
            #Verificar se o valor é um número válido
            try:
                valor_saque = float(valor_saque) #Tenta converter para float
                thread = threading.Thread(target = self.ok_sacar_thread, args = (valor_saque,))
                thread.start()
            except ValueError:
                #Se a conversão falhar, atualiza o terminal com uma mensagem de erro
                self.entry_terminal.delete("1.0", "end")  # Remove todo o texto atual
                self.entry_terminal.insert("1.0", "Por favor, digite um valor numérico válido para o saque!")  # Insere novo texto
                self.operacao_em_andamento = False


    #FRAME DEPÓSITO --------------------------------------------------------------------------------------
    def frame_deposito_mostrar(self):
        """Responsável por exibir o frame de depósito (frame_deposito)"""
        self.frame_transferencia.place_forget()
        self.frame_saque.place_forget()
        self.frame_extrato.place_forget()
        if self.frame_deposito.winfo_viewable():
            self.frame_deposito.place_forget()
        else:
            self.frame_deposito.place(x = 547, y = 130, width = 240, height = 178)
        
    def entry0_frame_deposito_focusin(self, event):
        """Função chamada quando o 'self.entry0_frame_deposito' é clicado"""
        #Se o texto atual é igual ao texto padrão, limpa o Entry
        if self.entry0_frame_deposito.get() == 'Digite o valor':
            self.entry0_frame_deposito.delete(0, tk.END)
            self.entry0_frame_deposito.insert(0, '') #Remove o texto padrão
            self.entry0_frame_deposito.config(fg = 'black') #Muda a cor do texto para preto
        

    def entry0_frame_deposito_focusout(self, event):
        """Função chamada quando o 'self.entry0_frame_deposito' perde o foco"""
        if self.entry0_frame_deposito.get() == '':
            self.entry0_frame_deposito.insert(0, 'Digite o valor')
            self.entry0_frame_deposito.config(fg = 'grey')
    
    #Botão 'Ok': Frame Depósito
    def ok_depositar_atualizar_UI(self, dados):
        if dados['status_code'] == 200:
            self.entry_terminal.delete("1.0", "end")  # Remove todo o texto atual
            self.entry_terminal.insert("1.0", dados['text_resp'])  # Insere novo texto
            if dados['saldo_atual'] != None:
                self.canvas.itemconfig(self.saldo_atual, text = f"R$ {dados['saldo_atual']}")
            self.operacao_em_andamento = False
        elif dados['status_code'] == 500:
            self.entry_terminal.delete("1.0", "end")  # Remove todo o texto atual
            self.entry_terminal.insert("1.0", dados['text_resp'])  # Insere novo texto
            self.operacao_em_andamento = False
        elif dados['status_code'] == 503:
            self.entry_terminal.delete("1.0", "end")  # Remove todo o texto atual
            self.entry_terminal.insert("1.0", dados['text_resp'])  # Insere novo texto
            self.operacao_em_andamento = False

    def ok_depositar_thread(self, valor_deposito):
        #Se a conversão for bem-sucedida, prossegue com o saque
        dados = self.conta_bancaria.depositar(valor_deposito)
        self.after(0, self.ok_depositar_atualizar_UI, dados)

    def ok_depositar(self):
        "Executa a operação de depósito. Coleta o valor a ser sacado e realiza o CRUD"
        if not self.operacao_em_andamento:
            self.operacao_em_andamento = True
            valor_deposito = self.entry0_frame_deposito.get().strip() #Obtém e remove espaços em branco
            try:
                valor_deposito = float(valor_deposito) #Tentar converter para float
                thread = threading.Thread(target = self.ok_depositar_thread, args = (valor_deposito,))
                thread.start()

            except ValueError:
                #Se a conversão falhar, atualiza o terminal com uma mensagem de erro
                self.entry_terminal.delete("1.0", "end")  # Remove todo o texto atual
                self.entry_terminal.insert("1.0", "Por favor, digite um valor numérico válido para o depósito!")  # Insere novo texto
                self.operacao_em_andamento = False


    #FRAME TRANSFERENCIA -----------------------------------------------------------------------
    def frame_transferencia_mostrar(self):
        """Responsável por mostrar o frame de transferência (frame_transferencia)"""
        self.frame_deposito.place_forget()
        self.frame_saque.place_forget()
        self.frame_extrato.place_forget()
        if self.frame_transferencia.winfo_viewable():
            self.frame_transferencia.place_forget()
        else:
            self.frame_transferencia.place(x = 547, y = 130, width = 240, height = 178)

    #Caixa de texto - Número da Agência Destino
    def entry0_frame_transferencia_focusin(self, event):
        """Função chamada quando o 'self.entry0_frame_transferencia' é clicado"""
        #Se o texto atual é igual ao texto padrão, limpa o Entry
        if self.entry0_frame_transferencia.get() == 'Número da Agência Destino':
            self.entry0_frame_transferencia.delete(0, tk.END)
            self.entry0_frame_transferencia.insert(0, '') #Remove o texto padrão
            self.entry0_frame_transferencia.config(fg = 'black') #Muda a cor do texto para preto

    def entry0_frame_transferencia_focusout(self, event):
        """Função chamada quando o 'self.entry0_frame_transferencia' perde o foco"""
        if self.entry0_frame_transferencia.get() == '':
            self.entry0_frame_transferencia.insert(0, 'Número da Agência Destino')
            self.entry0_frame_transferencia.config(fg = 'grey')

    #Caixa de texto  - Número da Conta Corrente
    def entry1_frame_transferencia_focusin(self, event):
        """Função chamada quando o 'self.entry1_frame_transferencia' é clicado"""
        #Se o texto atual é igual ao texto padrão, limpa o Entry
        if self.entry1_frame_transferencia.get() == 'Número da Conta Corrente Destino':
            self.entry1_frame_transferencia.delete(0, tk.END)
            self.entry1_frame_transferencia.insert(0, '') #Remove o texto padrão
            self.entry1_frame_transferencia.config(fg = 'black') #Muda a cor do texto para preto

    def entry1_frame_transferencia_focusout(self, event):
        """Função chamada quando o 'self.entry1_frame_transferencia' perde o foco"""
        if self.entry1_frame_transferencia.get() == '':
            self.entry1_frame_transferencia.insert(0, 'Número da Conta Corrente Destino')
            self.entry1_frame_transferencia.config(fg = 'grey')

    #Caixa de texto  - Valor
    def entry2_frame_transferencia_focusin(self, event):
        """Função chamada quando o 'self.entry2_frame_transferencia' é clicado"""
        #Se o texto atual é igual ao texto padrão, limpa o Entry
        if self.entry2_frame_transferencia.get() == 'Valor da Transferência':
            self.entry2_frame_transferencia.delete(0, tk.END)
            self.entry2_frame_transferencia.insert(0, '') #Remove o texto padrão
            self.entry2_frame_transferencia.config(fg = 'black') #Muda a cor do texto para preto

    def entry2_frame_transferencia_focusout(self, event):
        """Função chamada quando o 'self.entry2_frame_transferencia' perde o foco"""
        if self.entry2_frame_transferencia.get() == '':
            self.entry2_frame_transferencia.insert(0, 'Valor da Transferência')
            self.entry2_frame_transferencia.config(fg = 'grey')
        
    #Botão 'Ok': Frame Transferência
    def ok_transferir_atualizar_UI(self, dados):
        if dados['status_code'] == 200:
            self.entry_terminal.delete("1.0", "end")
            self.entry_terminal.insert("1.0", dados['text_resp'])
            if dados['saldo_atual'] != None:
                self.canvas.itemconfig(self.saldo_atual, text = f"R$ {dados['saldo_atual']}")
            self.operacao_em_andamento = False
        elif dados['status_code'] == 500:
            self.entry_terminal.delete("1.0", "end")
            self.entry_terminal.insert("1.0", dados['text_resp'])
            self.operacao_em_andamento = False
        elif dados['status_code'] == 503:
            self.entry_terminal.delete("1.0", "end")
            self.entry_terminal.insert("1.0", dados['text_resp'])
            self.operacao_em_andamento = False

    def ok_transferir_thread(self, valor, conta_destino, agencia_destino):
        dados = self.conta_bancaria.transferir(valor = valor,
                                               conta_destino = conta_destino, 
                                               agencia_destino = agencia_destino)
        self.after(0, self.ok_transferir_atualizar_UI, dados)

    def ok_transferir(self):
        """Função responsável por fazer a operação CRUD de transferência"""
        if not self.operacao_em_andamento:
            self.operacao_em_andamento = True
            "Checando se os campos foram preenchidos"
            #Pegar número da agência destino
            agencia_destino = self.entry0_frame_transferencia.get()
            if agencia_destino == 'Número da Agência Destino' or agencia_destino == '':
                aviso = 'Forneça o número da agência da conta destino!'
                self.entry_terminal.delete("1.0", "end")
                self.entry_terminal.insert("1.0", aviso)
                self.operacao_em_andamento = False
                return
            #Pegar número da conta corrente destino
            conta_destino = self.entry1_frame_transferencia.get()
            if conta_destino == 'Número da Conta Corrente Destino' or conta_destino == '':
                aviso = 'Forneça o número da conta corrente destino!'
                self.entry_terminal.delete("1.0", "end")
                self.entry_terminal.insert("1.0", aviso)
                self.operacao_em_andamento = False
                return
            #pegar valor da transferência
            valor = self.entry2_frame_transferencia.get()
            if valor == 'Valor da Transferência' or valor == '':
                aviso = 'Forneça o valor a ser transferido!'
                self.entry_terminal.delete("1.0", "end")
                self.entry_terminal.insert("1.0", aviso)
                self.operacao_em_andamento = False
                return

            "Se os campos foram preenchidos, checar se os valores informados são valores númericos válidos."
            verificacao = {'Agência Destino': agencia_destino, 'Conta Destino': conta_destino, 'Valor': valor}
            for chave, valor in verificacao.items():
                try:
                    valor = float(valor)
                except:
                    aviso = f"Forneça um valor numérico válido para o campo '{chave}' e tente novamente!"
                    self.entry_terminal.delete("1.0", "end")
                    self.entry_terminal.insert("1.0", aviso)
                    self.operacao_em_andamento = False
                    return

            #Se os campos forem preenchidos corretamente, prossegue com a operação de transferência
            valor = float(self.entry2_frame_transferencia.get())
            
            #Verifica se o valor fornecido é negativo
            if valor <= 0:
                aviso = "O valor deve ser um número positivo. Tente novamente!"
                self.entry_terminal.delete("1.0", "end")
                self.entry_terminal.insert("1.0", aviso)
                self.operacao_em_andamento = False
                return
            
            #Realiza a operação de transferência em uma thread secundária
            thread = threading.Thread(target = self.ok_transferir_thread, args = (valor, conta_destino, agencia_destino))
            thread.start()

    # FRAME EXTRATO -------------------------------------------------------------------
    def frame_extrato_mostrar(self):
        "Responsável por exibir o frame de extrato (self.frame_extrato)"
        self.frame_transferencia.place_forget()
        self.frame_deposito.place_forget()
        self.frame_saque.place_forget()
        if self.frame_extrato.winfo_viewable():
            self.frame_extrato.place_forget()
        else:
            self.frame_extrato.place(x = 547, y = 130, width = 240, height = 178)

    def exibir_extrato_atualizar_UI(self, informacoes_extrato_str = None, transacoes = None, aviso = None):
        "Responsável por executar a atualização da UI na thread principal"
        if transacoes is not None:
            self.entry_terminal.delete("1.0", "end")  # Remove todo o texto atual
            self.entry_terminal.insert("1.0", informacoes_extrato_str) 
            for texto_transacao in transacoes:
                self.entry_terminal.insert("end", texto_transacao)  # Insere novo texto
            self.operacao_em_andamento = False
        else:
            if informacoes_extrato_str is not None:
                self.entry_terminal.delete("1.0", "end")  # Remove todo o texto atual
                self.entry_terminal.insert("1.0", informacoes_extrato_str)
                self.entry_terminal.insert("end", aviso)
                self.operacao_em_andamento = False
            else:
                self.entry_terminal.delete("1.0", "end")  # Remove todo o texto atual
                self.entry_terminal.insert("end", aviso)
                self.operacao_em_andamento = False

    def exibir_extrato_thread(self):
        "Executa a operação demora de consulta em uma thread separada"
        
        data_consulta = self.entry_valor_frame_extrato.get_date()
        data_consulta = data_consulta.strftime('%Y-%m-%d')
        dados = self.conta_bancaria.consultar_extrato(data_consulta)

        if dados['status_code'] == 200:
            informacoes_extrato_str = (
                f"---------------------------\n\n"
                f"EXTRATO BANCÁRIO\n\n"
                f"Cliente: {dados['nome']}\n\n"
                f"Conta: {dados['id_conta']}\n\n"
                f"Agência: {dados['agencia_id']}\n\n"
                f"Data: {dados['data_consulta']}\n\n")
            if dados['transacoes'] is not None:
                transacoes = [
                    f"---------------------------\n"
                    f"{transacao['data_transacao']}:\n\n" #Data da transação
                    f"{transacao['tipo']} de R$ {transacao['valor']}\n\n"
                    f"Saldo inicial: R${transacao['saldo_inicial']}\n\n"
                    f"Saldo final: R${transacao['saldo_final']}\n\n" for transacao in dados['transacoes']
                    ]
                self.after(0, self.exibir_extrato_atualizar_UI, informacoes_extrato_str, transacoes)
            else:
                aviso = (
                    "---------------------------\n"
                    f'Não foram realizadas movimentações na data informada.\n'
                    "---------------------------\n"
                    )
                self.after(0, self.exibir_extrato_atualizar_UI, informacoes_extrato_str, aviso)
        
        elif dados['status_code'] == 500:
            aviso = (
                f'Não foi possível realizar a operação. Erro interno do servidor.'
            )
            self.after(0, self.exibir_extrato_atualizar_UI, aviso)
        elif dados['status_code'] == 503:
            aviso = (
                f'Não foi possível realizar a operação. Servidor indisponível no momento.'
            )
            self.after(0, self.exibir_extrato_atualizar_UI, aviso)

        # except:
        #     aviso = f'Não foram realizadas movimentações na data informada.'
        #     #Agenda atualização da UI na thread principal
        #     self.after(0, self.exibir_extrato_atualizar_UI, aviso)

    def exibir_extrato(self):
        """Responsável por exibir o extrato da conta bancária"""
        if not self.operacao_em_andamento:
            self.operacao_em_andamento = True
            thread = threading.Thread(target = self.exibir_extrato_thread)
            thread.start()
