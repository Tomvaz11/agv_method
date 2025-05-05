# Método AGV: Fluxo de Trabalho v1.2

Este documento descreve o fluxo de trabalho passo a passo para desenvolver software usando o Método AGV (Assistência Generativa à Velocidade), versão 1.2

## Visão Geral do Fluxo (v1.2)

O fluxo incorpora novos agentes auxiliares e refinamentos para maior clareza e assistência.

```mermaid
graph LR
    A[Fase 1: Você - Definição (Incl. Test Fw)] --> B(Fase 2: Tocrisna - Arquitetura);
    B --> C{Validação Arquitetura?};
    C -- Aprova --> C1(Fase 2.1: Opc. OrchestratorHelper - Sugerir Ordem);
    C -- Rejeita/Ajusta --> B;
    C1 --> C2{Início Ciclo Módulo};
    subgraph "Ciclo por Módulo (Repetir para cada item da Ordem)"
        D[Fase 2.2: RequirementHelper - Elaborar Funcionalidade] --> E[Fase 2.5: Severino - Especificação (Sugere Utils)];
        E --> F{Validação Especificação?};
        F -- Aprova --> G[Fase 3: Tocle - Implementação (Módulo + Opc. Utils)];
        F -- Rejeita/Ajusta --> E;
        G --> H[Fase 4: Você - Revisão & Testes Unitários];
        H --> I{Integração OK?};
        I -- Sim --> J[Commit & Próximo Módulo];
        I -- Não/Ajuste --> K{Refatorar?};
        K -- Sim --> L[Tolete - Refatoração Cód.];
        K -- Não --> M[Tocle - Ajuste Teste/Impl.];
        L --> G;
        M --> G;
    end
    C2 --> D;
    J --> C2;


    subgraph "Preparação Inicial"
        A; B; C; C1;
    end
```

*Diagrama conceitual. A validação de preenchimento de prompt (ValidadorCruzado) é um passo opcional antes de executar Severino/Tocle se usar IA preenchedora.*

## Papéis dos Agentes (v1.2)

- **Você:** Idealizador, Definidor (Funcionalidades Alto Nível, Stack, **Framework de Testes**), Coordenador, Validador Crítico.
- **RequirementHelper (Auxiliar):** Ajuda a elaborar a "Descrição de Alto Nível" da funcionalidade via entrevista. Usa `Prompts/Templates/Prompt_F2.2_RequirementHelper_ElaborateFunctionality_v1.0.md`.
- **Tocrisna (Arquiteta):** Define arquitetura (componentes, interfaces, dependências). Usa `Prompts/Templates/Prompt_F2_Tocrisna_Architecture_v1.1b.md`.
- **Orche (Engenheiro):** Implementa código e testes unitários (módulo principal + opcionalmente `utils`). Atualiza/refatora testes. Usa `Prompts/Templates/Prompt_F3_Tocle_Implementation_v1.2b.md` e `Prompts/Templates/Prompt_Tocle_RefatorTest_v1.0.md`.
- **Tolete (Refatorador):** Melhora código de produção existente. Usa `Prompts/Templates/Prompt_Tolete_Refatoracao_v1.0.md`.
- **(Meta-Agentes/Opcionais):** `PreenchedorGenerico` (v1.1), `ValidadorCruzado` (v1.0).

## Fases Detalhadas (v1.2)

### Fase 1: Definição e Preparação (Você)

- **Objetivo:** Estabelecer visão, escopo, restrições e stack.
- **Inputs:** Ideia.
- **Atividades:**
    1.  Definir nome, objetivo.
    2.  Listar funcionalidades chave (alto nível).
    3.  Pesquisar e decidir Stack Tecnológica (linguagem, libs, BD, **FRAMEWORK DE TESTES** - ex: pytest).
    4.  Identificar requisitos não funcionais e restrições.
    5.  Organizar informações (ex: `Veredito.md`).
