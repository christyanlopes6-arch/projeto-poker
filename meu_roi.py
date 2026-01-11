import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

# CONFIGURAÇÕES DE INTERFACE
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
        self.root.title("LION TRACKER PRO v6.0 - Advanced Analytics")
        self.root.geometry("1100x950")
        self.root.configure(bg=COLOR_BG)
        
        self.tipos_rake = {
            "MTT (Regular) - 10%": 0.10, "Spin & Go - 7%": 0.07,
            "Sit & Go - 8%": 0.08, "Turbo / Hyper - 5%": 0.05,
            "Customizado (0%)": 0.00
        }

        self.sugestoes_nomes = [
            "888 - Big Shot", "Bodog - The Whale", "Chico - Main Event", 
            "iPoker - Elite Series", "Sunday Million", "Bounty Builder"
        ]

        # --- CABEÇALHO PRINCIPAL ---
        self.header = tk.Frame(root, bg=COLOR_HEADER, pady=20)
        self.header.pack(fill="x")
        
        # Grid de Métricas Rápidas
        self.m_frame = tk.Frame(self.header, bg=COLOR_HEADER)
        self.m_frame.pack()

        self.lbl_saldo_total = tk.Label(self.m_frame, text="$ 0.00", font=("Arial", 32, "bold"), fg=COLOR_ACCENT, bg=COLOR_HEADER)
        self.lbl_saldo_total.pack()
        self.lbl_itm_top = tk.Label(self.m_frame, text="ITM: 0%", font=("Arial", 10, "bold"), fg=COLOR_SUB, bg=COLOR_HEADER)
        self.lbl_itm_top.pack()

        # --- CORPO DO PROGRAMA (Split Lateral) ---
        self.body = tk.Frame(root, bg=COLOR_BG, padx=20, pady=10)
        self.body.pack(fill="both", expand=True)

        # Lado Esquerdo: Inputs e Estatísticas
        self.left_panel = tk.Frame(self.body, bg=COLOR_BG, width=300)
        self.left_panel.pack(side="left", fill="y", padx=(0, 20))

        # Card de Estatísticas Avançadas
        self.stats_card = tk.Frame(self.left_panel, bg=COLOR_CARD, padx=15, pady=15, highlightthickness=1, highlightbackground="#2d3142")
        self.stats_card.pack(fill="x", pady=(0, 15))
        
        tk.Label(self.stats_card, text="ESTATÍSTICAS DO JOGADOR", font=("Arial", 10, "bold"), fg=COLOR_ACCENT, bg=COLOR_CARD).pack(anchor="w", pady=(0,10))
        
        self.stats_labels = {}
        for metric in ["Contagem", "Lucro Méd", "Stake Méd", "ROI Méd", "Lucro"]:
            f = tk.Frame(self.stats_card, bg=COLOR_CARD)
            f.pack(fill="x", pady=2)
            tk.Label(f, text=f"{metric}:", font=("Arial", 9), fg=COLOR_SUB, bg=COLOR_CARD).pack(side="left")
            self.stats_labels[metric] = tk.Label(f, text="---", font=("Arial", 9, "bold"), fg=COLOR_TEXT, bg=COLOR_CARD)
            self.stats_labels[metric].pack(side="right")

        # Card de Inputs
        self.input_card = tk.Frame(self.left_panel, bg=COLOR_CARD, padx=15, pady=15, highlightthickness=1, highlightbackground="#2d3142")
        self.input_card.pack(fill="x")
        
        self.create_label(self.input_card, "NOME DO TORNEIO")
        self.e_nome = tk.Entry(self.input_card, font=("Arial", 11), bg="#0f111a", fg=COLOR_TEXT, bd=0, insertbackground="white")
        self.e_nome.pack(pady=(2, 8), fill="x")
        self.e_nome.bind('<KeyRelease>', self.check_autocomplete)

        self.create_label(self.input_card, "BUY-IN ($)")
        self.e_buyin = self.create_entry(self.input_card)
        
        self.create_label(self.input_card, "PRÊMIO ($)")
        self.e_premio = self.create_entry(self.input_card)

        self.combo_tipo = ttk.Combobox(self.input_card, values=list(self.tipos_rake.keys()), state="readonly")
        self.combo_tipo.current(0)
        self.combo_tipo.pack(pady=10, fill="x")

        tk.Button(self.input_card, text="SALVAR", command=self.salvar, bg="#3d42f5", fg="white", font=("Arial", 10, "bold"), bd=0, pady=8).pack(fill="x")

        # Lado Direito: Histórico e Filtro
        self.right_panel = tk.Frame(self.body, bg=COLOR_BG)
        self.right_panel.pack(side="right", fill="both", expand=True)

        # Barra de Pesquisa
        search_f = tk.Frame(self.right_panel, bg=COLOR_BG)
        search_f.pack(fill="x", pady=(0, 10))
        tk.Label(search_f, text="🔍", font=("Arial", 12), fg=COLOR_SUB, bg=COLOR_BG).pack(side="left")
        self.e_filtro = tk.Entry(search_f, font=("Arial", 12), bg=COLOR_CARD, fg=COLOR_TEXT, bd=0, insertbackground="white")
        self.e_filtro.pack(side="left", padx=10, fill="x", expand=True)
        self.e_filtro.bind('<KeyRelease>', lambda e: self.atualizar_tudo())

        # Tabela
        self.lista_hist = ttk.Treeview(self.right_panel, columns=("data", "nome", "inv", "lucro"), show="headings")
        self.lista_hist.heading("data", text="DATA (Recent ▽)")
        self.lista_hist.heading("nome", text="TORNEIO")
        self.lista_hist.heading("inv", text="STAKE")
        self.lista_hist.heading("lucro", text="LUCRO")
        self.lista_hist.column("data", width=130)
        self.lista_hist.pack(fill="both", expand=True)
        
        self.lista_hist.tag_configure('positivo', foreground=COLOR_ACCENT)
        self.lista_hist.tag_configure('negativo', foreground=COLOR_LOSS)

        self.atualizar_tudo()

    def create_label(self, parent, text):
        tk.Label(parent, text=text, font=("Arial", 7, "bold"), fg=COLOR_SUB, bg=COLOR_CARD).pack(anchor="w")

    def create_entry(self, parent):
        e = tk.Entry(parent, font=("Arial", 12), bg="#0f111a", fg=COLOR_TEXT, bd=0, insertbackground="white")
        e.pack(pady=(2, 8), fill="x")
        tk.Frame(parent, height=1, bg="#2d3142").pack(fill="x", pady=(0, 5))
        return e

    def check_autocomplete(self, event):
        if event.keysym in ["BackSpace", "Return", "Left", "Right"]: return
        pasted = self.e_nome.get()
        if not pasted: return
        for s in self.sugestoes_nomes:
            if s.lower().startswith(pasted.lower()):
                self.e_nome.delete(0, tk.END)
                self.e_nome.insert(0, s)
                self.e_nome.selection_range(len(pasted), tk.END)
                break

    def salvar(self):
        try:
            buyin = float(self.e_buyin.get() or 0)
            premio = float(self.e_premio.get() or 0)
            nome = self.e_nome.get() or "Sessão"
            rake = self.tipos_rake[self.combo_tipo.get()]
            investido = buyin * (1 + rake)
            lucro = premio - investido
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open("historico_poker.txt", "a", encoding="utf-8") as f:
                f.write(f"{timestamp};{nome};{investido:.2f};{lucro:.2f};{premio:.2f}\n")
            
            self.atualizar_tudo()
            self.e_buyin.delete(0, tk.END); self.e_premio.delete(0, tk.END); self.e_nome.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos.")

    def atualizar_tudo(self):
        for i in self.lista_hist.get_children(): self.lista_hist.delete(i)
        
        registros = []
        filtro = self.e_filtro.get().lower()
        
        # Stats variabes
        total_lucro, total_investido, count, itm_count = 0.0, 0.0, 0, 0

        if os.path.exists("historico_poker.txt"):
            with open("historico_poker.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    p = linha.strip().split(";")
                    if len(p) >= 5:
                        registros.append(p)
            
            # ORDENAÇÃO POR DATA (Mais recente no topo)
            registros.sort(key=lambda x: x[0], reverse=True)

            for p in registros:
                data_iso, nome, inv, lucro, premio = p[0], p[1], float(p[2]), float(p[3]), float(p[4])
                data_br = datetime.strptime(data_iso, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%y %H:%M')
                
                if filtro in nome.lower() or filtro in data_br:
                    # Incrementa estatísticas
                    total_lucro += lucro
                    total_investido += inv
                    count += 1
                    if premio > 0: itm_count += 1
                    
                    tag = 'positivo' if lucro >= 0 else 'negativo'
                    self.lista_hist.insert("", "end", values=(data_br, nome, f"$ {inv:.2f}", f"$ {lucro:.2f}"), tags=(tag,))

        # CÁLCULOS AVANÇADOS
        lucro_med = total_lucro / count if count > 0 else 0
        stake_med = total_investido / count if count > 0 else 0
        roi = (total_lucro / total_investido * 100) if total_investido > 0 else 0
        itm_perc = (itm_count / count * 100) if count > 0 else 0

        # ATUALIZA UI
        self.lbl_saldo_total.config(text=f"$ {total_lucro:.2f}", fg=COLOR_ACCENT if total_lucro >= 0 else COLOR_LOSS)
        self.lbl_itm_top.config(text=f"ITM: {itm_perc:.1f}% | ROI Total: {roi:.1f}%")
        
        self.stats_labels["Contagem"].config(text=str(count))
        self.stats_labels["Lucro Méd"].config(text=f"$ {lucro_med:.2f}", fg=COLOR_ACCENT if lucro_med >= 0 else COLOR_LOSS)
        self.stats_labels["Stake Méd"].config(text=f"$ {stake_med:.2f}")
        self.stats_labels["ROI Méd"].config(text=f"{roi:.1f}%", fg=COLOR_ACCENT if roi >= 0 else COLOR_LOSS)
        self.stats_labels["Lucro"].config(text=f"$ {total_lucro:.2f}", fg=COLOR_ACCENT if total_lucro >= 0 else COLOR_LOSS)

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerApp(root)
    root.mainloop()