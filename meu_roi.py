import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

# CONFIGURAÇÃO DE CORES
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
        self.root.title("LION TRACKER PRO v3.6")
        self.root.geometry("600x900")
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
        
        tk.Label(self.header, text="SALDO ACUMULADO", font=("Arial", 9, "bold"), fg=COLOR_SUB, bg=COLOR_HEADER).pack()
        self.lbl_saldo_total = tk.Label(self.header, text="$ 0.00", font=("Arial", 32, "bold"), fg=COLOR_ACCENT, bg=COLOR_HEADER)
        self.lbl_saldo_total.pack(pady=5)

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
        
        self.create_label(card, "PRÊMIO ($)")
        self.e_premio = self.create_entry(card)

        tk.Button(root, text="CALCULAR E GUARDAR", command=self.salvar, font=("Arial", 10, "bold"),
                  bg="#3d42f5", fg="white", cursor="hand2", bd=0, pady=10).pack(padx=25, fill="x", pady=10)

        # --- SEÇÃO DE BUSCA/FILTRO ---
        search_f = tk.Frame(root, bg=COLOR_BG, padx=25)
        search_f.pack(fill="x", pady=(10, 0))
        
        tk.Label(search_f, text="BUSCAR POR DATA (ex: 11/01):", font=("Arial", 8, "bold"), fg=COLOR_SUB, bg=COLOR_BG).pack(side="left")
        
        self.e_busca = tk.Entry(search_f, font=("Arial", 10), bg=COLOR_CARD, fg=COLOR_TEXT, bd=0, width=10)
        self.e_busca.pack(side="left", padx=5)
        
        tk.Button(search_f, text="🔍", font=("Arial", 8, "bold"), bg="#2d3142", fg=COLOR_TEXT, bd=0, padx=10, command=self.filtrar_historico).pack(side="left")
        tk.Button(search_f, text="↺", font=("Arial", 8, "bold"), bg="#2d3142", fg=COLOR_TEXT, bd=0, padx=10, command=self.carregar_historico_visual).pack(side="left", padx=2)

        # --- TABELA ---
        hist_f = tk.Frame(root, bg=COLOR_BG, padx=25)
        hist_f.pack(fill="both", expand=True, pady=10)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COLOR_CARD, foreground=COLOR_TEXT, fieldbackground=COLOR_CARD, borderwidth=0)
        style.configure("Treeview.Heading", background=COLOR_HEADER, foreground=COLOR_TEXT, font=("Arial", 8, "bold"))

        self.lista_hist = ttk.Treeview(hist_f, columns=("data", "tipo", "lucro", "roi"), show="headings", height=12)
        self.lista_hist.heading("data", text="DATA/HORA")
        self.lista_hist.heading("tipo", text="TIPO")
        self.lista_hist.heading("lucro", text="LUCRO")
        self.lista_hist.heading("roi", text="ROI")
        
        self.lista_hist.column("data", width=100, anchor="center")
        self.lista_hist.column("tipo", width=100, anchor="center")
        self.lista_hist.column("lucro", width=100, anchor="center")
        self.lista_hist.column("roi", width=80, anchor="center")
        
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
            custo = buyin * (1 + rake)
            lucro = premio - custo
            roi = (lucro / custo * 100) if custo > 0 else 0
            
            data_hora = datetime.now().strftime("%d/%m %H:%M")
            tipo_limpo = self.combo_tipo.get().split(" ")[0]
            
            with open("historico_poker.txt", "a", encoding="utf-8") as f:
                f.write(f"{data_hora};{tipo_limpo};{lucro:.2f};{roi:.1f}\n")
            
            self.carregar_historico_visual()
            self.atualizar_saldo_total()
            self.e_buyin.delete(0, tk.END); self.e_premio.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", "Verifique os valores inseridos.")

    def carregar_historico_visual(self):
        # Limpa a tabela antes de carregar
        for i in self.lista_hist.get_children(): self.lista_hist.delete(i)
        self.e_busca.delete(0, tk.END) # Limpa campo de busca
        
        if os.path.exists("historico_poker.txt"):
            with open("historico_poker.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    self.adicionar_linha_tabela(linha)

    def filtrar_historico(self):
        termo = self.e_busca.get().strip()
        if not termo:
            return self.carregar_historico_visual()
            
        for i in self.lista_hist.get_children(): self.lista_hist.delete(i)
        
        if os.path.exists("historico_poker.txt"):
            with open("historico_poker.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    if termo in linha: # Se a data digitada estiver na linha
                        self.adicionar_linha_tabela(linha)

    def adicionar_linha_tabela(self, linha):
        try:
            partes = linha.strip().split(";")
            if len(partes) == 4:
                tag = 'positivo' if float(partes[2]) >= 0 else 'negativo'
                self.lista_hist.insert("", 0, values=(partes[0], partes[1], f"$ {partes[2]}", f"{partes[3]}%"), tags=(tag,))
        except: pass

    def atualizar_saldo_total(self):
        saldo = 0.0
        if os.path.exists("historico_poker.txt"):
            with open("historico_poker.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    try: saldo += float(linha.strip().split(";")[2])
                    except: pass
        self.lbl_saldo_total.config(text=f"$ {saldo:.2f}", fg=COLOR_ACCENT if saldo >= 0 else COLOR_LOSS)

    def apagar_historico(self):
        if messagebox.askyesno("Limpar", "Apagar histórico permanente?"):
            if os.path.exists("historico_poker.txt"): os.remove("historico_poker.txt")
            self.carregar_historico_visual(); self.atualizar_saldo_total()

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerApp(root)
    root.mainloop()