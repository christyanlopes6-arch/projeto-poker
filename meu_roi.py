import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os

# Cores Profissionais
COLOR_BG = "#1e1e1e"
COLOR_CARD = "#2d2d2d"
COLOR_ACCENT = "#2ecc71"
COLOR_TEXT = "#ffffff"
COLOR_SUB = "#aaaaaa"

class PokerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LION TRACKER PRO v2.0")
        self.root.geometry("450x750")
        self.root.configure(bg=COLOR_BG)
        
        # Definição de Rakes por Tipo
        self.tipos_rake = {
            "MTT (Regular) - 10%": 0.10,
            "Spin & Go - 7%": 0.07,
            "Sit & Go - 8%": 0.08,
            "Turbo / Hyper - 5%": 0.05,
            "Customizado (0%)": 0.00
        }

        # Título
        tk.Label(root, text="GOLDEN LION", font=("Impact", 28), fg=COLOR_ACCENT, bg=COLOR_BG).pack(pady=(20, 0))
        tk.Label(root, text="INTELIGÊNCIA DE RAKE ATIVADA", font=("Arial", 8, "bold"), fg=COLOR_SUB, bg=COLOR_BG).pack(pady=(0, 20))

        # Container de Inputs
        card = tk.Frame(root, bg=COLOR_CARD, padx=20, pady=20)
        card.pack(padx=30, fill="x")

        # Menu de Seleção de Tipo
        self.create_label(card, "TIPO DE TORNEIO (Define o Rake)")
        self.combo_tipo = ttk.Combobox(card, values=list(self.tipos_rake.keys()), state="readonly", font=("Arial", 10))
        self.combo_tipo.current(0) # Padrão MTT
        self.combo_tipo.pack(pady=(5, 15), fill="x")

        self.create_label(card, "VALOR DO BUY-IN ($)")
        self.e_buyin = self.create_entry(card)
        
        self.create_label(card, "PREMIAÇÃO RECEBIDA ($)")
        self.e_premio = self.create_entry(card)

        # Resultado de ROI
        self.res = tk.Label(root, text="ROI: --%", font=("Segoe UI", 32, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG)
        self.res.pack(pady=10)
        
        self.info_detalhes = tk.Label(root, text="Aguardando cálculo...", font=("Arial", 9), fg=COLOR_SUB, bg=COLOR_BG, justify="center")
        self.info_detalhes.pack()

        # Botões
        tk.Button(root, text="CALCULAR PERFORMANCE", command=self.calcular, font=("Arial", 10, "bold"),
                  bg=COLOR_ACCENT, fg="white", cursor="hand2", bd=0, padx=20, pady=10).pack(pady=10, fill="x", padx=50)

        self.btn_save = tk.Button(root, text="SALVAR NO HISTÓRICO", command=self.salvar, font=("Arial", 10, "bold"),
                                  bg=COLOR_CARD, fg=COLOR_TEXT, cursor="hand2", bd=1, padx=20, pady=10)
        self.btn_save.pack(pady=5, fill="x", padx=50)

        # Lista
        self.lista_hist = tk.Listbox(root, bg=COLOR_CARD, fg=COLOR_TEXT, bd=0, font=("Consolas", 8), highlightthickness=0)
        self.lista_hist.pack(padx=30, pady=20, fill="both", expand=True)

        self.carregar_historico()

    def create_label(self, parent, text):
        tk.Label(parent, text=text, font=("Arial", 7, "bold"), fg=COLOR_SUB, bg=COLOR_CARD).pack(anchor="w")

    def create_entry(self, parent):
        entry = tk.Entry(parent, font=("Arial", 12), bg=COLOR_BG, fg=COLOR_TEXT, bd=0, insertbackground="white", justify="center")
        entry.pack(pady=(2, 8), fill="x")
        tk.Frame(parent, height=2, bg=COLOR_ACCENT).pack(fill="x", pady=(0, 10))
        return entry

    def calcular(self):
        try:
            buyin_puro = float(self.e_buyin.get() or 0)
            premio = float(self.e_premio.get() or 0)
            
            # Pega a porcentagem de rake do menu
            tipo_selecionado = self.combo_tipo.get()
            porcentagem_rake = self.tipos_rake[tipo_selecionado]
            
            valor_rake = buyin_puro * porcentagem_rake
            custo_total = buyin_puro + valor_rake
            lucro = premio - custo_total
            
            roi = (lucro / custo_total * 100) if custo_total > 0 else 0
            
            color = COLOR_ACCENT if roi >= 0 else "#e74c3c"
            self.res.config(text=f"{roi:.1f}%", fg=color)
            
            detalhes = f"Custo Total: ${custo_total:.2f} (Taxa: ${valor_rake:.2f})\nLucro Líquido: ${lucro:.2f}"
            self.info_detalhes.config(text=detalhes)
            
            return custo_total, premio, roi, tipo_selecionado
        except:
            self.res.config(text="ERRO", fg="#f1c40f")
            return None

    def salvar(self):
        dados = self.calcular()
        if dados:
            custo, premio, roi, tipo = dados
            data = datetime.now().strftime("%d/%m")
            tipo_limpo = tipo.split(" ")[0] # Pega só o nome (ex: MTT)
            linha = f"[{data}] {tipo_limpo:<6} | Custo: ${custo:<5.1f} | ROI: {roi:>5.1f}%"
            with open("historico_poker.txt", "a", encoding="utf-8") as f:
                f.write(linha + "\n")
            self.lista_hist.insert(0, linha)
            self.btn_save.config(text="SALVO!", bg="#27ae60")
            self.root.after(2000, lambda: self.btn_save.config(text="SALVAR NO HISTÓRICO", bg=COLOR_CARD))

    def carregar_historico(self):
        if os.path.exists("historico_poker.txt"):
            with open("historico_poker.txt", "r", encoding="utf-8") as f:
                linhas = f.readlines()
                for l in linhas[-15:]:
                    self.lista_hist.insert(0, l.strip())

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerApp(root)
    root.mainloop()