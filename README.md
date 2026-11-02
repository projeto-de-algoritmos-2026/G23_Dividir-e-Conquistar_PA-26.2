# Preço Justo

Número da Lista: 23<br>
Conteúdo da Disciplina: Dividir e Conquistar<br>

## Alunos

|Matrícula | Aluno |
| -- | -- |
| 242004671 | Gabriel Ferreira |
| 242028735 | Luiz Henrique Tomaz Moreira |

## Sobre

O Preço Justo registra preços de um produto ao longo do tempo e responde a uma pergunta prática: **esta oferta é boa em relação ao que já foi observado?** A referência é a **mediana** do histórico filtrado por produto e período — uma medida que, diferente da média, não se desloca por causa de um preço extremo.

O interesse algorítmico está em **como** essa mediana é obtida. Ordenar todo o histórico para pegar o valor central custa `O(n log n)` e produz muito mais informação do que a pergunta exige. O projeto usa **seleção determinística por mediana das medianas (BFPRT)**, que encontra o k-ésimo menor elemento em **`O(n)` no pior caso**, sem nunca ordenar o conjunto inteiro — apenas grupos de até cinco elementos.

A aplicação tem três abas: **Comparar oferta**, com preço de referência e gráfico; **Meu histórico**, com cadastro e importação de CSV; e **Por dentro do algoritmo**, que exibe os eventos da última seleção — cada partição, com o pivô escolhido e as contagens de menores, iguais e maiores.

### Modelagem do problema

Todo valor monetário usado pelo algoritmo é um **inteiro positivo em centavos**, evitando o erro de arredondamento do ponto flutuante. A conversão de reais para centavos acontece na leitura; a exibição em reais ocorre apenas no fim.

| Símbolo | Significado |
|---|---|
| `p_i` | preço da i-ésima observação, inteiro positivo em centavos |
| `n` | quantidade de observações no produto e período filtrados |
| `k` | posição procurada na ordem crescente, base zero |
| `M` | mediana do histórico, em centavos |
| `o` | preço da oferta avaliada, inteiro positivo em centavos |
| `Δ = o − M` | diferença entre a oferta e a mediana |
| `Δ% = Δ ÷ M × 100` | variação percentual; negativo indica oferta abaixo da mediana |

Com `n` ímpar, `M` é o elemento de posição `⌊n/2⌋` — uma seleção. Com `n` par, `M` é a média dos dois valores centrais — duas seleções — e pode conter **meio centavo**, preservado como `Decimal` no cálculo e arredondado somente na exibição. A comparação usa a mediana exata, não a arredondada.

## Screenshots

As capturas serão adicionadas junto da publicação da interface.

## 🎥 Apresentação do Projeto

O vídeo será disponibilizado após a gravação da apresentação.

## Instalação

Linguagem: Python 3.10 ou superior<br>
Framework: nenhum — apenas a biblioteca padrão (`http.server`, `sqlite3`, `decimal`); interface em HTML, CSS e JavaScript<br>

Pré-requisitos: um navegador para abrir a interface, que roda em um servidor local. Não há dependências externas a instalar, nem arquivo de requisitos.

Clone o projeto e entre na pasta:

```bash
git clone https://github.com/projeto-de-algoritmos-2026/G23_Dividir-e-Conquistar_PA-26.2.git
cd G23_Dividir-e-Conquistar_PA-26.2
```

