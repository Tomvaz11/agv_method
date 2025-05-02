# Método AGV: Desenvolvimento Assistido por IA (v1.0)

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento%20(v1.0)-orange)

## 1. Introdução

Bem-vindo ao repositório do **Método AGV (Assistência Generativa à Velocidade)**. Este projeto documenta e gerencia uma metodologia estruturada para desenvolver software de alta qualidade através da colaboração estratégica entre um coordenador humano e Modelos de Linguagem Grandes (LLMs) atuando como assistentes especializados ("Agentes").

O objetivo principal é alavancar o poder das IAs generativas para acelerar o desenvolvimento, mantendo um foco rigoroso na qualidade do código, arquitetura sólida, manutenibilidade e aplicação de boas práticas de engenharia de software, sempre sob supervisão e validação humana crítica.

## 2. Filosofia e Princípios Chave

O Método AGV é construído sobre os seguintes pilares:

*   **Qualidade desde o Início:** Enfatiza a definição de uma arquitetura robusta e a aplicação de padrões de alta qualidade desde as fases iniciais para minimizar débitos técnicos e refatorações complexas futuras.
*   **Colaboração Humano-IA Estruturada:** Utiliza LLMs como ferramentas poderosas, mas reconhece a necessidade indispensável de direcionamento estratégico, definição de requisitos e validação crítica por parte do coordenador humano.
*   **Processo Orientado por Fases e Agentes:** Divide o ciclo de desenvolvimento em fases lógicas, com "agentes" (representados por prompts modelo especializados) responsáveis por tarefas específicas (arquitetura, especificação, implementação, refatoração, testes).
*   **Interfaces Explícitas:** Adota uma abordagem de **Integração Incremental via Interfaces Explícitas** para garantir baixo acoplamento e alta coesão entre os módulos. Os contratos entre componentes são definidos na arquitetura e rigorosamente seguidos na implementação.
*   **Prompts "Estado da Arte":** Utiliza prompts modelo detalhados, reutilizáveis e versionados como principal mecanismo para instruir a IA, garantindo consistência e qualidade nas interações.
*   **Iteração e Refinamento:** O método e seus artefatos (prompts, documentos) são considerados vivos e sujeitos a refinamento contínuo com base na experiência prática.

➡️ **Para detalhes aprofundados sobre os princípios, consulte:** [`Guides/AGV_Method_Principios_Chave.md`](./Guides/AGV_Method_Principios_Chave.md)

## 3. Os Agentes AGV (v1.0)

Mesmo que executados pela mesma LLM (guiada pelo coordenador humano), conceitualizamos o trabalho através dos seguintes agentes especializados:

*   **Tocrisna (Arquiteta):** Define a estrutura técnica, componentes, padrões e interfaces do sistema.
*   **Severino (Especificador):** Traduz requisitos funcionais de alto nível em especificações técnicas detalhadas para um módulo, respeitando a arquitetura.
*   **Tocle (Engenheiro):** Implementa o código funcional e os testes unitários (com mocks) conforme a especificação e a arquitetura. Também atualiza/refatora testes.
*   **Tolete (Refatorador):** Melhora a qualidade do código de produção existente sem alterar a funcionalidade.

## 4. Fluxo de Trabalho Resumido

O desenvolvimento de uma funcionalidade tipicamente segue as fases:

1.  **Definição (Você):** Visão, objetivos, stack.
2.  **Arquitetura (Tocrisna):** Geração do blueprint e interfaces. *[Validação Humana]*
3.  **Especificação (Severino):** Detalhamento funcional de um módulo. *[Validação Humana]*
4.  **Implementação (Tocle):** Geração de código e testes unitários.
5.  **Revisão & Testes (Você + Tocle/Tolete):** Revisão de código, execução de testes unitários, refatoração (Tolete), ajuste de testes (Tocle), execução de testes de integração. *[Validação Humana + Iteração]*
6.  **Integração & Próximo Ciclo:** Commit do código validado, seguir para próxima feature/módulo.

➡️ **Para o fluxo detalhado passo a passo, consulte:** [`Guides/AGV_Method_Workflow_v1.0.md`](./Guides/AGV_Method_Workflow_v1.0.md)

## 5. Estrutura do Repositório

*   **/Guides:** Contém a documentação principal do Método AGV:
    *   `AGV_Method_Workflow_v1.0.md`: O fluxo de trabalho detalhado.
    *   `AGV_Method_Principios_Chave.md`: Os princípios de design e arquitetura.
    *   `README_Prompt_*.md`: **Importante:** Arquivos README individuais explicando o propósito, uso e princípios de cada prompt modelo localizado na pasta `Prompts/Templates/`. Essenciais para análise e otimização dos prompts.
*   **/AGV_MethodTimeline:** Contém documentos históricos do desenvolvimento do método:
    *   `AGV_Method_State_Snapshot_v2.0.md`: Resumo periódico do estado da colaboração e definição do método (para continuidade).
*   **/Prompts:** Contém os templates e prompts preenchidos:
    *   **/Templates:** Templates de prompt modelo `.md` reutilizáveis para cada agente/tarefa. Estes são os arquivos a serem copiados e preenchidos para interagir com a LLM.
    *   **/FilledPrompts_Demo:** Exemplos de prompts preenchidos para referência.
*   **/Research:** Contém resultados de pesquisas e análises comparativas para escolha de tecnologias.
*   **Scripts de Automação:**
    *   `iniciar-trabalho.bat`: Script para preparar o ambiente de trabalho e sincronizar com o repositório remoto.
    *   `atualizar-github.bat`: Script para enviar alterações para o repositório remoto.
*   `README.md`: Este arquivo.

## 6. Como Usar o Método AGV (v1.0)

1.  **Familiarize-se:** Leia os documentos em `Guides/` (workflow e princípios) para entender o processo e a filosofia.
2.  **Siga o Fluxo:** Execute as fases descritas em `Guides/AGV_Method_Workflow_v1.0.md`.
3.  **Utilize os Prompts:** Para cada interação com a LLM representando um agente, copie o conteúdo do prompt modelo correspondente de `Prompts/Templates/`, preencha os placeholders com as informações específicas do seu projeto/tarefa, e submeta à LLM. Consulte o README do prompt específico em `Guides/` se tiver dúvidas sobre seu uso.
4.  **Valide e Itere:** Revise criticamente os outputs da IA em cada etapa e não hesite em iterar ou ajustar os prompts conforme necessário.
5.  **Use os Scripts de Automação:** Utilize os scripts batch fornecidos para facilitar o trabalho com o repositório Git:
   * Execute `iniciar-trabalho.bat` para preparar o ambiente e obter a versão mais recente do código.
   * Execute `atualizar-github.bat` para enviar suas alterações para o repositório remoto.

## 7. Status Atual

*   **Versão do Método:** 1.0 (definição inicial)
*   **Status:** Em desenvolvimento ativo e refinamento através de projetos piloto.

---