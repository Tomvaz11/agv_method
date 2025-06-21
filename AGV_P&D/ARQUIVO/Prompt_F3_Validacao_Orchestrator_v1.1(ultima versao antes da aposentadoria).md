# AGV Prompt Template: ValidadorOrdemDescricao v1.1 - Validação do Output do OrchestratorHelper (com Testes de Integração)

**Tarefa Principal:** Validar a consistência, correção e lógica do arquivo de "Ordem de Implementação, Descrições e Pontos de Teste de Integração" (`[NOME_ARQUIVO_ORDEM_COMPLETO.md]`) em relação ao Blueprint Arquitetural (`[NOME_ARQUIVO_BLUEPRINT.md]`).

**Contexto:** O agente `OrchestratorHelper` (v1.5+) gerou uma ordem de implementação sugerida para os módulos principais, descrições iniciais, e também identificou "Pontos de Verificação para Testes de Integração" com objetivos e cenários. Sua tarefa é verificar se essa saída está logicamente correta, consistente com a arquitetura definida no Blueprint, e se as sugestões de teste de integração são pertinentes.

**Arquivos para Análise:**

1.  **Ordem, Descrições e Pontos de Teste (a ser validado):**
    ```markdown
    # --- Conteúdo de [NOME_ARQUIVO_ORDEM_COMPLETO.md] ---
    [COLE AQUI O CONTEÚDO COMPLETO DO OUTPUT DO ORCHESTRATORHELPER V1.5+ (QUE INCLUI AS "PARADAS PARA TESTES DE INTEGRAÇÃO")]
    ```

2.  **Blueprint Arquitetural (Fonte da Verdade):**
    ```markdown
    # --- Conteúdo de [NOME_ARQUIVO_BLUEPRINT.md] ---
    [COLE AQUI O CONTEÚDO COMPLETO DO BLUEPRINT DA TOCRISNA (v1.1d+)]
    ```

**Instruções Detalhadas para Validação:**

1.  **Verificar Módulos Base:**
    *   Confirme se a lista de "Módulos Base" no arquivo de Ordem contém apenas módulos como modelos de dados, configuração, utilitários, definições de interfaces, etc., e não componentes com lógica de negócio principal ou fluxo de aplicação.

2.  **Validar Ordem Numerada dos Módulos Principais vs. Dependências:**
    *   Para **cada** item de Módulo Principal na "Ordem de Implementação Sugerida":
        *   Encontre a seção correspondente no Blueprint e verifique sua lista de "Dependências Diretas".
        *   Confirme se **todas as dependências diretas listadas** (que *também* são módulos principais e não apenas módulos base como interfaces) aparecem **antes** deste item na ordem numerada.
        *   Aponte qualquer violação de dependência encontrada (ex: "Módulo X listado antes de sua dependência principal Y").

3.  **Validar Descrição Inicial vs. Responsabilidade do Módulo:**
    *   Para **cada** item de Módulo Principal na ordem numerada:
        *   Compare a "Descrição de Alto Nível Inicial" fornecida no arquivo de Ordem com la "Responsabilidade Principal" definida para aquele mesmo módulo no Blueprint.
        *   Verifique se a Descrição Inicial é **consistente** com a Responsabilidade e representa uma expansão razoável e genérica dela, sem introduzir requisitos específicos não mencionados ou contraditórios. Aponte inconsistências significativas.

4.  **Validar Pontos de Verificação para Testes de Integração:**
    *   Para cada seção **">>> PARADA PARA TESTES DE INTEGRAÇÃO (Nome do Subsistema) <<<"**:
        *   **Coerência do Ponto de Parada:** Avalie se a parada para testes de integração está logicamente posicionada após a implementação de um conjunto de módulos que formam um subsistema funcional ou uma capacidade coesa.
        *   **Módulos no Grupo:** Verifique se a lista de "Módulos Implementados neste Grupo" corresponde corretamente aos módulos principais que foram listados na ordem desde a última parada de teste (ou desde o início, para a primeira parada).
        *   **Objetivo do Teste:** Avalie se o "Objetivo do Teste de Integração" é claro, relevante para os módulos do grupo e alinhado com suas funcionalidades combinadas conforme o Blueprint.
        *   **Cenários Chave:** Revise os "Cenários Chave para Teste de Integração" sugeridos. Verifique se:
            *   São pertinentes aos módulos do grupo e ao objetivo do teste.
            *   Testam interações significativas entre os módulos.
            *   São descritos de forma clara e compreensível.
            *   Parecem razoáveis e testáveis (mesmo que os detalhes da implementação do teste venham depois).
        *   Aponte quaisquer problemas ou sugestões de melhoria para os pontos de teste de integração (ex: "Ponto de parada X parece prematuro", "Cenário Y não testa a interação principal entre Módulo A e B", "Objetivo do teste Z é vago").

5.  **Verificar Ciclos (Verificação Adicional):**
    *   Embora o `OrchestratorHelper` deva detectar ciclos entre módulos principais, verifique rapidamente se há alguma dependência circular óbvia que possa ter passado despercebida na ordem proposta.

**Resultado Esperado:**

Um **Relatório de Validação Detalhado** em Markdown, contendo:

1.  **Resumo Geral da Validação:**
    *   Uma avaliação sucinta (ex: "Output do OrchestratorHelper (v1.5+) parece consistente, correto e as sugestões de teste de integração são pertinentes", "Encontradas pequenas inconsistências na ordem/descrição, mas os pontos de teste são bons", "Detectada violação de dependência e sugestões de melhoria para os cenários de teste de integração").

2.  **Lista Detalhada de Achados:**
    *   **Validação da Ordem dos Módulos Principais:** Confirmação de que a ordem respeita as dependências OU lista detalhada das violações encontradas.
    *   **Validação das Descrições dos Módulos:** Confirmação de que as descrições são consistentes com as responsabilidades OU lista das descrições que parecem inconsistentes ou problemáticas, explicando o porquê.
    *   **Validação dos Módulos Base:** Confirmação de que a lista parece correta.
    *   **Validação dos Pontos de Teste de Integração:**
        *   Feedback sobre a coerência dos pontos de parada.
        *   Feedback sobre a correção da lista de módulos em cada grupo de teste.
        *   Feedback sobre a clareza e relevância dos objetivos e cenários de teste de integração sugeridos.
        *   Liste quaisquer sugestões de cenários adicionais ou modificações nos cenários existentes que você considere importantes.
    *   **Ciclos:** Confirmação de ausência de ciclos óbvios ou identificação de possíveis ciclos.

3.  **Recomendação Final:**
    *   Indicar se o arquivo de Ordem (`Ordem_Com_Descricoes_e_Testes_Integracao.md`) está **aprovado** para guiar a implementação e os testes de integração, ou se ele **requer revisão/regeneração** pelo `OrchestratorHelper` com base nos achados.