A interface web será disponibilizada na próxima etapa de publicação. Até lá, o núcleo de seleção é exercitado pela demonstração em linha de comando, descrita em [Uso](#uso).

### Windows — PowerShell

```powershell
py -3 demo.py
py -3 app.py
```

### Linux e macOS

```bash
python3 demo.py
python3 app.py
```

Execute a partir da raiz do projeto, para que `preco_justo/` seja encontrado. O servidor sobe em **http://127.0.0.1:8501**; encerre com Ctrl+C.

## Uso

A demonstração analisa uma oferta contra o histórico fictício de `exemplos/precos.csv`, sem precisar da interface:

```bash
python3 demo.py
```

Ela filtra o `Café Marca A 500g` entre 2026-10-01 e 2026-10-26 — sete observações — e avalia uma oferta de R$ 13,00 contra a mediana de R$ 15,00, imprimindo o resultado em JSON, inclusive as etapas da seleção.

Com a interface publicada, o fluxo é:

1. Abra **http://127.0.0.1:8501** após iniciar o servidor.
2. Em **Meu histórico**, cadastre preços do mesmo produto — incluindo marca e peso no nome — ou importe um CSV.
3. Em **Comparar oferta**, escolha o produto e o período inclusivo de datas.
4. Informe o preço da oferta e veja a mediana de referência, a diferença percentual e a situação.
5. Em **Por dentro do algoritmo**, acompanhe as partições da última seleção, com pivôs e contagens.

### Formato do CSV

| Regra | Valor |
|---|---|
| Codificação e separador | UTF-8, ponto e vírgula |
| Cabeçalho | `produto;loja;data;preco` |
| Data | ISO `AAAA-MM-DD` |
| Preço | reais com vírgula ou ponto decimal, no máximo duas casas, positivo |

Importações **adicionam** observações: reenviar o mesmo arquivo duplica seus registros. O banco fica em `data/precos.sqlite3` e não é versionado. Esta versão não oferece exclusão de registros pela interface.

### Resultado da análise

| Campo | Significado na implementação |
|---|---|
| `quantidade` | Número de observações no produto e período filtrados |
| `mediana_centavos` | Mediana exata do histórico, em centavos; pode terminar em `.5` quando `n` é par |
| `mediana_reais` | A mesma mediana em reais, arredondada apenas para exibição |
| `diferenca_centavos` | `Δ`: quanto a oferta está acima ou abaixo da mediana |
| `variacao_percentual` | `Δ%` com duas casas; negativo significa oferta abaixo da mediana |
| `situacao` | `abaixo`, `acima` ou `igual` |
| `etapas` | Eventos da seleção, quando solicitados: partições com pivô e contagens, e os casos base |

> Os valores decimais saem como strings, para preservar a precisão monetária na serialização. A comparação é com o **histórico registrado pelo próprio usuário**: ela não garante o menor preço do mercado nem prevê preços futuros. Frete e descontos condicionais, se relevantes, devem estar embutidos no valor cadastrado.

## Outros

### Mediana das medianas

O algoritmo resolve o problema da **seleção**: encontrar o k-ésimo menor elemento sem ordenar o conjunto. A dificuldade de uma partição ingênua é o pivô — um pivô ruim deixa quase todos os elementos de um lado, e o pior caso degrada para `O(n²)`. O BFPRT resolve isso **escolhendo o pivô com uma chamada recursiva ao próprio algoritmo**, garantindo que ele caia sempre numa faixa central.

| Passo | Ideia |
|---|---|
| 1 | Divide a entrada em `⌈n/5⌉` grupos de até cinco elementos e ordena cada grupo. Como o tamanho do grupo é limitado, o custo total é `O(n)` |
| 2 | Coleta a mediana de cada grupo e **seleciona recursivamente a mediana dessas medianas** — uma chamada sobre entrada de tamanho `⌈n/5⌉`. Esse é o pivô |
| 3 | Metade das medianas de grupo é menor ou igual ao pivô, e cada uma dessas tem outros dois elementos menores em seu grupo: o pivô tem pelo menos `≈3n/10` elementos de cada lado |
| 4 | Logo, nenhum dos lados passa de `≈7n/10`. Particiona em menores, iguais e maiores — `O(n)` — e recorre **somente** no lado que contém `k` |
| 5 | Daí `T(n) ≤ T(⌈n/5⌉) + T(7n/10 + O(1)) + O(n)`. Como `1/5 + 7/10 = 9/10 < 1`, a soma geométrica converge e `T(n) = O(n)` no pior caso |

A mediana das medianas é o **pivô**, não necessariamente a resposta: ela só garante uma partição equilibrada. Em listas pares, duas seleções são feitas — o fator constante dobra, mas a ordem permanece `O(n)`.

Esta implementação aloca listas auxiliares a cada partição e usa `O(n)` de memória adicional. Apenas grupos de até cinco são ordenados; a ordenação completa nunca é usada para produzir a resposta — ela aparece somente nos testes, como referência independente de correção. O gráfico da interface ordena observações por data, o que é apresentação, não seleção.

Não se promete vantagem de tempo sobre `sorted` em conjuntos pequenos: a constante do BFPRT é alta e o `sorted` do Python é implementado em C. O ganho é assintótico e de pior caso garantido.

### Estrutura do projeto

```text
G23_Dividir-e-Conquistar_PA-26.2/
├── README.md
├── .gitignore
├── app.py                  # Servidor local e rotas JSON, na porta 8501
├── engine.py               # Adapter do núcleo e importação do CSV enviado pela interface
├── storage.py              # Persistência das observações em SQLite
├── demo.py                 # Demonstração do núcleo em linha de comando
├── exemplos/
│   └── precos.csv          # Histórico fictício de exemplo
├── preco_justo/            # Núcleo algorítmico, independente da interface
│   ├── __init__.py         # Fachada: selecionar, mediana, analisar_oferta, carregar_csv, filtrar_historico
│   ├── core.py             # Seleção BFPRT, mediana em Decimal e comparação da oferta
│   └── historico.py        # Leitura de CSV e filtro por produto e período
├── tests/
│   ├── test_core.py        # Seleção e mediana contra ordenação de referência; entradas inválidas
│   └── test_historico.py   # Importação de CSV, filtros e rejeição de registros inválidos
└── web/                    # Interface em HTML, CSS e JavaScript — a publicar
```
