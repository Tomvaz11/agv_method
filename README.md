# Método AGV - Desenvolvimento de Software de Alta Qualidade com IA

![Status](https://img.shields.io/badge/Status-Validado%20e%20em%20Evolução%20(Pós--Fotix)-blue)
![Versão do Método](https://img.shields.io/badge/Método-v3.0-brightgreen)

## 1. Introdução

Bem-vindo ao repositório do **Método AGV**. Este projeto documenta e gerencia uma metodologia estruturada e iterativa para desenvolver software de **alta qualidade, escalável e manutenível** através da colaboração estratégica entre um coordenador humano e Modelos de Linguagem Grandes (LLMs) atuando como assistentes especializados ("Agentes").

O objetivo principal é alavancar o poder das IAs generativas para acelerar o desenvolvimento, mantendo um foco rigoroso na qualidade do código, arquitetura sólida, e aplicação de boas práticas de engenharia de software, sempre sob supervisão e validação humana crítica. O método foi extensivamente validado através da implementação completa do projeto piloto "Fotix".

## 2. Filosofia e Visão Central

O Método AGV é construído sobre os seguintes pilares:

*   **Qualidade Prioritária:** Aplicar rigorosos princípios de engenharia de software desde o início (comparável a desenvolvedores sênior).
*   **Colaboração Estruturada Humano-IA:** Utilizar LLMs como ferramentas poderosas, guiadas por prompts especializados e um fluxo de trabalho definido.
*   **Validação Humana Crítica:** O coordenador humano é indispensável na definição, revisão, e tomada de decisão.
*   **Iteração e Aprendizado Contínuo:** Refinar o método, os prompts e as estratégias com base na experiência prática.
*   **Documentação Curada na Codebase:** Para bibliotecas específicas ou complexas, fornecer à IA documentação e exemplos diretamente no contexto do projeto, em vez de depender de buscas web externas, garantindo maior controle e precisão.

**Visão de Longo Prazo:** Evoluir o Método AGV para que permita a um coordenador (mesmo sem ser um programador sênior, mas com bom entendimento conceitual) guiar a IA de forma eficaz e cada vez mais eficiente para criar sistemas de software robustos e prontos para produção.

➡️ **Para detalhes aprofundados sobre a filosofia e os princípios, consulte:**
[`Guides/AGV_Method_Principios_Chave_v2.0.md`](./Guides/AGV_Method_Principios_Chave_v2.0.md)

➡️ **Para o roteiro estratégico de evolução do método, consulte:**
[`Guides/Roteiro_Estrategico_Metodo_AGV_Desenvolvimento_Evolucao_v2.0.md`](./Guides/Roteiro_Estrategico_Metodo_AGV_Desenvolvimento_Evolucao_v2.0.md)

## 3. Os Agentes AGV (v3.0 - Pós-Fotix)

O trabalho é orquestrado através dos seguintes agentes (representados por prompts especializados):

*   **Tocrisna (IA - Arquiteta):** Define a arquitetura técnica, componentes, interfaces e dependências.
    *   *Prompt:* `Prompts/Templates/Uso_Constante/Prompt_F1_Tocrisna_Architecture_v1.1d.md`
*   **OrchestratorHelper (IA - Planejadora):** Analisa o blueprint e sugere uma ordem de implementação, incluindo pontos e cenários para Testes de Integração (TIs).
    *   *Prompt:* `Prompts/Templates/Uso_Constante/Prompt_F2_Orchestrator_v1.5.md`
*   **ImplementadorMestre (IA - Engenheira de Implementação e TUs):** Implementa módulos e seus Testes Unitários (TUs), aderindo à stack e usando documentação curada na codebase quando necessário.
    *   *Prompt:* `Prompts/Templates/Uso_Constante/Prompt_F4_Implementador_Mestre_v2.7.md` (contém a Diretriz 4 evoluída)
*   **IntegradorTester (IA - Engenheira de TIs):** Gera Testes de Integração para grupos de módulos.
    *   *Prompt:* `Prompts/Templates/Uso_Constante/Prompt_F4.1_Implementador_TesteDeIntegracao_v1.0.md`
*   **(Opcional) ValidadorOrdemDescricao (IA - Validadora):** Revisa a saída do `OrchestratorHelper`.
    *   *Prompt:* `Prompts/Templates/Uso_Constante/Prompt_F3_Validacao_Orchestrator_v1.1.md`

## 4. Fluxo de Trabalho Resumido (v3.0)

O desenvolvimento segue um ciclo iterativo e incremental:

1.  **Definição Inicial (Coordenador):** Visão, escopo, stack tecnológica (incluindo framework de testes).
2.  **Arquitetura Técnica (Tocrisna):** Geração do Blueprint Arquitetural. *[Validação Humana]*
3.  **Ordem de Implementação e Planejamento de TIs (OrchestratorHelper):** Geração da ordem de implementação e identificação de pontos de Teste de Integração. *[Validação Humana Opcional/Recomendada]*
4.  **Ciclo de Implementação (Iterativo, por item da Ordem):**
    *   **Se Módulo Principal:**
        *   **Implementação e TUs (ImplementadorMestre):** IA implementa o módulo e seus Testes Unitários, usando documentação na codebase para bibliotecas específicas se instruído. *[Validação Humana Crítica do código, TUs e cobertura]*
    *   **Se Ponto de Teste de Integração:**
        *   **Geração de TIs (IntegradorTester):** IA gera Testes de Integração para o grupo de módulos recém-concluído. *[Validação Humana Crítica dos TIs]*
5.  **Commit e Próximo Item:** Após validação, o código é versionado.
6.  **Revisão Final e Conclusão do Projeto.**
7.  **Ciclo de Vida (Manutenção e Evolução):** O método pode ser reaplicado para novas features ou correções.

➡️ **Para o fluxo detalhado passo a passo, consulte:**
[`Guides/AGV_Method_Workflow_v3.0.md`](./Guides/AGV_Method_Workflow_v3.0.md)

## 5. Estrutura do Repositório (Recomendada)

*   **/AGV_MethodTimeline:** Contém documentos históricos da evolução do método, como os "Snapshots Detalhados e Contextualizados".
    *   `AGV_Method_State_Snapshot_v8.0.md` (Exemplo do snapshot final pós-Fotix).
*   **/Guides:** Contém a documentação principal e atualizada do Método AGV:
    *   `AGV_Method_Workflow_v3.0.md`
    *   `AGV_Method_Principios_Chave_v2.0.md`
    *   `Roteiro_Estrategico_Metodo_AGV_Desenvolvimento_Evolucao_v2.0.md`
*   **/Prompts:**
    *   **/Templates:** Contém os templates de prompt modelo `.md` organizados em:
        *   **/Uso_Constante:** Prompts principais utilizados regularmente no fluxo de trabalho (Tocrisna, OrchestratorHelper, ImplementadorMestre, IntegradorTester, etc.).
        *   **/Uso_Esporadico:** Prompts auxiliares utilizados em situações específicas ou menos frequentes.
    *   **/FilledPrompts_Demo:** Exemplos de prompts preenchidos para referência.
*   **/Relatorios_Testes_Implementacao_AGV (ou similar):** Contém relatórios de experimentos, comparações e os relatórios gerados pela IA durante as implementações.
*   `README.md`: Este arquivo.
*   *(Outras pastas conforme a necessidade do projeto sendo desenvolvido, ex: `src/`, `tests/` para o código do projeto piloto)*

## 6. Como Usar o Método AGV (v3.0)

1.  **Familiarize-se:** Leia os documentos em `Guides/` para entender o fluxo, os princípios e a estratégia.
2.  **Prepare o Ambiente:** Configure seu ambiente de desenvolvimento e acesso à LLM de sua escolha.
3.  **Fase 1 - Definição:** Defina claramente o projeto, escopo e stack.
4.  **Siga o Fluxo (Fase 2 em diante):** Execute as fases descritas em `Guides/AGV_Method_Workflow_v3.0.md`.
5.  **Utilize os Prompts:** Copie os templates de `Prompts/Templates/Uso_Constante/` (para os prompts principais do fluxo) ou `Prompts/Templates/Uso_Esporadico/` (para tarefas específicas), preencha-os cuidadosamente com o contexto necessário (incluindo Blueprint, Ordem de Implementação, código existente, e documentação curada de bibliotecas se aplicável) e submeta à LLM.
6.  **Valide CRITICAMENTE e Itere:** Revise todos os outputs da IA. Não hesite em pedir correções, refatorações ou re-implementações até que os padrões de qualidade sejam atendidos. A iteração é chave.
7.  **Documente os Aprendizados:** Use "Snapshots" ou outros mecanismos para registrar a evolução, os desafios e os aprendizados com o método e a IA.

## 7. Status Atual e Próximos Passos (do Método AGV)

*   **Validação da Qualidade (Prioridade #1):** O Método AGV foi validado com sucesso através da conclusão do projeto piloto "Fotix", demonstrando sua capacidade de produzir software de alta qualidade.
*   **Foco Atual (Prioridade #2):** Otimização do processo para maior autonomia da IA e velocidade de desenvolvimento, sem comprometer a qualidade.
*   **Próximos Passos:**
    1.  Consolidação da documentação final do método (workflows, princípios, este README).
    2.  Planejamento e execução de experimentos focados na otimização de prompts e do fluxo de trabalho.
    3.  Avaliação contínua de novas LLMs e ferramentas.

## 8. Validação Prática: O Projeto Piloto Fotix

Para validar e refinar o Método AGV, foi desenvolvido um projeto piloto completo chamado **Fotix**, uma aplicação desktop para detecção e gerenciamento de arquivos duplicados.

*   **Objetivo do Fotix:** Criar uma ferramenta robusta e intuitiva que permita aos usuários escanear diretórios (incluindo o conteúdo de arquivos ZIP), identificar arquivos duplicados com base em seu conteúdo (hash BLAKE3), e oferecer opções seguras para gerenciá-los (ex: mover para lixeira com capacidade de backup e restauração).

*   **Funcionalidades e Componentes Implementados com o Método AGV:**
    *   **Configuração da Aplicação:** Carregamento e persistência de configurações.
    *   **Infraestrutura:** Serviços para logging, operações de sistema de arquivos (incluindo movimentação para lixeira), manipulação eficiente de arquivos ZIP (usando `stream-unzip`), gerenciamento de concorrência para tarefas paralelas, e um sistema de backup/restauração.
    *   **Core/Domínio:** Lógica central para hashing de arquivos (BLAKE3), identificação de conjuntos de duplicatas, e múltiplas estratégias para seleção de qual arquivo manter em um conjunto.
    *   **Camada de Aplicação:** Serviços para orquestrar os casos de uso, como o processo de varredura e o gerenciamento de duplicatas (remoção/backup).
    *   **Interface do Usuário (UI):** Uma GUI desktop desenvolvida com PySide6, permitindo ao usuário selecionar diretórios, visualizar os resultados, e interagir com as funcionalidades de gerenciamento.

*   **Principais Desafios Superados e Aprendizados do Método AGV no Fotix:**
    *   **Adesão a Bibliotecas Específicas:** O desafio inicial de fazer a IA utilizar corretamente bibliotecas menos comuns ou com APIs complexas (como `stream-unzip` para leitura de ZIPs e `PySide6` para a UI) foi superado com sucesso através da **evolução da Diretriz 4 do `Prompt_Implementador_Mestre`**. A estratégia de fornecer documentação curada e exemplos dessas bibliotecas diretamente na codebase (ou contexto do prompt) e instruir a IA a parar e solicitar ajuda ao Coordenador se essa documentação fosse insuficiente, provou ser crucial. Isso evitou que a IA desviasse para alternativas não desejadas ou produzisse código não funcional.
    *   **Qualidade e Cobertura de Testes:** O método guiou a IA para produzir Testes Unitários com alta cobertura para a maioria dos módulos, frequentemente com a IA realizando auto-correções ou o Coordenador solicitando ajustes finos para atingir a cobertura desejada. Os Testes de Integração também foram implementados para validar a colaboração entre os principais subsistemas.
    *   **Estrutura Arquitetural:** A arquitetura em camadas, definida no início pela "Tocrisna" e seguida pelo "ImplementadorMestre", resultou em um código bem organizado, modular e testável.

*   **Resultado:** O projeto Fotix foi **concluído com sucesso**, com todos os seus componentes principais implementados e testados. Este resultado validou a **Prioridade #1 do Método AGV**: a capacidade de guiar a IA para produzir software de alta qualidade, comparável ao desenvolvido por humanos experientes. Os aprendizados obtidos com o Fotix foram fundamentais para refinar o Método AGV para sua versão atual.

## 9. Contribuições e Feedback

Este método está em constante evolução. Feedback, sugestões e relatos de experiência com a aplicação do Método AGV são muito bem-vindos!