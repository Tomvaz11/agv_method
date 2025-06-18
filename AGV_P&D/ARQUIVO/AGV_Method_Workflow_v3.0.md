# Método AGV: Fluxo de Trabalho v3.0 (Pós-Fotix)

Este documento descreve o fluxo de trabalho passo a passo para desenvolver software usando o Método AGV (Assistência Generativa à Velocidade), versão 3.0, consolidada após a conclusão bem-sucedida do projeto piloto Fotix.

## Visão Geral do Fluxo (v3.0)

O fluxo v3.0 refina e simplifica as interações, focando nos agentes e prompts que se mostraram mais eficazes, e integrando aprendizados cruciais como a estratégia de documentação na codebase.

```mermaid
graph LR
    A[Fase 1: Coordenador - Definição Inicial] --> B(Fase 2: Tocrisna - Arquitetura Técnica);
    B -- Blueprint Arquitetural --> C{Validação Humana?};
    C -- Aprova --> D[Fase 2.1: OrchestratorHelper - Ordem de Implementação & Pontos de TI];
    C -- Rejeita/Ajusta --> B;
    D -- Ordem de Implementação --> E{Validação Humana? (Opcional)};
    E -- Aprova --> F(Início do Ciclo de Implementação);
    E -- Rejeita/Ajusta --> D;

    subgraph "Ciclo por Módulo/Ponto de TI (Repetir conforme a Ordem)"
        direction LR
        F1[Coordenador: Seleciona Próximo Item da Ordem] --> G{Tipo de Item?};
        G -- Módulo Principal --> H[Fase 3.1: ImplementadorMestre - Implementa Módulo + TUs];
        H -- Código + TUs + Relatório --> I{Validação Humana?};
        I -- Aprova --> J[Commit & Próximo];
        I -- Rejeita/Ajusta --> H;
        G -- Ponto de Teste de Integração --> K[Fase 3.2: IntegradorTester - Gera Testes de Integração];
        K -- Código de TIs + Relatório --> L{Validação Humana?};
        L -- Aprova --> J;
        L -- Rejeita/Ajusta --> K;
    end
    F --> F1;
    J --> F1;

    subgraph "Preparação e Planejamento"
        A; B; C; D; E;
    end
```

## Papéis dos Agentes (v3.0)

-   **Coordenador (Humano):** Idealizador, Definidor (Funcionalidades Alto Nível, Stack, Framework de Testes), Revisor Crítico, Tomador de Decisões Finais, e **Fornecedor de Documentação Curada** para bibliotecas específicas.
-   **Tocrisna (IA - Arquiteta):** Define a arquitetura técnica, componentes, interfaces e dependências diretas.
    *   **Prompt Associado:** `Prompt_F1_Tocrisna_Architecture_v1.1d` (ou versão mais recente).
-   **OrchestratorHelper (IA - Planejadora):** Analisa o blueprint da Tocrisna e sugere uma ordem lógica de implementação para os módulos principais, incluindo descrições iniciais e identificação de pontos estratégicos para Testes de Integração (TIs) com cenários.
    *   **Prompt Associado:** `Prompt_F2_Orchestrator_v1.5` (ou versão mais recente).
-   **ImplementadorMestre (IA - Engenheira de Implementação e Testes Unitários):** Implementa o módulo alvo e seus Testes Unitários (TUs) obrigatórios, seguindo o escopo definido, aderindo à stack e utilizando a documentação fornecida na codebase para bibliotecas específicas.
    *   **Prompt Associado:** `Prompt_Implementador_Mestre_v2.7` (ou versão mais recente, contendo a Diretriz 4 evoluída).
-   **IntegradorTester (IA - Engenheira de Testes de Integração):** Gera os Testes de Integração (TIs) para um grupo de módulos recém-concluído, com base nos cenários sugeridos pelo `OrchestratorHelper`.
    *   **Prompt Associado:** `Prompt_IntegradorTester_v1.0` (ou `Prompt_F4.1_Implementador_TesteDeIntegracao_v1.0`, ou versão mais recente).
-   **(Opcional) ValidadorOrdemDescricao (IA - Validadora):** Revisa a saída do `OrchestratorHelper` para consistência com o blueprint.
    *   **Prompt Associado:** `Prompt_F3_Validacao_Orchestrator_v1.1` (ou versão mais recente).