- **Output:** Documento de Visão e Definição Inicial.
- **Validação:** Auto-revisão.

### Fase 2: Arquitetura Técnica (Tocrisna)

- **Objetivo:** Criar o blueprint técnico.
- **Inputs:** Output da Fase 1.
- **Atividades:**
    1.  Preparar (manualmente ou com Preenchedor + Validador) `Prompts/Templates/Prompt_F2_Tocrisna_Architecture_v1.1b.md`.
    2.  Executar prompt.
    3.  Analisar criticamente o Blueprint gerado.
- **Output:** `Blueprint_Arquitetural.md` (contendo componentes, interfaces, dependências diretas, etc.).
- **Validação (Você): CRÍTICA.** Revisar completude e lógica. Iterar se necessário.

### Fase 2.1: (Opcional) Sugestão de Ordem (OrchestratorHelper)

- **Objetivo:** Obter uma sequência lógica para implementação.
- **Inputs:** `Blueprint_Arquitetural.md` validado.
- **Atividades:**
    1.  Preparar e executar `Prompts/Templates/Prompt_F2.1_OrchestratorHelper_SuggestOrder_v1.0.md`.
- **Output:** `Ordem_Implementacao_Sugerida.md`.
- **Validação (Você):** Revisar a ordem sugerida, ajustar se necessário.

**--- INÍCIO DO CICLO POR MÓDULO ---**

*(Repetir Fases 2.2 a 4 para cada módulo, seguindo a ordem definida)*

### Fase 2.2: Elaboração Funcional (RequirementHelper)

- **Objetivo:** Gerar a "Descrição de Alto Nível" para o módulo atual.
- **Inputs:** Nome/Responsabilidade do Módulo Atual (do Blueprint/Ordem).
- **Atividades:**
    1.  Executar `Prompts/Templates/Prompt_F2.2_RequirementHelper_ElaborateFunctionality_v1.0.md` em modo interativo com a LLM.
    2.  Responder às perguntas da IA para detalhar a funcionalidade.
    3.  Validar o texto final gerado pela IA.
- **Output:** Bloco de texto "Descrição de Alto Nível" para o módulo atual.
- **Validação (Você): CRÍTICA.** Garantir que o texto gerado captura sua intenção funcional.

### Fase 2.5: Especificação Funcional Detalhada (Severino)

- **Objetivo:** Detalhar tecnicamente a funcionalidade do módulo atual e sugerir `utils`.
- **Inputs:**
    - Descrição de Alto Nível (Output da Fase 2.2).
    - Blueprint Arquitetural Aprovado (Output da Fase 2).
    - Nome do Módulo Alvo.
- **Atividades:**
    1.  Preparar (manualmente ou com Preenchedor + Validador) `Prompts/Templates/Prompt_F2.5_Severino_EspeciFi_v1.2.md` usando os inputs.
    2.  Executar o prompt.
    3.  Analisar a Especificação Técnica e as Sugestões para `utils`.
    4.  **Decidir quais sugestões para `utils` aprovar (se houver).**
- **Output:**
    - `Especificacao_[Modulo].md` (Bloco de texto com detalhes técnicos).
    - Lista de funções `utils` aprovadas (para usar na Fase 3).
- **Validação (Você): IMPORTANTE.** Revisar especificação e sugestões. Iterar se necessário.

### Fase 3: Implementação e Teste Unitário (Tocle)

- **Objetivo:** Escrever código funcional e testes unitários.
- **Inputs:**
    - `Prompts/Templates/Prompt_F3_Tocle_Implementation_v1.2b.md` preenchido com:
        - Contexto Arquitetural relevante (do Blueprint).
        - Especificação Técnica (Output principal da Fase 2.5).
        - **Instrução Adicional para `utils`** (com as funções aprovadas, se houver).
        - Stack tecnológica e **Framework de Testes** (definido na Fase 1).
    - **Contexto para IA (@):** Blueprint, Especificação, **Arquivos das Dependências Diretas**, Arquivo de `utils` (se for modificar).
