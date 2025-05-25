# AGV Prompt Template: OrchestratorHelper v1.6 - Ordem de Implementação com Pontos de Teste de Integração

**Tarefa Principal:** Analisar o Blueprint Arquitetural fornecido, sugerir uma ordem de implementação lógica para os componentes/módulos **principais**, gerar uma Descrição de Alto Nível Inicial para cada um, e identificar pontos de verificação estratégicos onde testes de integração devem ser realizados, sugerindo os principais cenários a serem cobertos. O resultado deve ser apresentado com **instruções claras para o Coordenador** sobre como proceder.

**Contexto:** O objetivo é fornecer ao Coordenador uma sequência recomendada, descrições iniciais, orientação explícita sobre quais módulos implementar, como lidar com os módulos base, e quando e como abordar os testes de integração iniciais.

**Input Principal (Blueprint Arquitetural):**

```markdown
# --- Conteúdo do Blueprint Arquitetural ---
[COLE AQUI O CONTEÚDO COMPLETO DO ARQUIVO MARKDOWN DO BLUEPRINT GERADO PELA TOCRISNA (v1.1d+). A IA deve extrair as informações necessárias a partir deste conteúdo.]
```

**Diretrizes para Geração:**

1.  **Identificar Componentes, Dependências e Nome Raiz do Pacote:**
    *   Parsear o blueprint para extrair componentes/módulos principais, módulos base, suas dependências e responsabilidades.
    *   **Inferir o "Nome Raiz do Pacote Principal do Projeto"** (ex: `fotix`, `meu_projeto`) a partir dos caminhos dos módulos e da estrutura de diretórios (ex: `src/[nome_raiz_pacote]/`) definidos no Blueprint. Este nome será usado para gerar exemplos de caminhos no output.

2.  **Separar Módulos Base:**
    *   Identifique módulos que são puramente utilitários, de configuração, modelos de dados ou definições de interfaces (ex: `[nome_raiz_pacote]/utils`, `[nome_raiz_pacote]/config`, `[nome_raiz_pacote]/core/models`, `[nome_raiz_pacote]/[camada]/interfaces.py`).

3.  **Analisar Grafo de Dependências (Módulos Principais):**
    *   Foque nas dependências entre os módulos que contêm lógica de implementação significativa (ex: Core, Infrastructure Services, Application Services, UI).

4.  **Gerar Ordem Lógica (Módulos Principais):**
    *   Produza uma sequência numerada **APENAS para os módulos principais** que respeite as dependências (implementar dependências primeiro).
    *   Priorize módulos de infraestrutura e core que são pré-requisitos para funcionalidades mais complexas.
    *   Se o Blueprint Arquitetural propuser uma decomposição da Camada de UI em Telas/Views ou Componentes de UI significativos, cada um desses componentes de UI deve ser tratado como um 'Módulo Principal' individual na ordem de implementação. Priorize a implementação de componentes de UI que dependam de funcionalidades de backend já implementadas ou que sejam fundamentais para o fluxo inicial do usuário.

5.  **Gerar Descrição Inicial e Justificativa (Para cada item na Ordem Principal):**
    *   Para cada módulo na ordem, forneça uma "Descrição de Alto Nível Inicial" (1-2 frases) do seu propósito principal, baseada no Blueprint.
    *   Forneça uma breve "Justificativa da Ordem" para sua posição na sequência.
    *   Liste também as "Dependências Chave (Inferidas do Blueprint)" de outros módulos ou interfaces importantes, se claramente identificáveis.

6.  **Identificar Pontos de Verificação para Testes de Integração:**
    *   Com base na arquitetura e na ordem de implementação sugerida, identifique grupos de módulos que, uma vez implementados, completam um "subsistema coerente" ou uma "capacidade funcional significativa" que se beneficiaria de testes de integração.
    *   Insira esses pontos de verificação na "Ordem de Implementação Sugerida" como uma **">>> PARADA PARA TESTES DE INTEGRAÇÃO (Nome do Subsistema) <<<"**.
    *   Para cada "PARADA PARA TESTES DE INTEGRAÇÃO":
        *   Liste os Módulos Principais (e seus módulos base associados) que foram implementados no grupo recém-concluído.
        *   Defina claramente o "Objetivo do Teste de Integração" para este grupo.
        *   Sugira 2-4 "Cenários Chave para Teste de Integração", descrevendo as interações ou fluxos específicos a serem testados. Esses cenários devem ser compreensíveis para o Coordenador.
        *   Inclua uma "Instrução para o Coordenador" clara sobre usar um prompt futuro (ex: `Prompt_IntegradorTester_vX.Y`, a ser definido) para gerar e executar esses testes antes de prosseguir.

