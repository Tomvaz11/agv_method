# AGV Prompt Template: OrchestratorHelper v1.4 - Sugestão de Ordem e Descrição Inicial com Instruções

**Tarefa Principal:** Analisar o Blueprint Arquitetural fornecido, sugerir uma ordem de implementação lógica para os componentes/módulos **principais**, gerar uma Descrição de Alto Nível Inicial para cada um, e apresentar o resultado com **instruções claras para o Coordenador** sobre como proceder.

**Contexto:** O objetivo é fornecer ao Coordenador uma sequência recomendada e descrições iniciais, além de orientação explícita sobre quais módulos implementar e como lidar com os módulos base.

**Input Principal (Blueprint Arquitetural):**

```markdown
# --- Conteúdo do Blueprint Arquitetural ---
[COLE AQUI O CONTEÚDO COMPLETO DO ARQUIVO MARKDOWN DO BLUEPRINT GERADO PELA TOCRISNA (v1.1d+). A IA deve extrair as informações necessárias a partir deste conteúdo.]
```

**Diretrizes para Geração:**

1.  **Identificar Componentes e Dependências:** Parsear o blueprint para extrair componentes, dependências e responsabilidades.
2.  **Separar Módulos Base:** Identifique módulos puramente utilitários, de configuração, modelos ou interfaces (`utils`, `config`, `domain.models`, `*.interfaces`).
3.  **Analisar Grafo (Módulos Principais):** Foque nas dependências entre os módulos Core (lógica), Infrastructure (implementações), Application e UI.
4.  **Gerar Ordem Lógica (Módulos Principais):** Produza uma sequência numerada **APENAS para os módulos principais** que respeite as dependências.
5.  **Gerar Descrição Inicial (Para cada item na Ordem Principal):** Baseie-se na responsabilidade encontrada no blueprint (pode ser genérica se a responsabilidade for vaga).
6.  **Justificativa da Ordem:** Forneça breve justificativa para a posição de cada item na ordem principal.
7.  **Listar Módulos Base Separadamente:** Liste os Módulos Base com suas responsabilidades.
8.  **Formatar Output com Instruções Claras:** **CRUCIAL:** Estruture o output final para incluir um texto introdutório explicando ao Coordenador como usar a informação gerada (conforme detalhado no Resultado Esperado).
9.  **Identificar Ciclos:** Se um ciclo *entre os módulos principais* for detectado, relate-o claramente em vez da ordem.

**Resultado Esperado:**

Um documento Markdown contendo:

1.  **Instruções para o Coordenador (Texto Introdutório - IMPORTANTE):** Um parágrafo claro no início do output explicando:
    *   Que o output separa "Módulos Base" de "Módulos Principais".
    *   Que os **Módulos Base listados abaixo NÃO devem ser implementados diretamente** usando o `ImplementadorMestre` nesta fase inicial (sua estrutura será criada conforme necessário e o conteúdo de `utils` adicionado organicamente).
    *   Que a implementação deve **SEGUIR a "Ordem de Implementação Sugerida (Módulos Principais)"**, começando pelo **Item #1** da lista numerada.
    *   Que para cada item numerado, o Coordenador deve usar o `Prompt_ImplementadorMestre` junto com o `@Blueprint` e este output (`@Ordem...`), preenchendo apenas o nome do módulo alvo.

2.  **Módulos Base:** Lista dos módulos base com suas responsabilidades (conforme encontradas no blueprint).

3.  **Ordem de Implementação Sugerida (Módulos Principais):** Lista **numerada** dos módulos principais.
4.  Para cada item da lista numerada:
    *   O nome completo do componente/módulo.
    *   **Descrição de Alto Nível Inicial:** (2-4 frases).
    *   *Justificativa da Ordem:* (Breve explicação).
5.  **OU**, se um ciclo for detectado:
    *   Mensagem de erro clara identificando o ciclo.

**Exemplo de Texto Introdutório (Instruções no Output):**

```markdown
## Análise de Implementação e Próximos Passos para Fotix

**Instruções para o Coordenador:**

Este documento organiza os módulos do projeto Fotix para guiar a implementação. Ele separa os "Módulos Base" (definições e utilitários) dos "Módulos Principais" (com a lógica central).

*   **NÃO implemente os "Módulos Base" listados abaixo diretamente agora.** Suas pastas e arquivos básicos serão criados quando necessário pela IA durante a implementação dos módulos principais. O conteúdo específico de `fotix.utils` será adicionado conforme a necessidade surgir.
*   **SIGA a "Ordem de Implementação Sugerida (Módulos Principais)" abaixo.** Comece pelo **Item #1** e prossiga sequencialmente.
*   Para **CADA item** da ordem numerada, use o `Prompt_ImplementadorMestre_v1.2`, preenchendo apenas o nome do módulo alvo (ex: "Item 1: fotix.infrastructure.logging_config"). Anexe sempre o `@Blueprint_Arquitetural.md`, este arquivo (`@Ordem_Com_Descricoes.md`) e o código relevante já existente como contexto. A "Descrição de Alto Nível Inicial" listada abaixo para cada item servirá como ponto de partida para a IA.

---

### Módulos Base (Estrutura Inicial / Conteúdo On-Demand)

*   `fotix.domain.models`: Define estruturas de dados fundamentais.
*   ... (etc.)

---

### Ordem de Implementação Sugerida (Módulos Principais) - COMECE AQUI (Item #1)

1.  **`fotix.infrastructure.logging_config`**
    *   **Descrição Inicial:** ...
    *   *Justificativa da Ordem:* ...
2.  **`fotix.infrastructure.file_system`**
    *   **Descrição Inicial:** ...
    *   *Justificativa da Ordem:* ...
... (etc.)
```