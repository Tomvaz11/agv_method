# AGV Prompt Template: ValidadorOrdemDescricao v1.0 - Validação do Output do OrchestratorHelper

**Tarefa Principal:** Validar a consistência e correção do arquivo "Ordem e Descrições Iniciais" (`[NOME_ARQUIVO_ORDEM_COM_DESCRICOES.md]`) em relação ao Blueprint Arquitetural (`[NOME_ARQUIVO_BLUEPRINT.md]`).

**Contexto:** O agente OrchestratorHelper gerou uma ordem de implementação sugerida e descrições iniciais para os módulos principais. Sua tarefa é verificar se essa saída está logicamente correta e consistente com a arquitetura definida no Blueprint.

**Arquivos para Análise:**

1.  **Ordem e Descrições Iniciais (a ser validado):**
    ```markdown
    # --- Conteúdo de [NOME_ARQUIVO_ORDEM_COM_DESCRICOES.md] ---
    [COLE AQUI O CONTEÚDO COMPLETO DO OUTPUT DO ORCHESTRATORHELPER V1.2]
    ```

2.  **Blueprint Arquitetural (Fonte da Verdade):**
    ```markdown
    # --- Conteúdo de [NOME_ARQUIVO_BLUEPRINT.md] ---
    [COLE AQUI O CONTEÚDO COMPLETO DO BLUEPRINT DA TOCRISNA (v1.1c+)]
    ```

**Instruções Detalhadas para Validação:**

1.  **Verificar Módulos Base:** Confirme se a lista de "Módulos Base" no arquivo de Ordem contém apenas módulos como `models`, `config`, `utils`, `*.interfaces`, etc., e não componentes com lógica de negócio principal ou fluxo de aplicação.
2.  **Validar Ordem Numerada vs. Dependências:** Para **cada** item na "Ordem de Implementação Sugerida (Módulos Principais)":
    *   Encontre a seção correspondente no Blueprint e verifique sua lista de "Dependências Diretas".
    *   Confirme se **todas as dependências diretas listadas** (que *também* são módulos principais) aparecem **antes** deste item na ordem numerada.
    *   Aponte qualquer violação de dependência encontrada.
3.  **Validar Descrição Inicial vs. Responsabilidade:** Para **cada** item na ordem numerada:
    *   Compare a "Descrição de Alto Nível Inicial" fornecida no arquivo de Ordem com a "Responsabilidade Principal" definida para aquele mesmo módulo no Blueprint.
    *   Verifique se a Descrição Inicial é **consistente** com a Responsabilidade e representa uma **expansão razoável e genérica** dela, sem introduzir requisitos específicos não mencionados ou contraditórios. Aponte inconsistências significativas.
4.  **Verificar Ciclos (Redundante, mas útil):** Embora o OrchestratorHelper deva detectar ciclos, verifique rapidamente se há alguma dependência circular óbvia na ordem proposta.

**Resultado Esperado:**

Um **Relatório de Validação Detalhado** em Markdown, contendo:

1.  **Resumo Geral:** Uma avaliação sucinta (ex: "Output do OrchestratorHelper parece consistente e correto", "Encontradas pequenas inconsistências na ordem/descrição", "Detectada violação de dependência").
2.  **Lista de Achados:**
    *   **Validação da Ordem:** Confirmação de que a ordem respeita as dependências OU lista detalhada das violações encontradas (ex: "Módulo X listado antes de sua dependência Y").
    *   **Validação das Descrições:** Confirmação de que as descrições são consistentes com as responsabilidades OU lista das descrições que parecem inconsistentes ou problemáticas, explicando o porquê.
    *   **Módulos Base:** Confirmação de que a lista parece correta.
3.  **Recomendação:** Indicar se o arquivo `Ordem_Com_Descricoes.md` está pronto para guiar a implementação ou se precisa de revisão/regeneração pelo OrchestratorHelper.