7.  **Formatar Output com Instruções Claras para o Coordenador:**
    *   **CRUCIAL:** Estruture o output final para incluir um texto introdutório explicando ao Coordenador como usar a informação gerada, incluindo como lidar com os Módulos Base e as novas "PARADAS PARA TESTES DE INTEGRAÇÃO".

8.  **Listar Módulos Base Separadamente (Após as Instruções):**
    *   Após o texto introdutório, liste os Módulos Base identificados com suas responsabilidades (conforme encontradas no blueprint), para que o Coordenador esteja ciente deles, mesmo que não os implemente diretamente.

9.  **Identificar Ciclos:**
    *   Se um ciclo de dependência *entre os módulos principais* for detectado que impeça uma ordenação linear, relate-o claramente em vez da ordem.

**Resultado Esperado:**

Um documento Markdown (`Ordem_Com_Descricoes_e_Testes_Integracao.md` ou similar) contendo:

1.  **Instruções para o Coordenador (Texto Introdutório - IMPORTANTE):**
    Um parágrafo claro no início do output explicando:
    *   Que o output separa "Módulos Base" de "Módulos Principais".
    *   Que os **Módulos Base listados NÃO devem ser implementados diretamente** usando o `ImplementadorMestre` nesta fase inicial (sua estrutura será criada conforme necessário e o conteúdo de `utils` adicionado organicamente).
    *   Que a implementação deve **SEGUIR a "Ordem de Implementação Sugerida (Módulos Principais e Pontos de Teste de Integração)"**, começando pelo **Item #1** da lista numerada.
    *   Que para cada item numerado de Módulo Principal, o Coordenador deve usar o `Prompt_ImplementadorMestre_vX.Y` (recomenda-se a versão mais recente, ex: v1.7+) junto com o `@Blueprint_Arquitetural.md` e este output (`@Ordem_Com_Descricoes_e_Testes_Integracao.md`), preenchendo apenas o nome do módulo alvo.
    *   **NOVO:** Que em certos pontos, o documento indicará uma **">>> PARADA PARA TESTES DE INTEGRAÇÃO (Nome do Subsistema) <<<"**. Nestes momentos, antes de prosseguir com o próximo módulo da lista, o Coordenador deverá usar um prompt específico para testes de integração (ex: `Prompt_IntegradorTester_vX.Y`, a ser definido) para criar e executar testes de integração para o grupo de módulos recém-concluído, usando os cenários sugeridos como guia.

2.  **Módulos Base (Estrutura Inicial / Conteúdo On-Demand):**
    Lista dos módulos base com suas responsabilidades (ex: `[nome_raiz_pacote].core.models`, `[nome_raiz_pacote].utils.helpers`, etc.).

3.  **Ordem de Implementação Sugerida (Módulos Principais e Pontos de Teste de Integração):**
    Lista **numerada** dos módulos principais, intercalada com as seções "PARADA PARA TESTES DE INTEGRAÇÃO".

4.  Para cada **item de Módulo Principal** na lista numerada:
    *   O nome completo do componente/módulo (ex: `[nome_raiz_pacote].infrastructure.logging_config`).
    *   **Descrição de Alto Nível Inicial:** (1-2 frases).
    *   **Justificativa da Ordem:** (Breve explicação).
    *   **Dependências Chave (Inferidas do Blueprint):** (Lista opcional das principais interfaces ou módulos dos quais depende).

5.  Para cada **">>> PARADA PARA TESTES DE INTEGRAÇÃO (Nome do Subsistema) <<<"**:
    *   **Módulos Implementados neste Grupo:** (Lista dos módulos principais recém-concluídos).
    *   **Objetivo do Teste de Integração:** (O que se quer validar).
    *   **Cenários Chave para Teste de Integração:** (2-4 cenários descritos).
    *   **Instrução para o Coordenador:** (Como proceder com o teste de integração).

6.  **OU**, se um ciclo for detectado entre os módulos principais:
    *   Mensagem de erro clara identificando o ciclo.

**Exemplo de Texto Introdutório (Instruções no Output):**

