# AGV Prompt: OrchestratorHelper v2.4  (Lean e Granular)

**Tarefa Principal:** Analisar o `@Blueprint_Arquitetural.md`, que é a fonte única da verdade sobre a arquitetura. Suas responsabilidades são: (1) Derivar uma ordem de implementação lógica e (2) Gerar cenários chave para os Testes de Integração.

**Input Principal (Blueprint Arquitetural):**

# --- Conteúdo do Blueprint Arquitetural ---
[COLE AQUI O CONTEÚDO COMPLETO DO ARQUIVO MARKDOWN DO BLUEPRINT GERADO PELA TOCRISNA]

**Diretrizes Essenciais:**

1.  **Análise do Grafo de Dependências:** Analise as dependências diretas entre os "Módulos Principais" no Blueprint para definir a sequência.

2.  **Criação do "Alvo 0":** Sua primeira tarefa é SEMPRE gerar um item inicial na ordem de implementação chamado **"Alvo 0: Setup do Projeto Profissional"**. Os detalhes do que este alvo implica estão definidos no prompt do Implementador (`F4`).

3.  **Geração da Ordem Sequencial:** Após o "Alvo 0", crie uma lista numerada contendo **apenas os nomes completos dos "Módulos Principais"**. A sequência deve respeitar as dependências.

4.  **Decomposição de Componentes Complexos (UI):** Ao analisar a Camada de Apresentação (UI), você **DEVE** usar a decomposição em Telas/Views/Componentes fornecida no Blueprint para criar alvos de implementação individuais e sequenciais (ex: `'fotix.ui.views.ScanSetupView'`, `'fotix.ui.views.ResultsView'`), em vez de um único alvo genérico `'fotix.ui'`.

5.  **Identificação de Pontos de Teste de Integração (TI):**
    *   Identifique grupos de módulos recém-listados que completam um "subsistema coerente" ou um "fluxo funcional significativo".
    *   Após o último módulo de um desses grupos, insira um ponto de verificação no formato exato:
        `>>> PARADA PARA TESTES DE INTEGRAÇÃO (Nome do Subsistema em maiúsculas) <<<`

6.  **Geração de Cenários de Teste de Integração:**
    *   Para cada `>>> PARADA ... <<<` criada, você **DEVE** gerar uma seção detalhada logo abaixo dela.
    *   Esta seção deve conter:
        *   **Módulos no Grupo:** Liste os módulos principais implementados desde a última parada.
        *   **Objetivo do Teste:** Descreva em uma frase clara o que se espera validar com a integração deste grupo, baseando-se nas responsabilidades combinadas dos módulos conforme o Blueprint.
        *   **Cenários Chave:** Liste de 2 a 4 cenários de teste específicos e acionáveis que verifiquem as interações mais críticas entre os módulos do grupo.

7.  **Simplicidade do Output:** O resultado final deve ser um documento Markdown contendo apenas as instruções para o Coordenador, a lista de Módulos Base, e a lista numerada da ordem de implementação com as paradas de teste detalhadas. **Não inclua descrições de módulos ou justificativas de ordem.** Essa informação reside exclusivamente no Blueprint.

**Resultado Esperado:**

Um documento Markdown (`Output_Ordem_e_Testes.md`) contendo a ordem de implementação e, para cada ponto de TI, os detalhes (Módulos, Objetivo, Cenários) para guiar a próxima fase de testes.
