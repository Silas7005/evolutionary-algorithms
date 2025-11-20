# NSGA-II Load Balancing (notebook)

Este repositório contém um notebook de exemplo (NSGA-II) para balanceamento de carga (`nsga2_load_balancing.ipynb`). Abaixo estão instruções para executar o notebook localmente no Windows (PowerShell) usando um ambiente virtual.

Pré-requisitos
- Python 3.10+ (recomendado)
- VS Code ou um navegador para abrir Jupyter Lab/Notebook

Passos (PowerShell)

1) Abrir a pasta do projeto:

```powershell
cd 'C:\Users\silaz\Documents\UFRPE\Intro a IA\nsga2'
```

2) Criar e ativar um ambiente virtual (se ainda não existir):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Instalar dependências (arquivo `requirements.txt` está incluído e gerado a partir do venv atual):

```powershell
pip install -r requirements.txt
```

4) Abrir o notebook interativamente (VS Code ou Jupyter Lab):

- VS Code: abra a pasta, abra `nsga2_load_balancing.ipynb` e selecione o kernel do `.venv` (procure por `\.venv\Scripts\python.exe`).
- Jupyter Lab/Notebook:

```powershell
jupyter lab
# ou
jupyter notebook
```

5) Executar todas as células (ou rodar interativamente). A execução gera arquivos de saída:
- `pareto_plot.html` — gráfico interativo da fronteira de Pareto (latency vs cost)
- `pareto_vals.csv`  — valores salvos da fronteira de Pareto
- `nsga2_load_balancing_executed.ipynb` — resultado da execução headless (se você usar nbconvert)

Execução headless (linha de comando)

Para executar todas as células e salvar o notebook executado:

```powershell
& '.\.venv\Scripts\python.exe' -m jupyter nbconvert --to notebook --execute "nsga2_load_balancing.ipynb" --output "nsga2_load_balancing_executed.ipynb" --ExecutePreprocessor.timeout=600
```

Problemas comuns e soluções rápidas
- Erro "ModuleNotFoundError": ative o `.venv` correto e rode `pip install -r requirements.txt`.
- Kernel do notebook não aparece no VS Code: instale e registre o kernel:

```powershell
pip install ipykernel
python -m ipykernel install --user --name nsga2-env --display-name "nsga2 (.venv)"
```

- Avisos sobre event loop no Windows (zmq): pode ignorar; se preferir, use:

```powershell
# Em Python, antes de iniciar kernels que usam tornado/zmq
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
```

Extras que eu adicionei
- Célula que plota e salva a fronteira de Pareto como `pareto_plot.html` (Plotly) e `pareto_vals.csv`.
- Correção para atribuir crowding distance antes de usar a seleção por torneio (evita AttributeError).

Se quiser que eu:
- Exporte também PNG/SVG automaticamente (adiciono `kaleido`),
- Reduza os parâmetros `NGEN`/`POP_SIZE` para testes mais rápidos,
- Ou adicione instruções para rodar em CI (usando `papermill`),

diga qual opção prefere e eu aplico as alterações.