```markdown
## Análise de Implementação e Próximos Passos para [Nome do Projeto Inferido]

**Instruções para o Coordenador:**

Este documento organiza os módulos do projeto [Nome do Projeto Inferido] para guiar a implementação. Ele separa os "Módulos Base" (definições, utilitários e interfaces) dos "Módulos Principais" (que contêm a lógica central e as implementações concretas dos serviços).

*   **NÃO implemente os "Módulos Base" listados abaixo diretamente agora.** Suas pastas e arquivos básicos (como `__init__.py`, arquivos de interfaces, modelos de dados) serão criados ou modificados quando necessário pela IA (`ImplementadorMestre`) durante a implementação dos módulos principais que dependem deles. O conteúdo específico de módulos como `[nome_raiz_pacote].utils` será adicionado organicamente conforme a necessidade surgir.
*   **SIGA a "Ordem de Implementação Sugerida (Módulos Principais e Pontos de Teste de Integração)" abaixo.** Comece pelo **Item #1** da lista de Módulos Principais e prossiga sequencialmente.
*   Para **CADA item** da ordem numerada de Módulo Principal, use o `Prompt_ImplementadorMestre_vX.Y` (recomenda-se a versão mais recente, ex: v1.7+), preenchendo apenas o nome do módulo alvo (ex: "Item 1: `[nome_raiz_pacote].infrastructure.logging_config`"). Anexe sempre o `@Blueprint_Arquitetural.md`, este arquivo (`@Ordem_Com_Descricoes_e_Testes_Integracao.md`) e o código relevante já existente como contexto. A "Descrição de Alto Nível Inicial" listada abaixo para cada item servirá como ponto de partida para a IA.
*   **PONTOS DE TESTE DE INTEGRAÇÃO:** Em certos pontos, este documento indicará uma **">>> PARADA PARA TESTES DE INTEGRAÇÃO (Nome do Subsistema) <<<"**. Nestes momentos, **antes de prosseguir** com o próximo Módulo Principal da lista, você deverá usar um prompt dedicado para testes de integração (ex: `Prompt_IntegradorTester_vX.Y`, que será definido posteriormente) para guiar a IA na criação e execução de testes de integração para o grupo de módulos recém-concluído. Utilize os "Cenários Chave para Teste de Integração" listados como ponto de partida para esses testes. Após os testes de integração serem concluídos e validados, você poderá prosseguir para o próximo item da ordem de implementação.

---

### Módulos Base (Estrutura Inicial / Conteúdo On-Demand)

*   `[nome_raiz_pacote].core.models`: Define as estruturas de dados centrais do domínio (ex: FileInfo, DuplicateSet).
*   `[nome_raiz_pacote].utils.helpers`: Contém funções auxiliares genéricas.
*   `[nome_raiz_pacote].config`: Gerencia a configuração da aplicação.
*   `[nome_raiz_pacote].infrastructure.interfaces`: Define os contratos para os serviços da camada de infraestrutura.
*   `[nome_raiz_pacote].core.interfaces`: Define os contratos para os serviços da camada de core/domínio.
*   ... (outros conforme identificados no Blueprint)

---

### Ordem de Implementação Sugerida (Módulos Principais e Pontos de Teste de Integração) - COMECE AQUI (Item #1)

1.  **`[nome_raiz_pacote].infrastructure.logging_config`**
    *   **Descrição de Alto Nível Inicial:** Configurar o sistema de logging para a aplicação.
    *   **Justificativa da Ordem:** Essencial para depuração e monitoramento desde o início.
    *   **Dependências Chave (Inferidas do Blueprint):** `[nome_raiz_pacote].config` (para níveis de log, etc.)

2.  **`[nome_raiz_pacote].infrastructure.file_system`**
    *   **Descrição de Alto Nível Inicial:** Implementar a interface `IFileSystemService` para operações de arquivo.
    *   **Justificativa da Ordem:** Base para muitas outras funcionalidades.
    *   **Dependências Chave (Inferidas do Blueprint):** `[nome_raiz_pacote].infrastructure.interfaces.IFileSystemService`

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (INFRAESTRUTURA DE ARQUIVOS E LOG) <<<**

*   **Módulos Implementados neste Grupo:** `logging_config`, `file_system` (e seus módulos base associados como `[nome_raiz_pacote].config`, `[nome_raiz_pacote].infrastructure.interfaces`).
*   **Objetivo do Teste de Integração:** Verificar se o `FileSystemService` opera corretamente e se suas ações são logadas conforme esperado pelo `logging_config`.
*   **Cenários Chave para Teste de Integração:**
    1.  **Operação de Arquivo com Logging:** Execute uma operação básica do `FileSystemService` (ex: criar um diretório temporário, listar seu conteúdo e depois removê-lo) e verifique se as mensagens de log apropriadas (INFO, DEBUG, ERROR em caso de falha simulada) são geradas e capturadas.
    2.  **Configuração de Log Afetando Serviço:** (Se aplicável e o `logging_config` for dinâmico) Mude um nível de log através do `config` e verifique se o output do log do `FileSystemService` (ou de outros serviços que o usem) reflete a mudança.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` (a ser definido) para gerar testes para estes cenários. Após os testes passarem e serem validados, prossiga para o próximo item da ordem de implementação.
---
... (etc.)
```