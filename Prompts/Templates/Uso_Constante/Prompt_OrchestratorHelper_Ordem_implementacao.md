# AGV Prompt Template: OrchestratorHelper v1.0 - Sugestão de Ordem de Implementação

## Tarefa Principal

Analisar o Blueprint Arquitetural fornecido e sugerir uma **ordem de implementação lógica e eficiente** para os principais componentes/módulos definidos, baseando-se nas suas dependências diretas.

## Contexto

O objetivo é fornecer ao coordenador humano uma sequência recomendada para implementar os módulos do projeto, seguindo uma abordagem preferencialmente bottom-up (implementando dependências antes dos módulos que dependem delas) para facilitar a integração incremental.

## Input Principal (Blueprint Arquitetural)

### --- Conteúdo do Blueprint Arquitetural (Output da Tocrisna v1.1b+) ---

[COLE AQUI O CONTEÚDO COMPLETO DO ARQUIVO MARKDOWN DO BLUEPRINT GERADO PELA TOCRISNA, GARANTINDO QUE ELE CONTENHA A SEÇÃO "Dependências Diretas" PARA CADA COMPONENTE]

### Diretrizes para Geração da Ordem

1.  **Identificar Componentes e Dependências:** Parsear o blueprint para extrair a lista de todos os componentes/módulos principais definidos e suas respectivas listas de "Dependências Diretas".
2.  **Analisar o Grafo de Dependências:** Construir mentalmente (ou explicitamente, se for mais fácil) o grafo de dependências com base nas informações extraídas.
3.  **Gerar Ordem Lógica (Topological Sort):** Produzir uma sequência linear (ordem numérica) dos componentes que respeite as dependências. Ou seja, um componente só deve aparecer na lista após todos os seus dependentes diretos já terem aparecido.
4.  **Prioridade:** Começar com componentes que não têm nenhuma dependência ou cujas dependências são apenas externas/da biblioteca padrão/do domínio base (ex: `fotix.domain.models`).
5.  **Justificativa:** Para cada componente na ordem sugerida, fornecer uma breve justificativa para sua posição (ex: "Sem dependências internas", "Depende apenas de X e Y que já estão antes na lista").
6.  **Identificar Possíveis Ciclos:** Se uma dependência circular é detectada (A depende de B e B depende de A), a geração de uma ordem linear válida é impossível. Neste caso, o output deve identificar e relatar claramente o ciclo de dependência encontrado em vez de fornecer uma ordem inválida.
7.  **Clareza:** Apresentar a ordem de forma clara e fácil de seguir.

### Resultado Esperado

Uma Lista Ordenada de Implementação em Markdown, contendo:

- Uma lista numerada dos componentes/módulos na ordem sugerida.
- Para cada item da lista:
    - O nome completo do componente/módulo (ex: `fotix.core.lógica_de_decisão`).
    - Uma breve justificativa para sua posição na sequência, mencionando suas dependências chave já resolvidas.

OU, se um ciclo for detectado:

- Uma mensagem clara indicando que um ciclo de dependência foi encontrado.
- A identificação dos componentes envolvidos no ciclo.
- Uma nota de que a arquitetura (blueprint) precisa ser revisada para resolver o ciclo antes de prosseguir.

#### Exemplo de Saída Esperada (Sem Ciclos)

## Ordem de Implementação Sugerida

1.  **`fotix.domain.models`**
    - *Justificativa:* Define as estruturas de dados base, sem dependências internas do projeto.
2.  **`fotix.utils.helpers`** (se existir)
    - *Justificativa:* Funções utilitárias genéricas, provavelmente sem dependências internas complexas.
3.  **`fotix.core.decision_logic`**
    - *Justificativa:* Depende apenas de `fotix.domain.models`.
4.  **`fotix.infrastructure.FileSystemService`**
    - *Justificativa:* Implementa acesso ao sistema de arquivos, pode depender de `fotix.domain.models` ou `fotix.utils`, mas não do core principal ainda.
5.  **`fotix.infrastructure.hasher_impl`**
    - *Justificativa:* Depende de `fotix.domain.models` e talvez `fotix.infrastructure.FileSystemService`.
6.  **`fotix.core.duplicate_finder`**
    - *Justificativa:* Depende de `fotix.domain.models` e da interface do `hasher_impl` (a ser fornecida pela infraestrutura).
7.  **`fotix.application.ScanService`**
    - *Justificativa:* Orquestrador principal, depende de vários componentes do core e da infraestrutura (`duplicate_finder`, `decision_logic`, `FileSystemService`, etc.).
8.  **`fotix.gui.MainWindow`**
    - *Justificativa:* Camada de apresentação, depende da camada de aplicação (`ScanService`).

... (Continuar para todos os componentes principais)

#### Exemplo de Saída Esperada (Com Ciclo)

## Erro: Ciclo de Dependência Detectado!

Não foi possível gerar uma ordem de implementação linear válida devido a um ciclo de dependência envolvendo os seguintes componentes:

- `fotix.moduleA` (Declara dependência de `fotix.moduleB`)
- `fotix.moduleB` (Declara dependência de `fotix.moduleA`)

**Ação Necessária:** Revise o Blueprint Arquitetural e refatore a arquitetura para remover a dependência circular antes de tentar gerar a ordem de implementação novamente.

Pronto! Com este prompt, você pode, após validar o blueprint da Tocrisna, pedir a uma LLM para analisar esse blueprint e te dar uma sugestão clara de por onde começar e como continuar a implementação dos módulos do seu projeto.