import tkinter as tk
from tkinter import messagebox, scrolledtext
import psutil
import threading
import time
from datetime import datetime

class DigitalSecurityFW:
    def __init__(self, master):
        self.master = master
        master.title("Digital Security FW - Pro")
        master.geometry("450x550")
        master.configure(bg="#2c3e50")

        # Cabeçalho
        tk.Label(master, text="DIGITAL SECURITY FW", fg="white", bg="#2c3e50", font=("Helvetica", 16, "bold")).pack(pady=15)
        
        self.status_label = tk.Label(master, text="Status: PROTEÇÃO DESATIVADA", fg="#e74c3c", bg="#2c3e50", font=("Helvetica", 10, "bold"))
        self.status_label.pack()

        # Botão de Ativação
        self.btn_iniciar = tk.Button(master, text="ATIVAR PROTEÇÃO", command=self.iniciar_thread, bg="#27ae60", fg="white", font=("Helvetica", 10, "bold"), padx=20, pady=10)
        self.btn_iniciar.pack(pady=15)

        # Histórico de Varredura
        tk.Label(master, text="Histórico de Varredura:", fg="white", bg="#2c3e50").pack(pady=(5,0))
        self.log_area = scrolledtext.ScrolledText(master, width=50, height=12, font=("Consolas", 9))
        self.log_area.pack(pady=10, padx=10)
        
        self.protecao_ativa = False

    def escrever_log(self, texto):
        horario = datetime.now().strftime("%H:%M:%S")
        self.log_area.insert(tk.END, f"[{horario}] {texto}\n")
        self.log_area.see(tk.END)

    def iniciar_thread(self):
        # Resolve o erro de atributo garantindo que a thread comece aqui
        if not self.protecao_ativa:
            self.protecao_ativa = True
            self.status_label.config(text="Status: MONITORAMENTO ATIVO", fg="#2ecc71")
            self.btn_iniciar.config(text="PROTEÇÃO LIGADA", state="disabled", bg="#95a5a6")
            
            thread = threading.Thread(target=self.monitorar_processos, daemon=True)
            thread.start()
            self.escrever_log("Escaneamento iniciado com sucesso.")

    def monitorar_processos(self):
        # WHITELIST TOTAL: Adicione aqui os executáveis que mais "gritam" no seu PC
        whitelist_global = (
            "idle", "system", "code.exe", "python.exe", "explorer.exe", 
            "chrome.exe", "msedge.exe", "svchost.exe", "searchindexer.exe",
            "taskmgr.exe", "runtimebroker.exe", "shellexperiencehost.exe"
        )

        while self.protecao_ativa:
            count = 0
            for proc in psutil.process_iter(['name', 'cpu_percent']):
                try:
                    nome = proc.info.get('name', '').lower()
                    cpu = proc.info.get('cpu_percent', 0)
                    count += 1

                    # Ignora se estiver na lista de executáveis seguros
                    if any(app in nome for app in whitelist_global):
                        continue

                    # Só alerta se for algo desconhecido usando MUITA CPU (acima de 85%)
                    if cpu > 85.0: 
                        self.gerar_alerta(proc.info['name'])
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.escrever_log(f"Varredura OK: {count} processos verificados.")
            time.sleep(4) # Intervalo maior para não sobrecarregar o PC

    def gerar_alerta(self, nome_processo):
        self.escrever_log(f"!!! SUSPEITO DETECTADO: {nome_processo} !!!")
        resposta = messagebox.askquestion("Ação Necessária", f"O processo '{nome_processo}' está com consumo crítico.\n\nDeseja encerrar?")
        
        if resposta == 'yes':
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == nome_processo:
                    try:
                        proc.terminate()
                        self.escrever_log(f"Encerrado: {nome_processo}")
                        messagebox.showinfo("Sucesso", "Processo finalizado.")
                        break
                    except:
                        self.escrever_log("Erro: Permissão negada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalSecurityFW(root)
    root.mainloop()