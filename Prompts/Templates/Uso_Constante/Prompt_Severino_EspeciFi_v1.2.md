# AGV Prompt Template: Severino v1.2 - Especificação Funcional Detalhada

**Tarefa Principal:** Detalhar a especificação técnica para a funcionalidade/módulo descrito na seção "Descrição de Alto Nível" abaixo, baseando-se estritamente no contexto arquitetural. **Adicionalmente**, identificar e listar possíveis funções auxiliares genéricas que poderiam ser movidas para `fotix.utils`. O resultado principal deve ser formatado para uso no prompt do Tocle.

**Contexto do Projeto e Arquitetura (Definido por Fases Anteriores):**

*   **Nome do Projeto:** `[NOME_DO_PROJETO]`
*   **Objetivo Geral do Projeto:** `[BREVE DESCRIÇÃO DO PROPÓSITO GERAL DO PROJETO]`
*   **Blueprint Arquitetural Relevante (Extraído do Output da Tocrisna):**
    *   **Módulo/Arquivo Alvo desta Especificação:** `[CAMINHO/COMPLETO/DO/ARQUIVO_ALVO.py]`
    *   **Principais Responsabilidades deste Módulo/Arquivo (Conforme Arquitetura):** `[COPIAR DESCRIÇÃO DA RESPONSABILIDADE DO BLUEPRINT]`
    *   **Dependências Diretas deste Módulo (Conforme Arquitetura):**
        *   `[COPIAR A LISTA EXPLÍCITA DE DEPENDÊNCIAS DIRETAS DO BLUEPRINT. Ex:]`
        *   `fotix.domain.models`
        *   `utils.helpers`
    *   **Interfaces de Dependências (Contratos a serem Usados por este Módulo):**
        *   `[COPIAR AS INTERFACES RELEVANTES DO BLUEPRINT - Assinaturas e descrições das funções/métodos de outros módulos que este precisa chamar. Ex:]`
        *   `utils.helpers.calcular_hash(file_path: Path) -> str`
        *   `core.database.UserRepository.get_user_by_id(user_id: int) -> Optional[User]`
    *   **Interfaces Expostas (Contratos Fornecidos por este Módulo):**
        *   `[COPIAR AS INTERFACES RELEVANTES DO BLUEPRINT - Assinaturas e descrições das funções/métodos públicos que este módulo deve expor. Ex:]`
        *   `Classe 'DuplicateDetector' com método público 'find_duplicates(directory_path: Path) -> Dict[str, List[Path]]'`
    *   **Estruturas de Dados Relevantes (Definidas pela Arquitetura):** `[COPIAR DEFINIÇÕES DE DATACLASSES/NAMEDTUPLES RELEVANTES DO BLUEPRINT]`

**Descrição de Alto Nível da Funcionalidade (Gerada com RequirementHelper):** **<<< INPUT GERADO VIA REQUIREMENT HELPER >>>**

[COLE AQUI O OUTPUT DO REQUIREMENTHELPER VALIDADO POR VOCÊ]

**Diretrizes para Geração da Especificação:**

1.  **Base na Descrição de Alto Nível:** Implementar fielmente a funcionalidade descrita.
2.  **Clareza e Precisão:** Especificação inequívoca.
3.  **Detalhamento:** Descrever passos lógicos.
4.  **Referência às Interfaces:** Referenciar explicitamente as interfaces do Contexto Arquitetural.
5.  **Inputs e Outputs:** Detalhar claramente.
6.  **Regras de Negócio:** Incorporar regras.
7.  **Tratamento de Erros:** Especificar cenários e tratamento.
8.  **Casos de Borda:** Mencionar casos óbvios.
9.  **Formato Adequado:** Linguagem clara, listas. Adequado para colar no `Prompt_Tocle`.
10. **Sugestão para `fotix.utils` (NOVO):** Durante a descrição dos passos lógicos (Diretriz 3), se identificar operações ou cálculos que são genéricos, reutilizáveis e não específicos da lógica principal deste módulo, liste-os separadamente como candidatos para `fotix.utils`. Para cada candidato, sugira um nome de função e descreva brevemente seu propósito.

**Resultado Esperado:**

1.  **Especificação Técnica Detalhada:** Um bloco de texto contendo a especificação principal da funcionalidade, pronta para ser usada no prompt do Tocle (detalhando inputs, passos lógicos, outputs, regras, erros, bordas).
2.  **Sugestões para `fotix.utils` (se houver):** Uma seção separada (ex: `## Sugestões para fotix.utils`) listando as funções auxiliares candidatas identificadas na Diretriz 10.
    *   *Exemplo:*
        ```
        ## Sugestões para fotix.utils:
        *   `format_filesize(size_in_bytes: int) -> str`: Converte bytes para uma string legível (KB, MB, GB). Útil para exibição na GUI.
        *   `is_valid_image_extension(filename: str) -> bool`: Verifica se a extensão do arquivo corresponde a formatos de imagem suportados.
        ```