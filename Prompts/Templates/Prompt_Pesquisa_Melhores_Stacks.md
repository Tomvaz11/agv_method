# Template de Solicitação de Pesquisa Profunda

## Projeto  
Desenvolver, em **Python**, uma aplicação desktop (**Windows**, **sem web**) para **detectar fotos e vídeos idênticos/duplicados**, composta por backend e frontend.

---

## Objetivo da Pesquisa  
Levantar, comparar e ranquear as **melhores opções atuais** (ferramentas, bibliotecas, frameworks, etc.) para cada camada da stack descrita abaixo, considerando popularidade, maturidade, desempenho e facilidade de uso.

---

## Escopo da Pesquisa

| # | Camada / Tema | Perguntas-chave |
|---|---------------|-----------------|
| **1** | **GUI (Frontend)** | - Quais frameworks/bibliotecas GUI mais modernos, utilizados e bem-mantidos para aplicações Python **desktop Windows**?<br>- Quais oferecem melhor performance, experiência do usuário e ecossistema de componentes? |
| **2** | **Motor de Escaneamento de Duplicatas Idênticas** | - Quais bibliotecas especializadas (imagens e vídeos) são líderes de mercado para **cálculo de hash criptográfico** e comparação byte-a-byte?<br>- Quais apresentam **melhor desempenho** (tempo de processamento, uso de memória, GPU opcional)? |
| **3** | **Manipulação de Arquivos & Sistema** | - Quais bibliotecas Python recomendadas para operações intensivas de I/O (cópia, exclusão, restauração) com suporte robusto a **multithreading/multiprocessing**?<br>- Quais opções facilitam interação segura com a **Lixeira do Windows** (move, restore, purge)? |
| **4** | **Descompactação Otimizada de Arquivos Compactados** | - Quais bibliotecas Python permitem **descompactar arquivos enquanto processam** os dados simultaneamente (streaming/unpacking sob demanda), maximizando o desempenho?<br>- Quais são as opções mais modernas, eficientes e compatíveis com grandes volumes de dados? |

---

## Formato Esperado da Resposta

Para **cada** item do escopo, fornecer:

1. **Top 3–5 candidatos** (nome + link oficial).  
2. **Resumo comparativo** (prós, contras, métricas de adoção e benchmarks se disponíveis).  
3. **Recomendação final** (justificativa concisa).  
4. **Referências** (artigos, repositórios, posts de benchmark, etc.).

Após a análise detalhada, gerar também:

- Uma **tabela resumida final** em **Markdown**, contendo:
  - Nome da camada/tema
  - Biblioteca ou ferramenta recomendada
  - Breve justificativa da escolha

- No cabeçalho do documento, informar o **modelo exato da LLM** utilizado para gerar a pesquisa.

---

## Regras de Formatação

- A resposta deve ser escrita em **português**.
- A resposta deve ser formatada usando **Markdown**.

---

> **Observação:** manter o conteúdo técnico atualizado (últimos 6–12 meses) e citar fontes confiáveis.
