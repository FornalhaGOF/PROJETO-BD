# Guia de apresentação — Projeto 10: Dashboard de Vendas

> Repositório público + demo ao vivo. Este guia amarra cada fala aos critérios da
> **Ficha de Avaliação de Projetos** (`Ficha_Avaliacao_Projetos.pdf`).

---

## 0. Resumo da ficha (o que o professor vai pontuar)

| Critério | Peso | Nota máx. | O que ele observa |
|----------|------|-----------|-------------------|
| Objetivos e requisitos | 30% | 3,0 | atendeu à proposta, escopo e entregas previstas |
| Qualidade dos resultados | 25% | 2,5 | qualidade, coerência e utilidade do que foi feito |
| Planejamento e organização | 15% | 1,5 | método, etapas, cumprimento de prazos |
| Análise e solução de problemas | 15% | 1,5 | argumentação, verificação dos números, soluções adotadas |
| Apresentação e registros | 15% | 1,5 | clareza, demonstração ao vivo e documentação |
| **Total** | **100%** | **10,0** | |

**Leitura prática:** 55% da nota vem de *mostrar que o escopo pedido está pronto e funciona*
(objetivos + qualidade). Os outros 45% vêm de *saber explicar* o que fez, como testou e como
resolveu os problemas.

---

## 1. No dia anterior (checklist de 20 minutos)

Execute tudo **uma vez** antes, para não descobrir problema na frente da turma:

```powershell
cd C:\Users\gofor\OneDrive\Desktop\escola\bdd\PROJETOS\ProjetoBD-4Bimestre
scripts\iniciar_mongodb.bat
.\.venv\Scripts\Activate.ps1
python verificar_ambiente.py
python -m unittest discover -s tests -t . -v
python -m p10_dashboard.main
```

Checklist:

- [ ] MongoDB sobe (janela "MongoDB" minimizada aparece)
- [ ] `verificar_ambiente.py` termina com "Ambiente pronto"
- [ ] Os 6 testes passam (`OK`)
- [ ] O gráfico `p10_dashboard\grafico_vendas.png` abre
- [ ] O repositório no GitHub está **público** (abra o link em uma aba anônima)
- [ ] Você tem o link do repositório copiado para colar no chat/quadro

> Deixe **duas janelas** abertas antes de começar: uma no terminal (já na pasta do projeto,
> com o venv ativado) e outra no navegador com o repositório aberto.

---

## 2. Roteiro de 10 minutos (fala + demo)

### ⏱ 0:00–1:00 — Abertura (critério: Objetivos e requisitos)

> "Meu projeto é o **Dashboard de Vendas**, o projeto 10 do material de MongoDB com Python.
> O objetivo é ler as vendas gravadas no MongoDB, consolidar por categoria com **aggregation
> pipeline** e gerar três entregas: relatório no terminal, ranking dos produtos mais vendidos
> e um gráfico em PNG. Está no GitHub, público, no link [mostre o link]."

**Mostre o repositório aberto** e aponte a estrutura: `conexao.py`, as 10 pastas `p01`…`p10`,
`tests/`, `README_DO_PROJETO.md`.

### ⏱ 1:00–3:00 — Modelagem (critério: Qualidade dos resultados)

Abra o `README_DO_PROJETO.md` na seção **5. Modelo de dados** e diga:

> "Cada venda é um documento. Eu guardo valores em **centavos, como inteiro**, para não ter
> erro de arredondamento de ponto flutuante. O `total_centavos` fica gravado no documento —
> é uma desnormalização consciente, para o relatório não recalcular a multiplicação toda vez.
> O campo `codigo` tem **índice único**, e criei um índice composto `(categoria, data)` para
> os filtros por período e o agrupamento por categoria."

### ⏱ 3:00–6:00 — Demonstração ao vivo (critério: Apresentação e registros)

No terminal, execute (ou mostre a saída já pronta se o tempo estiver curto):

```powershell
python -m p10_dashboard.main
```

Enquanto roda, explique os 3 passos:

> "Primeiro o script **semeia** os dados de exemplo. Depois roda o pipeline: `$match` filtra o
> período, `$group` soma o faturamento e as unidades por categoria, e `$sort` ordena do maior
> para o menor. No fim ele gera o PNG e o CSV."

Aponte na tela os números:

- Informática: **R$ 5.676,40**, 13 unidades
- Móveis: **R$ 1.658,00**, 2 unidades
- Papelaria: **R$ 533,30**, 37 unidades
- **Faturamento geral: R$ 7.867,70 | 52 unidades**
- Top 1: **Notebook, R$ 3.499,00**

Abra `p10_dashboard\grafico_vendas.png`.

**Segunda execução (o ponto alto da demo):**

```powershell
python -m p10_dashboard.main
```

> "Repare que os totais são **idênticos**. Isso é idempotência: cada venda tem um `codigo`
> único e o insert usa `upsert` com `$setOnInsert`. Rodar dez vezes não duplica nada.
> Se eu quisesse dados novos, mudaria o código da venda."

**Filtro por período (desafio extra):**

```powershell
python -m p10_dashboard.main --dias 7 --top 3 --sem-grafico
```

