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
        self.root.title("LION TRACKER PRO v4.0")
        self.root.geometry("850x950")
        self.root.configure(bg=COLOR_BG)
        
        self.tipos_rake = {
            "MTT (Regular) - 10%": 0.10,
            "Spin & Go - 7%": 0.07,
            "Sit & Go - 8%": 0.08,
            "Turbo / Hyper - 5%": 0.05,
            "Customizado (0%)": 0.00
        }

        # --- CABEÇALHO ---
        self.header = tk.Frame(root, bg=COLOR_HEADER, pady=20)
        self.header.pack(fill="x")
        
        # Container para os cards de métricas
        metrics_frame = tk.Frame(self.header, bg=COLOR_HEADER)
        metrics_frame.pack()

        # Card Saldo
        f_saldo = tk.Frame(metrics_frame, bg=COLOR_HEADER, padx=20)
        f_saldo.pack(side="left")
        tk.Label(f_saldo, text="LUCRO LÍQUIDO", font=("Arial", 8, "bold"), fg=COLOR_SUB, bg=COLOR_HEADER).pack()
        self.lbl_saldo_total = tk.Label(f_saldo, text="$ 0.00", font=("Arial", 24, "bold"), fg=COLOR_ACCENT, bg=COLOR_HEADER)
        self.lbl_saldo_total.pack()

        # Card ITM (NOVO!)
        f_itm = tk.Frame(metrics_frame, bg=COLOR_HEADER, padx=20)
        f_itm.pack(side="left")
        tk.Label(f_itm, text="FREQUÊNCIA ITM", font=("Arial", 8, "bold"), fg=COLOR_SUB, bg=COLOR_HEADER).pack()
        self.lbl_itm = tk.Label(f_itm, text="0 / 0 (0%)", font=("Arial", 24, "bold"), fg="#3d42f5", bg=COLOR_HEADER)
        self.lbl_itm.pack()

        # --- INPUTS ---
        container = tk.Frame(root, bg=COLOR_BG, padx=25, pady=10)
        container.pack(fill="x")
        card = tk.Frame(container, bg=COLOR_CARD, padx=20, pady=15, highlightthickness=1, highlightbackground="#2d3142")
        card.pack(fill="x")

        self.create_label(card, "MODALIDADE")
        self.combo_tipo = ttk.Combobox(card, values=list(self.tipos_rake.keys()), state="readonly")
        self.combo_tipo.current(0)
        self.combo_tipo.pack(pady=(5, 10), fill="x")

        self.create_label(card, "BUY-IN ($)")
        self.e_buyin = self.create_entry(card)
        self.create_label(card, "PRÊMIO FINAL ($)")
        self.e_premio = self.create_entry(card)

        tk.Button(root, text="REGISTRAR SESSÃO", command=self.salvar, font=("Arial", 10, "bold"),
                  bg="#3d42f5", fg="white", cursor="hand2", bd=0, pady=12).pack(padx=25, fill="x", pady=10)

        # --- BUSCA E TABELA ---
        search_f = tk.Frame(root, bg=COLOR_BG, padx=25)
        search_f.pack(fill="x", pady=(10, 0))
        self.e_busca = tk.Entry(search_f, font=("Arial", 10), bg=COLOR_CARD, fg=COLOR_TEXT, bd=0, width=15)
        self.e_busca.pack(side="left", padx=5)
        tk.Button(search_f, text="🔍", font=("Arial", 8), bg="#2d3142", fg=COLOR_TEXT, bd=0, command=self.filtrar_historico).pack(side="left")
        tk.Button(search_f, text="DELETAR", font=("Arial", 8), bg=COLOR_LOSS, fg="white", bd=0, command=self.apagar_selecionado).pack(side="right")

        hist_f = tk.Frame(root, bg=COLOR_BG, padx=25)
        hist_f.pack(fill="both", expand=True, pady=10)
        
        self.lista_hist = ttk.Treeview(hist_f, columns=("data", "tipo", "investido", "liquido", "roi"), show="headings")
        for col in self.lista_hist["columns"]: self.lista_hist.heading(col, text=col.upper())
        self.lista_hist.pack(fill="both", expand=True)
        
        self.lista_hist.tag_configure('positivo', foreground=COLOR_ACCENT)
        self.lista_hist.tag_configure('negativo', foreground=COLOR_LOSS)

        self.atualizar_saldo_total()
        self.carregar_historico_visual()

    def create_label(self, parent, text):
        tk.Label(parent, text=text, font=("Arial", 7, "bold"), fg=COLOR_SUB, bg=COLOR_CARD).pack(anchor="w")

    def create_entry(self, parent):
        entry = tk.Entry(parent, font=("Arial", 14), bg="#0f111a", fg=COLOR_TEXT, bd=0, justify="center")
        entry.pack(pady=(2, 8), fill="x")
        tk.Frame(parent, height=1, bg="#2d3142").pack(fill="x", pady=(0, 5))
        return entry

    def salvar(self):
        try:
            buyin = float(self.e_buyin.get() or 0)
            premio = float(self.e_premio.get() or 0)
            rake = self.tipos_rake[self.combo_tipo.get()]
            investido = buyin * (1 + rake)
            liquido = premio - investido
            roi = (liquido / investido * 100) if investido > 0 else 0
            
            # Formato de salvamento: Data;Tipo;Investido;Liquido;ROI;PremioOriginal
            # Adicionamos o PremioOriginal no final para facilitar o cálculo de ITM
            with open("historico_poker.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now().strftime('%d/%m %H:%M')};{self.combo_tipo.get().split(' ')[0]};{investido:.2f};{liquido:.2f};{roi:.1f};{premio:.2f}\n")
            
            self.carregar_historico_visual()
            self.atualizar_saldo_total()
            self.e_buyin.delete(0, tk.END); self.e_premio.delete(0, tk.END)
        except: messagebox.showerror("Erro", "Valores inválidos.")

    def carregar_historico_visual(self):
        for i in self.lista_hist.get_children(): self.lista_hist.delete(i)
        if os.path.exists("historico_poker.txt"):
            with open("historico_poker.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    p = linha.strip().split(";")
                    if len(p) >= 5:
                        tag = 'positivo' if float(p[3]) >= 0 else 'negativo'
                        self.lista_hist.insert("", "end", values=(p[0], p[1], f"$ {p[2]}", f"$ {p[3]}", f"{p[4]}%"), tags=(tag,))

    def filtrar_historico(self):
        termo = self.e_busca.get().lower()
        for i in self.lista_hist.get_children(): self.lista_hist.delete(i)
        if os.path.exists("historico_poker.txt"):
            with open("historico_poker.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    if termo in linha.lower():
                        p = linha.strip().split(";")
                        tag = 'positivo' if float(p[3]) >= 0 else 'negativo'
                        self.lista_hist.insert("", "end", values=(p[0], p[1], f"$ {p[2]}", f"$ {p[3]}", f"{p[4]}%"), tags=(tag,))

    def apagar_selecionado(self):
        item = self.lista_hist.selection()
        if not item: return
        if messagebox.askyesno("Confirmar", "Deletar registro?"):
            data_id = self.lista_hist.item(item)['values'][0]
            with open("historico_poker.txt", "r", encoding="utf-8") as f:
                linhas = [l for l in f if data_id not in l]
            with open("historico_poker.txt", "w", encoding="utf-8") as f:
                f.writelines(linhas)
            self.carregar_historico_visual(); self.atualizar_saldo_total()

    def atualizar_saldo_total(self):
        saldo = 0.0
        total_torneios = 0
        vitorias_itm = 0
        
        if os.path.exists("historico_poker.txt"):
            with open("historico_poker.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    try:
                        p = linha.strip().split(";")
                        saldo += float(p[3])
                        total_torneios += 1
                        # Se houver a 6ª coluna (prêmio bruto), checamos se é > 0
                        # Se não houver (dados antigos), checamos se o lucro líquido foi positivo
                        premio_bruto = float(p[5]) if len(p) > 5 else float(p[3])
                        if premio_bruto > 0:
                            vitorias_itm += 1
                    except: pass
        
        # Cálculo da porcentagem
        porcentagem = (vitorias_itm / total_torneios * 100) if total_torneios > 0 else 0
        
        self.lbl_saldo_total.config(text=f"$ {saldo:.2f}", fg=COLOR_ACCENT if saldo >= 0 else COLOR_LOSS)
        self.lbl_itm.config(text=f"{vitorias_itm} / {total_torneios} ({porcentagem:.1f}%)")

if __name__ == "__main__":
    root = tk.Tk(); app = PokerApp(root); root.mainloop()