## Fases Detalhadas (v3.0)

### Fase 1: Definição Inicial (Coordenador)

-   **Objetivo:** Estabelecer visão, escopo, restrições e stack tecnológica.
-   **Atividades:**
    1.  Definir nome, objetivo principal do projeto.
    2.  Listar funcionalidades chave em alto nível.
    3.  Pesquisar e decidir a Stack Tecnológica completa (linguagem, frameworks, bibliotecas principais, BD, **Framework de Testes** - ex: pytest).
    4.  Identificar requisitos não funcionais e restrições.
    5.  Preparar documentação inicial (ex: Veredito, resumo da visão).
-   **Output:** Documento de Visão e Definição Inicial.
-   **Validação:** Auto-revisão pelo Coordenador.

### Fase 2: Arquitetura Técnica (Tocrisna)

-   **Objetivo:** Criar o blueprint técnico detalhado do sistema.
-   **Inputs:** Output da Fase 1.
-   **Atividades:**
    1.  Coordenador prepara o `Prompt_F1_Tocrisna_Architecture_vX.Y` com as informações da Fase 1.
    2.  Executar prompt com a IA (Tocrisna).
    3.  Coordenador analisa criticamente o Blueprint Arquitetural (`Output_BluePrint_Arquitetural_Tocrisna_vZ.md`) gerado.
-   **Output:** `Output_BluePrint_Arquitetural_Tocrisna_vZ.md` (contendo componentes, suas responsabilidades, interfaces explícitas, dependências diretas, estrutura de diretórios).
-   **Validação (Coordenador): CRÍTICA.** Revisar completude, lógica, aderência aos princípios AGV. Iterar com Tocrisna se necessário.

### Fase 2.1: Ordem de Implementação e Planejamento de Testes de Integração (OrchestratorHelper)

-   **Objetivo:** Gerar uma ordem de implementação lógica para os módulos principais e identificar pontos para Testes de Integração (TIs) com cenários.
-   **Inputs:** Blueprint Arquitetural validado.
-   **Atividades:**
    1.  Coordenador prepara o `Prompt_F2_Orchestrator_vX.Y` com o Blueprint.
    2.  Executar prompt com a IA (OrchestratorHelper).
    3.  Coordenador analisa o output (`Output_Ordem_Para_Implementacao_Geral.md`).
    4.  **(Opcional)** Coordenador pode usar o `Prompt_F3_Validacao_Orchestrator_vX.Y` para uma validação assistida por IA da ordem e dos pontos de TI.
-   **Output:** `Output_Ordem_Para_Implementacao_Geral.md` (contendo a lista de módulos base, a ordem numerada de módulos principais, descrições iniciais, e "PARADAS PARA TESTES DE INTEGRAÇÃO" com objetivos e cenários).
-   **Validação (Coordenador): IMPORTANTE.** Revisar a ordem, as descrições, a pertinência e clareza dos pontos de TI e cenários. Ajustar manualmente se necessário.

**--- INÍCIO DO CICLO DE IMPLEMENTAÇÃO (Iterativo) ---**

*(O Coordenador segue a `Output_Ordem_Para_Implementacao_Geral.md` sequencialmente)*

### Fase 3.1: Implementação de Módulo Principal e Testes Unitários (ImplementadorMestre)

-   **Objetivo:** Implementar o módulo principal alvo e seus Testes Unitários (TUs) com alta cobertura.
-   **Pré-requisito:** Se o módulo depende de uma biblioteca específica/complexa, o Coordenador deve garantir que a documentação relevante (ou exemplos de uso) esteja disponível na codebase/contexto a ser fornecido à IA.
-   **Inputs (para o `Prompt_Implementador_Mestre_v2.7`):**
    *   Nome completo do Módulo Principal alvo (extraído da Ordem de Implementação).
    *   `@Blueprint_Arquitetural.md`.
    *   `@Output_Ordem_Para_Implementacao_Geral.md` (para contexto da descrição inicial).
    *   `@Contexto Adicional do Workspace`: Código de dependências diretas já implementadas, módulos base relevantes (`models.py`, `interfaces.py` da camada, etc.), e **documentação/exemplos da biblioteca específica, se aplicável**.