- **Atividades:**
    1.  Executar prompt com LLM/ferramenta (Cursor, etc.), fornecendo contexto via `@`.
    2.  Analisar código(s) e testes gerados.
- **Output:**
    - Arquivo `.py` do módulo principal.
    - Arquivo(s) `test_*.py` do módulo principal.
    - (Opcional) Arquivo `.py` de `utils` atualizado.
    - (Opcional) Arquivo(s) `test_*.py` de `utils`.
- **Validação (Você):** Ver Fase 4.

### Fase 4: Revisão, Integração e Testes (Você + IA)

- **Objetivo:** Garantir qualidade, funcionalidade isolada e integração correta.
- **Inputs:** Código de produção e testes gerados na Fase 3.
- **Atividades (Ciclo Iterativo):**
    1.  **Revisão de Código (Você):** Ler código(s) gerado(s). Clareza? Diretrizes? Lógica correta?
    2.  **Execução de Testes Unitários (Você/Ambiente):** Rodar testes do módulo principal e de `utils` (se houver). Passam? Testam o correto?
    3.  **Refatoração (Opcional - Tolete):** Se necessário, usar `Prompts/Templates/Prompt_Tolete_Refatoracao_v1.0.md` no código de produção. *Após refatorar, voltar ao Passo 2.*
    4.  **Ajuste de Testes (Opcional - Tocle):** Se necessário, usar `Prompts/Templates/Prompt_Tocle_RefatorTest_v1.0.md`. *Após ajustar, voltar ao Passo 2.*
    5.  **Teste de Integração (Você/Ambiente):** **CRUCIAL (Incremental):** Executar testes que verifiquem a interação com outros módulos já existentes.
    6.  **Commit (Você):** Versionar código funcional e testes no Git.
- **Output:** Código validado e integrado. Base de código atualizada.
- **Validação (Você):** Código faz o que deveria? Testes passam? Integração OK? **Só então seguir para o próximo módulo.**

**--- FIM DO CICLO POR MÓDULO ---**

### Fase 5: Ciclo de Vida (Manutenção e Evolução)

- Para **novas features:** Retornar à Fase 2.2 (RequirementHelper) ou 2.5 (Severino).
- Para **corrigir bugs:** Analisar, usar Tocle (implementação ou teste) ou Tolete para corrigir e garantir testes.
- Para **refatorar código existente:** Usar Tolete.
- Para **atualizar testes:** Usar Tocle com o prompt de teste.

## Princípios Chave e de Engenharia

> O Método AGV é guiado por princípios de engenharia de software que visam maximizar a qualidade, manutenibilidade e eficiência da colaboração humano-IA. Os detalhes desses princípios estão documentados em [`Guides/AGV_Method_Principios_Chave_v1.0.md`](./Guides/AGV_Method_Principios_Chave_v1.0.md). Os mais importantes incluem:

- **Integração Incremental via Interfaces Explícitas:** Define como os módulos são projetados para interagir de forma robusta e desacoplada (Ver detalhes no documento de princípios).
- **Validação Humana Contínua:** Ênfase na revisão e aprovação humana em etapas críticas (Arquitetura, Especificação, Código/Testes).
- **Foco na Qualidade:** Aplicação consistente de boas práticas (PEP 8, SRP, DRY, KISS, Type Hints, Docstrings, Testes).
- **Gerenciamento de Contexto da IA:** Uso de prompts focados e contexto mínimo necessário.
- **Iteração:** Reconhecimento de que o desenvolvimento é iterativo e ajustes nos prompts ou no código podem ser necessários.
- **Teste de Integração (Você/Ambiente):** **CRUCIAL (Incremental):** Executar testes que verifiquem:
    - A interação com outros módulos já existentes.
- **Commit (Você):** Versionar código funcional e testes no Git.