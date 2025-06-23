# AGV Prompt: OrchestratorHelper v2.3 (Lean com Cenários de TI)

**Tarefa Principal:** Analisar o `@Blueprint_Arquitetural.md`, que é a fonte única da verdade sobre a arquitetura. Suas responsabilidades são: (1) Gerar o "Alvo 0" para setup do projeto, (2) Derivar uma ordem de implementação lógica para os demais módulos, e (3) Gerar cenários chave para os Testes de Integração.

**Input Principal (Blueprint Arquitetural):**

# --- Conteúdo do Blueprint Arquitetural ---
[COLE AQUI O CONTEÚDO COMPLETO DO ARQUIVO MARKDOWN DO BLUEPRINT GERADO PELA TOCRISNA]


**Diretrizes Essenciais:**

1.  **Análise do Grafo de Dependências:** Analise as dependências diretas entre os "Módulos Principais" no Blueprint para definir a sequência.

2.  **Criação do "Alvo 0 - Setup do Projeto Profissional":** Sua primeira tarefa é SEMPRE gerar um item inicial na ordem de implementação chamado **"Alvo 0: Setup do Projeto Profissional"**. A responsabilidade deste alvo é criar o andaime ("scaffolding") completo, incluindo:
    *   A estrutura de diretórios base (`src/nome_do_projeto`, `tests/unit`, `tests/integration`).
    *   Os arquivos `__init__.py` necessários.
    *   O arquivo `pyproject.toml` configurando dependências, `pytest`, e as ferramentas de qualidade **`ruff`** (linter) e **`black`** (formatador).
    *   O arquivo de configuração do `pre-commit` (`.pre-commit-config.yaml`) para automatizar a execução de `ruff` e `black`.
    *   Instruções claras para o Coordenador sobre como instalar as dependências (`pip install -e .[dev]`) e inicializar o `pre-commit` (`pre-commit install`).

3.  **Geração da Ordem Sequencial:** Após o "Alvo 0", crie uma lista numerada contendo **apenas os nomes completos dos "Módulos Principais"**. A sequência deve respeitar as dependências.

4.  **Identificação de Pontos de Teste de Integração (TI):**
    *   Identifique grupos de módulos recém-listados que completam um "subsistema coerente" ou um "fluxo funcional significativo".
    *   Após o último módulo de um desses grupos, insira um ponto de verificação no formato exato:
        `>>> PARADA PARA TESTES DE INTEGRAÇÃO (Nome do Subsistema em maiúsculas) <<<`

5.  **Geração de Cenários de Teste de Integração:**
    *   Para cada `>>> PARADA ... <<<` criada, você **DEVE** gerar uma seção detalhada logo abaixo dela.
    *   Esta seção deve conter:
        *   **Módulos no Grupo:** Liste os módulos principais implementados desde a última parada.
        *   **Objetivo do Teste:** Descreva em uma frase clara o que se espera validar com a integração deste grupo, baseando-se nas responsabilidades combinadas dos módulos conforme o Blueprint.
        *   **Cenários Chave:** Liste de 2 a 4 cenários de teste específicos e acionáveis que verifiquem as interações mais críticas entre os módulos do grupo.

6.  **Simplicidade do Output:** O resultado final deve ser um documento Markdown contendo apenas as instruções para o Coordenador, a lista de Módulos Base, e a lista numerada da ordem de implementação com as paradas de teste detalhadas. **Não inclua descrições de módulos ou justificativas de ordem.** Essa informação reside exclusivamente no Blueprint.

**Resultado Esperado:**

Um documento Markdown (`Output_Ordem_e_Testes.md`) contendo a ordem de implementação e, para cada ponto de TI, os detalhes (Módulos, Objetivo, Cenários) para guiar a próxima fase de testes.