-   **Atividades:**
    1.  Coordenador prepara e executa o `Prompt_Implementador_Mestre_v2.7` com a IA.
    2.  A IA implementa o módulo, cria/modifica módulos base estritamente necessários (interfaces, modelos de dados), e gera Testes Unitários com estrutura espelhada (`tests/unit/...`).
    3.  A IA segue a **Diretriz 4 evoluída**: consulta a documentação fornecida na codebase para bibliotecas da stack; se insuficiente ou ausente, PARA e SOLICITA ao Coordenador.
    4.  A IA gera um relatório detalhado.
-   **Output:**
    *   Arquivo(s) `.py` do módulo principal implementado.
    *   Arquivo(s) `test_*.py` dos Testes Unitários.
    *   Módulos base (`interfaces.py`, `models.py`, etc.) criados/atualizados, se necessário.
    *   `README.md` do pacote/módulo (se aplicável).
    *   Relatório da IA.
-   **Validação (Coordenador): CRÍTICA.**
    1.  Revisar o relatório da IA.
    2.  Analisar o código de produção (aderência ao blueprint, qualidade, boas práticas).
    3.  Analisar os Testes Unitários (cobertura, relevância, clareza).
    4.  Executar os TUs e verificar a cobertura real.
    5.  Iterar com o `ImplementadorMestre` se ajustes forem necessários no código ou nos TUs.

### Fase 3.2: Geração de Testes de Integração (IntegradorTester)

-   **Objetivo:** Gerar Testes de Integração (TIs) para o grupo de módulos recém-concluído, conforme indicado na `Output_Ordem_Para_Implementacao_Geral.md`.
-   **Inputs (para o `Prompt_IntegradorTester_v1.0`):**
    *   Lista dos módulos alvo da integração (do grupo atual, conforme a Ordem).
    *   `@Blueprint_Arquitetural.md`.
    *   `@Output_Ordem_Para_Implementacao_Geral.md` (para extrair o objetivo e cenários de TI relevantes).
    *   `@Contexto Adicional do Workspace`: Código dos módulos alvo implementados e outros módulos relevantes para stubs/fakes de dependências externas ao grupo.
-   **Atividades:**
    1.  Coordenador prepara e executa o `Prompt_IntegradorTester_v1.0` com a IA.
    2.  A IA analisa os módulos, o blueprint e os cenários para gerar os TIs.
    3.  A IA gera um relatório detalhado.
-   **Output:**
    *   Arquivo(s) `test_*.py` dos Testes de Integração (em `tests/integration/...`).
    *   Fixtures `pytest` necessárias.
    *   Relatório da IA.
-   **Validação (Coordenador): CRÍTICA.**
    1.  Revisar o relatório da IA.
    2.  Analisar o código dos TIs (aderência aos cenários, clareza, uso de mocks/stubs/fakes para dependências externas ao grupo).
    3.  Executar os TIs.
    4.  Depurar e iterar com o `IntegradorTester` (ou ajustar manualmente) se os TIs falharem ou não cobrirem adequadamente os cenários.

### Fase 3.3: Commit e Próximo Item

-   Após a validação bem-sucedida do módulo principal e seus TUs, ou dos TIs, o Coordenador versiona o código.
-   Coordenador seleciona o próximo item da `Output_Ordem_Para_Implementacao_Geral.md` e retorna a F1 do ciclo.

**--- FIM DO CICLO DE IMPLEMENTAÇÃO ---**

### Fase 4: Revisão Final e Conclusão do Projeto

-   **Objetivo:** Realizar uma revisão holística do projeto concluído.
-   **Atividades:**
    1.  Coordenador revisa a cobertura geral de testes.
    2.  Executa todos os testes (unitários e de integração) para garantir que o sistema está estável.
    3.  Considera testes manuais para fluxos de UI (se aplicável).
    4.  Prepara a documentação final do projeto.
-   **Output:** Software concluído e validado, documentação do projeto.

### Fase 5: Ciclo de Vida (Manutenção e Evolução)

-   Para **novas features:** Retornar à Fase 2 (Tocrisna) se a arquitetura for impactada, ou diretamente à Fase 2.1/Ciclo de Implementação.
-   Para **corrigir bugs:** Usar `ImplementadorMestre` para corrigir o código e/ou os testes.
-   Para **refatorar:** Usar prompts específicos de refatoração (não detalhados neste fluxo principal, mas podem ser derivados do `ImplementadorMestre`).