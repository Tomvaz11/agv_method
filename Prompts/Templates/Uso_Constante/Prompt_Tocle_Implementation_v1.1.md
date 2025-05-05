# AGV Prompt Template: Tocle v1.2b - Implementação de Código Novo

**Tarefa Principal:** Implementar a funcionalidade/módulo descrito na seção "Especificação" abaixo, criando ou modificando o arquivo Python `[NOME_DO_ARQUIVO_A_SER_CRIADO_OU_MODIFICADO.py]`. **Opcionalmente**, implementar também as funções auxiliares aprovadas para `fotix.utils` (se instruído). Siga rigorosamente as diretrizes e o contexto arquitetural.

**Contexto Arquitetural (Definido por Tocrisna / Severino):**

*   **Nome do Projeto:** `[NOME_DO_PROJETO]`
*   **Objetivo Geral do Projeto:** `[BREVE DESCRIÇÃO DO PROPÓSITO GERAL DO PROJETO]`
*   **Localização deste Módulo/Arquivo:** `[CAMINHO/PASTA/ONDE/ESTE/ARQUIVO/DEVE_FICAR.py]`
*   **Principais Responsabilidades deste Módulo/Arquivo:** `[DESCRIÇÃO CONCISA DO QUE ESTE ARQUIVO DEVE FAZER, CONFORME ARQUITETURA]`
*   **Dependências Diretas deste Módulo:**
    *   `[COPIAR A LISTA EXPLÍCITA DE DEPENDÊNCIAS DIRETAS DO OUTPUT DO SEVERINO/BLUEPRINT. Ex:]`
    *   `fotix.domain.models`
    *   `utils.helpers`
*   **Interfaces de Dependências (Contratos a serem Usados):**
    *   `[FORNECER AQUI AS ASSINATURAS E DESCRIÇÕES DAS FUNÇÕES/MÉTODOS/CLASSES DE *OUTROS MÓDULOS* QUE ESTE CÓDIGO PRECISA CHAMAR. SEJA PRECISO. Ex:]`
    *   `utils.helpers.calcular_hash(file_path: Path) -> str`
*   **Interfaces Expostas (Contratos a serem Fornecidos - se aplicável):**
    *   `[SE ESTE MÓDULO EXPÕE FUNÇÕES/CLASSES PARA OUTROS USarem, LISTAR SUAS ASSINATURAS ESPERADAS AQUI. Ex:]`
    *   `Classe 'DecisionEngine' com método público 'decide_file_to_keep(group: DuplicateGroup) -> FileMetadata'`
*   **Padrões de Design Chave (Relevantes para esta Implementação):** `[PADRÕES RELEVANTES DA ARQUITETURA]`
*   **Estrutura de Dados Principal (Relevantes para esta Implementação):** `[DEFINIÇÃO DE DATACLASSES/NAMEDTUPLES RELEVANTES QUE ESTE MÓDULO USARÁ OU RETORNARÁ]`

**Especificação da Funcionalidade/Módulo a ser Implementada (Gerada por Severino):**

[COLE AQUI A PARTE PRINCIPAL (Especificação Técnica Detalhada) DO OUTPUT DO SEVERINO]

**Instrução Adicional para `fotix.utils` (Opcional - Preencher se houver sugestões aprovadas do Severino):**

*   Implementar também as seguintes funções auxiliares no módulo/arquivo apropriado dentro de `fotix.utils` (ex: `fotix/utils/helpers.py` ou `fotix/utils/formatting.py`):
    *   `[COPIAR AQUI A ASSINATURA E DESCRIÇÃO DA PRIMEIRA FUNÇÃO APROVADA PARA UTILS]`
    *   `[COPIAR AQUI A ASSINATURA E DESCRIÇÃO DA SEGUNDA FUNÇÃO APROVADA PARA UTILS, SE HOUVER]`
*   Se esta seção for deixada em branco ou removida, implementar apenas o módulo principal.

**Stack Tecnológica Permitida (Definida na Fase 1):**

