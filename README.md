# Preço Justo

Número da Lista: 23  
Conteúdo da Disciplina: Dividir e Conquistar

## Alunos

| Matrícula | Aluno |
|---|---|
| 242004671 | [Gabriel Ferreira](https://github.com/diangellis) |
| 242028735 | [Luiz Henrique Tomaz Moreira](https://github.com/luizhtmoreira) |

## Sobre

O Preço Justo registra preços de um produto e compara uma oferta com a mediana do histórico selecionado. O objetivo é oferecer uma referência baseada nas observações do usuário e demonstrar a seleção determinística por mediana das medianas.

A aplicação tem três abas: **Comparar oferta**, com preço de referência e gráfico; **Meu histórico**, com cadastro e importação de CSV; e **Por dentro do algoritmo**, com explicação e eventos da última seleção.


A comparação de ofertas estará disponível após a integração do núcleo de seleção.

## Screenshots

As capturas serão adicionadas junto da publicação da interface.



## 🎥 Apresentação do Projeto

O vídeo será disponibilizado após a gravação da apresentação.

## Instalação

A interface será disponibilizada na próxima etapa de publicação.

Linguagem: Python 3.10 ou superior. Interface: HTML, CSS e JavaScript, servidos localmente pela biblioteca padrão do Python. Nenhuma dependência externa é necessária para esta entrega.

```bash
git clone https://github.com/projeto-de-algoritmos-2026/G23_Dividir-e-Conquistar_PA-26.2.git
cd G23_Dividir-e-Conquistar_PA-26.2
python app.py
```

No Windows, pode-se usar `py -3 app.py`; no Linux/macOS, `python3 app.py`. Abra **http://127.0.0.1:8501**. Encerre com Ctrl+C.

## Uso

1. Em Meu histórico, cadastre preços do mesmo produto, incluindo marca e peso no nome, ou carregue o exemplo fictício.
2. Em Comparar oferta, escolha o produto e o período inclusivo de datas.
3. Informe o preço da oferta. Com o núcleo integrado, a aplicação mostra mediana, diferença percentual e situação acima/abaixo/igual.
4. Consulte o gráfico e as etapas na aba do algoritmo.

CSV: UTF-8, ponto e vírgula, cabeçalho `produto;loja;data;preco`. Datas em `AAAA-MM-DD`; valores em reais com vírgula ou ponto decimal e no máximo duas casas. Importações adicionam observações; repetir um arquivo duplica seus registros. O banco fica em `data/precos.sqlite3` e não é versionado. A interface não oferece exclusão nesta versão.

## Outros

### Mediana das medianas

Os preços internos são centavos inteiros positivos. A seleção divide a entrada em grupos de até cinco, encontra suas medianas, seleciona recursivamente um pivô e particiona o conjunto. A mediana das medianas é um pivô, não necessariamente a mediana final. Em listas pares, a média dos dois valores centrais pode conter meio centavo, preservado no cálculo e arredondado apenas na exibição.

No núcleo combinado: tempo O(n) no pior caso e memória adicional O(n). O gráfico ordena observações por data; essa ordenação não substitui a seleção dos preços. A comparação com o histórico não garante o menor preço disponível nem prevê valores futuros.

### Estrutura do projeto

```text
app.py           Servidor local e rotas
storage.py       Banco SQLite
engine.py        Adapter para o núcleo e importação CSV
web/             Interface, estilos e comportamento
tests/           Testes da entrega de interface
preco_justo/     Núcleo a integrar pelo Luiz
```
