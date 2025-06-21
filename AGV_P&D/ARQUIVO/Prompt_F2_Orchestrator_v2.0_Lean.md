# AGV Prompt: OrchestratorHelper v2.0 (Lean) - Sequência de Implementação

**Tarefa Principal:** Analisar o `@Blueprint_Arquitetural.md` fornecido, que é a fonte única da verdade sobre a arquitetura do projeto. Sua única responsabilidade é derivar uma ordem de implementação lógica e identificar pontos de parada para testes de integração.

**Input Principal (Blueprint Arquitetural):**

```markdown
# --- Conteúdo do Blueprint Arquitetural ---
[COLE AQUI O CONTEÚDO COMPLETO DO ARQUIVO MARKDOWN DO BLUEPRINT GERADO PELA TOCRISNA]
```

**Diretrizes Essenciais:**

1.  **Análise do Grafo de Dependências:** Analise a seção "Descrição dos Componentes/Módulos" e a seção "Diagrama de Componentes" do Blueprint para entender as dependências diretas entre os "Módulos Principais".

2.  **Geração da Ordem Sequencial:** Crie uma lista numerada contendo **apenas os nomes completos dos "Módulos Principais"** a serem implementados. A sequência deve respeitar as dependências (um módulo só pode ser listado após todas as suas dependências já terem sido listadas).

3.  **Identificação de Pontos de Teste de Integração:**
    *   Durante a criação da sequência, identifique grupos de módulos recém-listados que completam um "subsistema coerente" ou uma "capacidade funcional significativa".
    *   **Aplique este princípio tanto para os subsistemas de backend quanto para os da camada de Apresentação (UI).** Para a UI, um subsistema pode ser um fluxo de usuário principal (ex: o fluxo de escaneamento, o fluxo de restauração).
    *   Após o último módulo de um desses grupos, insira um ponto de verificação no seguinte formato exato:
        `>>> PARADA PARA TESTES DE INTEGRAÇÃO (Nome do Subsistema em maiúsculas) <<<`

4.  **Simplicidade do Output:** O resultado final deve ser um documento Markdown contendo **apenas** as instruções para o Coordenador, a lista de Módulos Base para ciência, e a lista numerada da ordem de implementação com as paradas de teste intercaladas. **Não inclua descrições de módulos, justificativas de ordem ou listas de dependências no output final.** Essa informação reside exclusivamente no Blueprint.

**Resultado Esperado:**

Um documento Markdown (`Output_Ordem_Para_Implementacao_Geral.md`) com a seguinte estrutura:

1.  **Instruções para o Coordenador:** Um texto introdutório explicando como usar a lista, mencionando que os Módulos Base não estão na ordem numerada e que as informações detalhadas para cada implementação devem ser consultadas diretamente no Blueprint Arquitetural.
2.  **Módulos Base (Para Ciência do Coordenador):** Uma lista simples dos módulos considerados "base" (interfaces, modelos, utils, etc.) para que o Coordenador saiba que eles serão criados sob demanda.
3.  **Ordem de Implementação Sugerida (Módulos Principais e Pontos de Teste de Integração):** A lista numerada final, contendo apenas os nomes dos módulos e as paradas de teste.

**Exemplo de Texto para as "Instruções para o Coordenador" no Output:**

```markdown
**Instruções para o Coordenador:**

Este documento fornece a ordem de implementação sequencial e os pontos de verificação para testes de integração.

*   A seção "Módulos Base" lista componentes estruturais que serão criados sob demanda durante a implementação dos "Módulos Principais".
*   Siga a "Ordem de Implementação Sugerida" numerada abaixo. Para cada item, use o `Prompt_Implementador_Mestre` correspondente.
*   **Para obter os detalhes de CADA tarefa (responsabilidades, dependências, tecnologias), consulte SEMPRE e EXCLUSIVAMENTE o `@Blueprint_Arquitetural.md`, que é a nossa fonte única da verdade arquitetural.**
```