*   **Linguagem:** Python `[VERSÃO - Ex: 3.10+]`
*   **Frameworks Principais:** `[LISTAR - Ex: PySide6]`
*   **Bibliotecas Essenciais:** `[LISTAR - Ex: BLAKE3, send2trash, stream-unzip]` (Permitir importação apenas destas, das bibliotecas padrão Python e dos outros módulos do projeto listados nas 'Dependências Diretas', a menos que instruído a adicionar nova dependência).

**Diretrizes Específicas de Implementação (Versão Explícita - RECOMENDADA):**

1.  **Aderência Estrita às Interfaces e Especificação:** Implementar a funcionalidade conforme descrito na Especificação, utilizando e expondo *exatamente* as interfaces definidas no Contexto Arquitetural. Se instruído na seção "Instrução Adicional", implementar também as funções auxiliares em `fotix.utils`.
2.  **Código Limpo e Legível (PEP 8):** Seguir rigorosamente o PEP 8 para formatação, nomenclatura e estilo. Priorizar clareza e simplicidade (KISS).
3.  **Modularidade e Coesão (SRP):** Criar funções e classes com responsabilidades únicas e bem definidas. Manter alta coesão dentro do módulo(s).
4.  **Type Hints (PEP 484):** Utilizar type hints completos e precisos para todas as funções, métodos, parâmetros e variáveis importantes.
5.  **Tratamento de Erros Robusto:** Antecipar e tratar erros potenciais conforme especificado na seção "Especificação". Usar exceções específicas. Propagar ou tratar erros de forma clara. Utilizar `try/except/finally` e gerenciadores de contexto (`with`) apropriadamente.
6.  **Segurança Básica:** Validar e sanitizar todos os inputs externos ou não confiáveis (incluindo parâmetros recebidos). Evitar práticas inseguras comuns. Usar bibliotecas padrão e seguras para operações sensíveis.
7.  **Documentação (Docstrings PEP 257):** Escrever docstrings claras e completas para o módulo, classes, funções e métodos públicos (propósito, `Args`, `Returns`, `Raises`), referenciando os contratos de interface quando relevante. Comentar apenas lógica complexa ou o *porquê*. Aplicar também às funções em `utils`, se implementadas.
8.  **Sem Código Morto/Desnecessário:** Implementar apenas o necessário para a funcionalidade especificada (tanto no módulo principal quanto em `utils`, se aplicável).
9.  **Testes Unitários:** **OBRIGATÓRIO:** Gerar testes unitários (usando `[NOME_DO_FRAMEWORK_DE_TESTE - Ex: pytest]`) para:
    *   As funções/métodos públicos do **módulo principal**.
    *   **E também** para as funções implementadas em `fotix.utils` (se instruído na seção "Instrução Adicional").
    *   Os testes devem cobrir casos da Especificação ou do propósito da função (sucesso, erro, borda).
    *   Utilizar **mocks/stubs** para simular as "Interfaces de Dependências" ao testar o módulo principal. Testes para `utils` devem ser autocontidos se possível.
    *   Verificar se os "Outputs Esperados" estão corretos.
    *   Colocar testes nos locais apropriados (ex: `tests/unit/[caminho_correspondente]/test_[nome_do_modulo].py`, `tests/unit/utils/test_helpers.py`).
10. **Eficiência (Consideração):** Escrever código razoavelmente eficiente para a tarefa, sem otimização prematura.
11. **Contexto Essencial:** **IMPORTANTE:** Para implementar corretamente, você **precisará conhecer as definições exatas** dos arquivos/módulos listados na seção **"Dependências Diretas"**. Ao executar (ex: no Cursor/Augment), certifique-se de fornecer o conteúdo desses arquivos como contexto (ex: usando `@path/to/dependency.py`). Se estiver implementando funções em `utils`, forneça também o contexto do arquivo de `utils` sendo modificado, se necessário.

**Resultado Esperado:**

1.  **Código Python Completo (Módulo Principal):** Conteúdo final do arquivo `[NOME_DO_ARQUIVO_PRINCIPAL.py]`.
2.  **Código Python Completo (`utils` - se aplicável):** Conteúdo atualizado do arquivo em `fotix.utils` com as novas funções.
3.  **Código de Testes Unitários:** Arquivo(s) de teste para o módulo principal E para as funções de `utils` (se aplicável).
4.  **(Opcional) Breve Relatório:** Explicação de decisões, desafios ou sugestões.