> "Aqui o `$match` por data entra em ação: só os últimos 7 dias, e o ranking cai para 3."

### ⏱ 6:00–8:00 — Verificação e problemas resolvidos (critérios: Análise e solução de problemas + Planejamento)

Rode os testes:

```powershell
python -m unittest discover -s tests -t . -v
```

> "São 6 testes. Eles verificam que a carga não duplica, que o índice único funciona, que a
> soma do relatório bate com a soma dos documentos e que o formato de moeda está correto."

Conte **três problemas reais** que você resolveu — isso vale 1,5 ponto:

1. **Duplicação de dados**: a primeira versão inseria com `insert_one` e duplicava a cada
   execução. Troquei por `update_one` + `upsert` + `$setOnInsert` com índice único em `codigo`.
2. **Valores monetários**: `float` gerava centavos errados na soma. Passei tudo para inteiro
   em centavos e formatei com padrão brasileiro (`R$ 5.676,40`).
3. **Acentos no terminal**: o console do Windows usa cp1252; resolvi formatando a saída e
   usando UTF-8 nos arquivos, mantendo o gráfico com rótulos acentuados.

### ⏱ 8:00–10:00 — Fechamento (critério: Objetivos e requisitos)

> "Entreguei: os 10 projetos do material funcionando, o dashboard com relatório, ranking,
> gráfico e CSV, testes automatizados e a documentação. Os desafios extras foram o filtro por
> período, o ranking configurável e a exportação em CSV. Como evolução, eu colocaria isso numa
> API com FastAPI — que já está implementada no projeto 09 — e um painel web consumindo os dados."

---

## 3. Mapa critério → evidência (para não perder ponto)

| Critério da ficha | O que mostrar |
|-------------------|---------------|
| Objetivos e requisitos (3,0) | Link do repo público + estrutura de pastas + as 3 entregas do projeto 10 |
| Qualidade dos resultados (2,5) | Números coerentes, gráfico legível, CSV, idempotência |
| Planejamento e organização (1,5) | README, `requirements.txt`, `.env.example`, `.gitignore`, scripts, histórico de commits |
| Análise e solução de problemas (1,5) | Os 3 problemas acima + testes passando + `verificar_ambiente.py` |
| Apresentação e registros (1,5) | Fala cronometrada, demo ao vivo, gráfico e prints salvos |

---

## 4. Perguntas prováveis (e respostas curtas)

**"Por que MongoDB e não SQL?"**
Porque o dado de venda é um documento com estrutura variável; o aggregation pipeline resolve
o relatório em uma consulta, sem `JOIN` nem `GROUP BY` separado.

**"O que é `$group`?"**
É a etapa do pipeline que agrupa documentos por uma chave (`_id`) e aplica acumuladores como
`$sum` e `$avg` — equivalente ao `GROUP BY` do SQL.

**"Por que guardar `total_centavos` se dá para calcular?"**
Porque o total é imutável depois da venda e evita recalcular em cada leitura. É desnormalização
proposital, comum em modelagem de documentos.

**"Como você garante que não duplica?"**
Índice único em `codigo` + `upsert` com `$setOnInsert`. O banco rejeita o duplicado e o script
é idempotente.

**"E se o MongoDB estiver desligado?"**
O `conexao.py` faz `ping` na inicialização e devolve uma mensagem clara dizendo para rodar
`scripts\iniciar_mongodb.bat` — em vez de estourar um `ServerSelectionTimeoutError` cru.

**"Isso serve para produção?"**
Não como está: faltaria autenticação, backup, logs e testes de carga. É um projeto didático.

**"Quanto tempo levou / como você organizou?"**
Cite as etapas: ambiente → conexão → modelagem → carga idempotente → pipeline → relatório →
gráfico → testes → documentação. Isso responde o critério de planejamento.

---

## 5. Plano B (se algo falhar na hora)

| Problema | Ação rápida |
|----------|-------------|
| MongoDB não sobe | `scripts\iniciar_mongodb.bat` e aguarde 4 s; confira a porta 27017 |
| "Não foi possível conectar" | O `.env` está na raiz? O MongoDB está rodando? |
| `python` não encontrado | Use `.\.venv\Scripts\python.exe -m p10_dashboard.main` |
| Sem internet | Tudo roda local (MongoDB portátil) — só o link do GitHub precisa de internet |
| Gráfico não abre | Mostre o PNG já gerado na pasta (é só um arquivo) |
| Tempo curto | Pule o `--dias 7` e vá direto para os testes e o fechamento |

**Frase de segurança:** "Se a demo falhar, os resultados já estão documentados no README e nas
capturas de tela do repositório." — por isso tire os prints **antes**.

---

## 6. Evidências para anexar (critério Apresentação e registros)

1. Print do terminal com o relatório completo.
2. Print do `grafico_vendas.png` aberto.
3. Print dos testes com `OK`.
4. Print do MongoDB Compass mostrando `laboratorio_python` → `vendas_p10` (ou do
   `verificar_ambiente.py` listando as coleções, se o Compass não estiver instalado).
5. Link do repositório público.

Salve os prints em uma pasta `evidencias/` **fora do versionamento** (ou anexe no relatório).
