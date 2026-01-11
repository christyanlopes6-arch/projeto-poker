import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

# CORES PREMIUM
COLOR_BG = "#0f111a"
COLOR_HEADER = "#1a1d2e"
COLOR_CARD = "#1c1f2e"
COLOR_ACCENT = "#00ff88"
COLOR_LOSS = "#ff4d4d"
COLOR_TEXT = "#e1e1e6"
COLOR_SUB = "#888b9e"

class PokerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LION TRACKER PRO v3.4")
        self.root.geometry("500x850")
        self.root.configure(bg=COLOR_BG)
        
        self.tipos_rake = {
            "MTT (Regular) - 10%": 0.10,
            "Spin & Go - 7%": 0.07,
            "Sit & Go - 8%": 0.08,
            "Turbo / Hyper - 5%": 0.05,
            "Customizado (0%)": 0.00
        }

        # --- HEADER (Dashboard de Saldo) ---
        self.header = tk.Frame(root, bg=COLOR_HEADER, pady=25)
        self.header.pack(fill="x")
        
        tk.Label(self.header, text="SALDO ACUMULADO", font=("Arial", 9, "bold"), fg=COLOR_SUB, bg=COLOR_HEADER).pack()
        self.lbl_saldo_total = tk.Label(self.header, text="$ 0.00", font=("Arial", 32, "bold"), fg=COLOR_ACCENT, bg=COLOR_HEADER)
        self.lbl_saldo_total.pack(pady=5)

        # --- CONTAINER DE INPUTS ---
        container = tk.Frame(root, bg=COLOR_BG, padx=25, pady=15)
        container.pack(fill="x")

        card = tk.Frame(container, bg=COLOR_CARD, padx=20, pady=20, highlightthickness=1, highlightbackground="#2d3142")
        card.pack(fill="x")

        self.create_label(card, "MODALIDADE")
        self.combo_tipo = ttk.Combobox(card, values=list(self.tipos_rake.keys()), state="readonly")
        self.combo_tipo.current(0)
        self.combo_tipo.pack(pady=(5, 12), fill="x")

        self.create_label(card, "BUY-IN ($)")
        self.e_buyin = self.create_entry(card)
        
        self.create_label(card, "PRÊMIO ($)")
        self.e_premio = self.create_entry(card)

        # --- RESULTADO ---
        self.res = tk.Label(root, text="ROI: --%", font=("Arial", 22, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG)
        self.res.pack(pady=5)
        
        # --- BOTÕES DE AÇÃO ---
        btn_f = tk.Frame(root, bg=COLOR_BG, padx=40)
        btn_f.pack(fill="x")

        tk.Button(btn_f, text="CALCULAR E GUARDAR", command=self.salvar, font=("Arial", 10, "bold"),
                  bg="#3d42f5", fg="white", cursor="hand2", bd=0, pady=12).pack(fill="x", pady=5)

        # --- HISTÓRICO ---
        hist_f = tk.Frame(root, bg=COLOR_BG, padx=25)
        hist_f.pack(fill="x", pady=(20, 0))
        
        tk.Label(hist_f, text="HISTÓRICO (Data/Hora)", font=("Arial", 10, "bold"), fg=COLOR_TEXT, bg=COLOR_BG).pack(side="left")
        
        tk.Button(hist_f, text="🗑 APAGAR TUDO", font=("Arial", 7, "bold"), fg=COLOR_LOSS, bg=COLOR_BG, 
                  bd=0, cursor="hand2", command=self.apagar_historico).pack(side="right", padx=5)
        
        tk.Button(hist_f, text="✖ REMOVER ITEM", font=("Arial", 7, "bold"), fg="#f1c40f", bg=COLOR_BG, 
                  bd=0, cursor="hand2", command=self.remover_selecionado).pack(side="right", padx=5)

        self.lista_hist = tk.Listbox(root, bg=COLOR_CARD, fg=COLOR_TEXT, bd=0, font=("Consolas", 8), 
                                     highlightthickness=0, selectbackground="#3d42f5")
        self.lista_hist.pack(padx=25, pady=10, fill="both", expand=True)

        self.atualizar_saldo_total()
        self.carregar_historico_visual()

    def create_label(self, parent, text):
        tk.Label(parent, text=text, font=("Arial", 7, "bold"), fg=COLOR_SUB, bg=COLOR_CARD).pack(anchor="w")

    def create_entry(self, parent):
        entry = tk.Entry(parent, font=("Arial", 14), bg="#0f111a", fg=COLOR_TEXT, bd=0, justify="center", insertbackground="white")
        entry.pack(pady=(2, 8), fill="x")
        tk.Frame(parent, height=1, bg="#2d3142").pack(fill="x", pady=(0, 10))
        return entry

    def calcular_logica(self):
        try:
            buyin = float(self.e_buyin.get() or 0)
            premio = float(self.e_premio.get() or 0)
            rake = self.tipos_rake[self.combo_tipo.get()]
            custo = buyin * (1 + rake)
            lucro = premio - custo
            roi = (lucro / custo * 100) if custo > 0 else 0
            return custo, premio, lucro, roi, self.combo_tipo.get()
        except:
            messagebox.showerror("Erro", "Insira apenas números.")
            return None

    def salvar(self):
        dados = self.calcular_logica()
        if dados:
            custo, premio, lucro, roi, tipo = dados
            data_hora = datetime.now().strftime("%d/%m %H:%M")
            tipo_id = tipo.split(" ")[0]
            # LINHA ABAIXO DEVE FICAR EM UMA ÚNICA LINHA SEM QUEBRAS:
            linha = f"{data_hora} | {tipo_id:<6} | Lucro: ${lucro:>8.2f} | ROI: {roi:>6.1f}%"
            
            self.res.config(text=f"ROI: {roi:.1f}%", fg=COLOR_ACCENT if roi >= 0 else COLOR_LOSS)
            
            with open("historico_poker.txt", "a", encoding="utf-8") as f:
                f.write(linha + "\n")
            
            self.lista_hist.insert(0, linha)
            self.atualizar_saldo_total()
            self.e_buyin.delete(0, tk.END)
            self.e_premio.delete(0, tk.END)

    def atualizar_saldo_total(self):
        saldo = 0.0
        if os.path.exists("historico_poker.txt"):
            with open("historico_poker.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    if "Lucro: $" in linha:
                        try:
                            val = linha.split("Lucro: $")[1].split(" |")[0]
                            saldo += float(val)
                        except: pass
        self.lbl_saldo_total.config(text=f"$ {saldo:.2f}", fg=COLOR_ACCENT if saldo >= 0 else COLOR_LOSS)

    def remover_selecionado(self):
        selecao = self.lista_hist.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um item.")
            return
        
        item_texto = self.lista_hist.get(selecao)
        if os.path.exists("historico_poker.txt"):
            with open("historico_poker.txt", "r", encoding="utf-8") as f:
                linhas = f.readlines()
            with open("historico_poker.txt", "w", encoding="utf-8") as f:
                for linha in linhas:
                    if linha.strip() != item_texto:
                        f.write(linha)
        
        self.lista_hist.delete(selecao)
        self.atualizar_saldo_total()

    def apagar_historico(self):
        if messagebox.askyesno("Confirmar", "Apagar tudo?"):
            if os.path.exists("historico_poker.txt"): os.remove("historico_poker.txt")
            self.lista_hist.delete(0, tk.END)
            self.atualizar_saldo_total()

    def carregar_historico_visual(self):
        self.lista_hist.delete(0, tk.END)
        if os.path.exists("historico_poker.txt"):
            with open("historico_poker.txt", "r", encoding="utf-8") as f:
                linhas = f.readlines()
                for l in linhas: self.lista_hist.insert(0, l.strip())

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerApp(root)
    root.mainloop()