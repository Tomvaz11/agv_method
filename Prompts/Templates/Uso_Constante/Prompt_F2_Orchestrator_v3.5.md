# AGV Prompt: OrchestratorHelper v3.5 (Granularidade Máxima)

**Tarefa Principal:** Analisar o `@Blueprint_Arquitetural.md`, que é a fonte única da verdade sobre a arquitetura. Suas responsabilidades são: (1) Derivar uma ordem de implementação lógica e (2) Gerar cenários chave para os Testes de Integração.

**Input Principal (Blueprint Arquitetural):**

## --- Conteúdo do Blueprint Arquitetural ---

[ADICIONE AQUI O CONTEÚDO DO BLUEPRINT]

---

**Diretrizes Essenciais:**

1. **Análise de Dependências com Decomposição Máxima:** A ordem de implementação deve ser determinada pelo princípio de **responsabilidade única por alvo**. Siga estas regras de decomposição:

   a. **Ordem de Módulos Transversais:** Os módulos que fornecem funcionalidades transversais **DEVEM** ser implementados primeiro. A ordem de implementação e validação entre eles deve seguir a lógica de dependência: **Autenticação > Gestão de Usuários e Autorização > Multi-Tenancy**.

   b. **Decomposição Obrigatória por Tipo (Backend):** Para cada módulo de negócio (ex: `iabank.users`, `iabank.loans`), você **DEVE** criar alvos de implementação separados e sequenciais para cada camada lógica, na seguinte ordem:

   1. **Modelos:** Apenas os arquivos `models.py`.
   2. **Repositórios/Infraestrutura:** Apenas a lógica de acesso a dados.
   3. **Serviços de Aplicação:** Apenas a lógica de negócio dos casos de uso.
   4. **Serializers:** Apenas os arquivos `serializers.py` da API.
   5. **Views/URLs:** Apenas os endpoints `views.py` e o roteamento `urls.py`.

   c. **Regra Especial para `users`:** O módulo de usuários **DEVE** ser decomposto em duas fases funcionais distintas, cada uma com sua própria parada de testes:

   1. **Fase 1: Autenticação JWT.** Implemente apenas os modelos, serializers e views necessários para os endpoints de obtenção e refresh de token (ex: `/token/`).
   2. **Fase 2: Gestão de Usuários e Autorização.** Após validar a autenticação, implemente os endpoints de CRUD de usuários (ex: `/users/`, `/users/me/`) e a lógica de permissões/perfis (RBAC).

2. **Criação do "Alvo 0":** Sua primeira tarefa é SEMPRE gerar um item inicial na ordem de implementação chamado **"Alvo 0: Setup do Projeto Profissional"**. Os detalhes do que este alvo implica estão definidos no prompt do Implementador (`F4`).

3. **Geração da Ordem Sequencial e Pontos de Teste:** Crie uma lista numerada de "Alvos de Implementação".

   - **Formato do Alvo:** Cada item da lista deve seguir o formato `**Alvo X:** <Módulo>: <Responsabilidade Única>` (ex: `**Alvo 2:** iabank.users: Modelos e Migrações`).
   - **Identificação de Paradas de Teste:** Insira um ponto de verificação após **um grupo de 2 a 4 alvos** que, juntos, completam uma funcionalidade vertical mínima (ex: após implementar modelos, serializers e views de um CRUD básico).
   - **Formato da Parada de Teste:** O ponto de verificação deve seguir o formato exato:
     `>>> **PARADA DE TESTES DE INTEGRAÇÃO T<Número>** (Nome da Funcionalidade Validada) <<<`
     O `<Número>` deve ser sequencial, começando em 1.

4. **Decomposição Granular Obrigatória da UI:** Ao definir os alvos para a Camada de Apresentação (UI), você **DEVE** criar alvos de implementação separados para cada camada lógica da arquitetura frontend, na seguinte ordem estrita:

   a. **Alvo UI-1:** Camada `shared/ui` (Biblioteca de componentes puros e reutilizáveis).
   b. **Alvo UI-2:** Camada `shared/api` e `shared/lib` (Configuração do cliente HTTP, utilitários e hooks genéricos).
   c. **Alvo UI-3:** Camada `entities` (Componentes, tipos e hooks relacionados a entidades de negócio).
   d. **Alvo UI-4:** Camada `features` (Implementação das lógicas de interação do usuário).
   e. **Alvo UI-5:** Camada `app` e `pages` (Configuração global, roteamento e composição final das telas).

   **Crie paradas de teste intermediárias para validar a UI, por exemplo, uma após a implementação das camadas `shared` e `entities` (para testar os componentes), e outra no final (para testar o fluxo completo).**

5. **Geração de Cenários de Teste de Integração:**

   - Para cada `>>> PARADA ... <<<` criada, você **DEVE** gerar uma seção detalhada logo abaixo dela.
   - Esta seção deve conter:
     - **Módulos no Grupo:** Liste os módulos principais implementados desde a última parada.
     - **Objetivo do Teste:** Descreva em uma frase clara o que se espera validar com a integração deste grupo, baseando-se nas responsabilidades combinadas dos módulos conforme o Blueprint.
     - **Cenários Chave:** Liste de 2 a 4 cenários de teste específicos e acionáveis que verifiquem as interações mais críticas. Para paradas que dependem de etapas anteriores (ex: testar uma funcionalidade que requer autenticação), os cenários devem mencionar o uso de simulação de pré-condições (ex: "Usando um usuário autenticado simulado...") em vez de repetir o fluxo completo.

6. **Simplicidade do Output:** O resultado final deve ser um documento Markdown contendo apenas a lista numerada da "Ordem de Implementação" com os "Alvos" e as "Paradas de Teste" detalhadas. **Não inclua justificativas ou descrições adicionais; foque apenas no plano de ação.**

**Resultado Esperado:**

Um documento Markdown (`Output_Ordem_e_Testes.md`) contendo a ordem de implementação e, para cada ponto de TI, os detalhes (Módulos, Objetivo, Cenários) para guiar a próxima fase de testes.
