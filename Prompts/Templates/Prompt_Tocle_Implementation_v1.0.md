# AGV Prompt Template: Tocle v1.1 - Implementação de Código Novo

**Tarefa Principal:** Implementar a funcionalidade/módulo descrito na seção "Especificação" abaixo, criando ou modificando o arquivo Python `[NOME_DO_ARQUIVO_A_SER_CRIADO_OU_MODIFICADO.py]`. Siga rigorosamente as diretrizes e o contexto arquitetural fornecido.

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

[COLE AQUI O OUTPUT COMPLETO DA ESPECIFICAÇÃO TÉCNICA DETALHADA GERADA PELO SEVERINO NA FASE 2.5]

**Stack Tecnológica Permitida (Definida na Fase 1):**

*   **Linguagem:** Python `[VERSÃO - Ex: 3.10+]`
*   **Frameworks Principais:** `[LISTAR - Ex: PySide6]`
*   **Bibliotecas Essenciais:** `[LISTAR - Ex: BLAKE3, send2trash, stream-unzip]` (Permitir importação apenas destas, das bibliotecas padrão Python e dos outros módulos do projeto listados nas 'Dependências Diretas', a menos que instruído a adicionar nova dependência).

**Diretrizes Específicas de Implementação:**

1.  **Aderência Estrita às Interfaces e Especificação:** Implementar a funcionalidade conforme descrito na Especificação, utilizando e expondo *exatamente* as interfaces definidas no Contexto Arquitetural.
2.  **Código Limpo e Legível (PEP 8):** Seguir rigorosamente o PEP 8. Priorizar clareza e simplicidade (KISS).
3.  **Modularidade e Coesão (SRP):** Criar funções e classes com responsabilidades únicas e bem definidas.
4.  **Type Hints (PEP 484):** Utilizar type hints completos e precisos.
5.  **Tratamento de Erros Robusto:** Antecipar e tratar erros potenciais conforme especificado. Usar exceções específicas.
6.  **Segurança Básica:** Validar inputs, evitar práticas inseguras.
7.  **Documentação (Docstrings PEP 257):** Escrever docstrings claras e completas, referenciando contratos de interface.
8.  **Sem Código Morto/Desnecessário:** Implementar apenas o necessário.
9.  **Testes Unitários:** **OBRIGATÓRIO:** Gerar testes unitários (usando `[NOME_DO_FRAMEWORK_DE_TESTE - Ex: pytest, unittest]`) para as funções/métodos públicos. Os testes devem:
    *   Cobrir casos de sucesso, erro e borda mencionados na Especificação.
    *   **Utilizar mocks/stubs para simular as "Interfaces de Dependências"** (não chamar o código real de outros módulos).
    *   Verificar se os "Outputs Esperados" estão corretos.
    *   Colocar os testes em `tests/unit/[caminho_correspondente]/test_[nome_do_modulo].py`.
10. **Eficiência (Consideração):** Escrever código razoavelmente eficiente, sem otimização prematura.
11. **Contexto Essencial:** **NOVO/IMPORTANTE:** Para implementar esta funcionalidade corretamente, você **precisará conhecer as definições exatas** dos arquivos/módulos listados na seção **"Dependências Diretas"** acima. Ao executar (ex: no Cursor/Augment), certifique-se de fornecer o conteúdo desses arquivos como contexto (ex: usando `@path/to/dependency.py`).

**Resultado Esperado:**

1.  **Código Python Completo:** O conteúdo final do arquivo `[NOME_DO_ARQUIVO_A_SER_CRIADO_OU_MODIFICADO.py]`.
2.  **Código de Testes Unitários:** O conteúdo do arquivo de teste correspondente com testes unitários usando mocks.
3.  **(Opcional) Breve Relatório:** Explicação de decisões, desafios ou sugestões.