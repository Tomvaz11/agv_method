# Método AGV: Desenvolvimento Assistido por IA (v1.2)

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento%20(v1.2)-orange)

## 1. Introdução

Bem-vindo ao repositório do **Método AGV (Assistência Generativa à Velocidade)**. Este projeto documenta e gerencia uma metodologia estruturada para desenvolver software de alta qualidade através da colaboração estratégica entre um coordenador humano e Modelos de Linguagem Grandes (LLMs) atuando como assistentes especializados ("Agentes").

O objetivo principal é alavancar o poder das IAs generativas para acelerar o desenvolvimento, mantendo um foco rigoroso na qualidade do código, arquitetura sólida, manutenibilidade e aplicação de boas práticas de engenharia de software, sempre sob supervisão e validação humana crítica.

## 2. Filosofia e Princípios Chave

O Método AGV é construído sobre os seguintes pilares:

*   **Qualidade desde o Início:** Enfatiza a definição de uma arquitetura robusta e a aplicação de padrões de alta qualidade desde as fases iniciais para minimizar débitos técnicos e refatorações complexas futuras.
*   **Colaboração Humano-IA Estruturada:** Utiliza LLMs como ferramentas poderosas, mas reconhece a necessidade indispensável de direcionamento estratégico, definição de requisitos e validação crítica por parte do coordenador humano.
*   **Processo Orientado por Fases e Agentes:** Divide o ciclo de desenvolvimento em fases lógicas, com "agentes" (representados por prompts modelo especializados) responsáveis por tarefas específicas (arquitetura, elaboração de requisitos, especificação, implementação, refatoração, testes, etc.).
*   **Interfaces Explícitas:** Adota uma abordagem de **Integração Incremental via Interfaces Explícitas** para garantir baixo acoplamento e alta coesão entre os módulos. Os contratos entre componentes são definidos na arquitetura e rigorosamente seguidos na implementação.
*   **Prompts "Estado da Arte":** Utiliza prompts modelo detalhados, reutilizáveis e versionados como principal mecanismo para instruir a IA, garantindo consistência e qualidade nas interações.
*   **Iteração e Refinamento:** O método e seus artefatos (prompts, documentos) são considerados vivos e sujeitos a refinamento contínuo com base na experiência prática.

➡️ **Para detalhes aprofundados sobre os princípios, consulte:** [`Guides/AGV_Method_Principios_Chave_v1.0.md`](./Guides/AGV_Method_Principios_Chave_v1.0.md) *(Nota: O conteúdo dos princípios permanece v1.0, mas o método evoluiu)*

## 3. Os Agentes AGV (v1.2)

Conceitualizamos o trabalho através dos seguintes agentes especializados (mesmo que executados pela mesma LLM):

*   **RequirementHelper (Auxiliar):** Assiste o coordenador na elaboração da "Descrição de Alto Nível" de uma funcionalidade através de uma entrevista guiada.
*   **Tocrisna (Arquiteta):** Define a estrutura técnica, componentes, padrões, interfaces e dependências diretas do sistema.
*   **OrchestratorHelper (Auxiliar):** Analisa o blueprint da Tocrisna e sugere uma ordem lógica de implementação dos módulos.
*   **Severino (Especificador):** Traduz a "Descrição de Alto Nível" em especificações técnicas detalhadas para um módulo, respeitando a arquitetura e sugerindo funções para `utils`.
*   **Tocle (Engenheiro):** Implementa o código funcional e testes unitários (com mocks) do módulo principal e, opcionalmente, funções em `utils`, conforme a especificação e a arquitetura. Também atualiza/refatora testes.
*   **Tolete (Refatorador):** Melhora a qualidade do código de produção existente sem alterar a funcionalidade.
*   **(Meta-Agentes/Opcionais):** `PreenchedorGenerico` (para preencher prompts), `ValidadorCruzado` (para validar preenchimento).

## 4. Fluxo de Trabalho Resumido (v1.2)

O desenvolvimento de uma funcionalidade tipicamente segue as fases:

1.  **Definição (Você):** Visão, objetivos, stack, **framework de testes**.
2.  **Arquitetura (Tocrisna):** Geração do blueprint (componentes, interfaces, dependências). *[Validação Humana]*
3.  **(Opcional) Ordem de Implementação (OrchestratorHelper):** Geração da sequência sugerida.
4.  **PARA CADA MÓDULO (seguindo a ordem):**
    *   a. **Elaboração Funcional (RequirementHelper):** Geração da "Descrição de Alto Nível". *[Interação Humana]*
    *   b. **Especificação (Severino):** Detalhamento técnico + sugestões para `utils`. *[Validação Humana]*
    *   c. **Implementação (Tocle):** Geração de código (módulo + opc. `utils`) e testes unitários.
    *   d. **Revisão & Testes (Você + Tocle/Tolete):** Revisão, testes unitários, refatoração, ajuste testes, testes de integração. *[Validação Humana + Iteração]*
5.  **Integração & Próximo Ciclo:** Commit, seguir para próximo módulo.

➡️ **Para o fluxo detalhado passo a passo, consulte:** [`Guides/AGV_Method_Workflow_v1.2.md`](./Guides/AGV_Method_Workflow_v1.2.md)

## 5. Estrutura do Repositório

*   **/Guides:** Contém a documentação principal do Método AGV:
    *   `AGV_Method_Workflow_v1.2.md`: O fluxo de trabalho detalhado atualizado.
    *   `AGV_Method_Principios_Chave_v1.0.md`: Os princípios de design e arquitetura.
    *   *(Removida referência aos READMEs individuais dos prompts)*
*   **/AGV_MethodTimeline:** Contém documentos históricos do desenvolvimento do método:
    *   `AGV_Method_State_Snapshot_v*.md`: Resumos periódicos do estado da colaboração.
*   **/Prompts:** Contém os templates e prompts preenchidos:
    *   **/Templates:** Templates de prompt modelo `.md` reutilizáveis para cada agente/tarefa. Estes são os arquivos a serem copiados e preenchidos para interagir com a LLM.
    *   **/FilledPrompts_Demo:** Exemplos de prompts preenchidos para referência.
*   **/Research:** Contém resultados de pesquisas e análises comparativas.
*   **Scripts de Automação:**
    *   `iniciar-trabalho.bat`: Script para preparar o ambiente.
    *   `atualizar-github.bat`: Script para enviar alterações.
*   `README.md`: Este arquivo.

## 6. Como Usar o Método AGV (v1.2)

1.  **Familiarize-se:** Leia os documentos em `Guides/` (workflow v1.2 e princípios v1.0).
2.  **Siga o Fluxo:** Execute as fases descritas em `Guides/AGV_Method_Workflow_v1.2.md`. Note a adição dos passos com `RequirementHelper` e `OrchestratorHelper`.
3.  **Utilize os Prompts:** Copie os templates de `Prompts/Templates/`, preencha (manualmente ou com IA + validação) e submeta à LLM. Os próprios templates contêm instruções e placeholders.
4.  **Valide e Itere:** Revise criticamente os outputs da IA.
5.  **Use os Scripts de Automação:** Conforme descrito.

## 7. Status Atual

*   **Versão do Método:** 1.2 (Refinamentos no fluxo e adição de helpers)
*   **Status:** Em desenvolvimento ativo e refinamento através de projetos piloto.