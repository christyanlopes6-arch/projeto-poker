🦁 LION TRACKER PRO v2.0
Gestão de Bankroll e Inteligência de ROI para Poker.

O Lion Tracker Pro é uma ferramenta desenvolvida em Python para jogadores de poker que buscam precisão no cálculo de sua lucratividade. Diferente de calculadoras comuns, este sistema aplica automaticamente as taxas de rake (fee) baseadas na modalidade de torneio escolhida, fornecendo o ROI real sobre o investimento total.

🚀 Funcionalidades
Cálculo de ROI Inteligente: Aplica automaticamente taxas de 5% a 10% dependendo do tipo de torneio.

Interface Dark Mode: Design moderno focado em alta legibilidade e aspecto profissional.

Histórico Persistente: Salva suas sessões automaticamente em um banco de dados local (historico_poker.txt).

Feedback Visual: Indicadores coloridos para lucro (verde) e prejuízo (vermelho).

Suporte a Múltiplas Modalidades: MTT, Spin & Go, Sit & Go, Turbo e Hyper.

🛠️ Tecnologias Utilizadas
Python 3.13

Tkinter: Para a interface gráfica (GUI).

Datetime: Para registro temporal das sessões.

File I/O: Para persistência de dados.

📋 Como Instalar e Rodar
Certifique-se de ter o Python instalado.

Organize os arquivos:

Mantenha o arquivo meu_roi.py na pasta C:\ProjetoPoker.

Execute via Terminal:

DOS

cd C:\ProjetoPoker
python meu_roi.py
📊 Regras de Rake Aplicadas
O sistema utiliza as médias de mercado para calcular o custo real da entrada: | Modalidade | Taxa Aplicada | | :--- | :--- | | MTT (Regular) | 10% | | Sit & Go | 8% | | Spin & Go | 7% | | Turbo / Hyper | 5% |

📝 Próximas Implementações
[ ] Integração com Gráficos Lineares (Matplotlib).

[ ] Exportação direta para Excel (.csv).

[ ] Filtro de histórico por data.

DESENVOLVIDO POR CHRISTYANLOPES6-ARCH/
