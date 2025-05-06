# AGV Prompt Template: ValidadorCruzado v1.0 - Validação de Preenchimento de Prompt

**Tarefa Principal:** Validar a precisão e completude do prompt AGV preenchido (`[NOME_DO_ARQUIVO_PROMPT_PREENCHIDO.md]`) em relação aos seus documentos fonte originais (`[LISTAR_ARQUIVOS_FONTE_USADOS_PELO_PREENCHEDOR.md]`).

**Contexto:** Uma IA ("Preenchedor") foi usada para preencher um template de prompt AGV (`[NOME_DO_ARQUIVO_TEMPLATE_ORIGINAL.md]`) usando os documentos fonte listados. Sua tarefa é atuar como um revisor independente para garantir que o preenchimento foi feito corretamente, sem omissões, alucinações ou interpretações errôneas.

**Arquivos para Análise:**

1.  **Prompt Preenchido (a ser validado):**
    ```markdown
    # --- Conteúdo de [NOME_DO_ARQUIVO_PROMPT_PREENCHIDO.md] ---
    [COLE AQUI O CONTEÚDO COMPLETO DO PROMPT PREENCHIDO PELA IA PREENCHEDORA]
    ```

2.  **Template Original (para referência da estrutura):**
    ```markdown
    # --- Conteúdo de [NOME_DO_ARQUIVO_TEMPLATE_ORIGINAL.md] ---
    [COLE AQUI O CONTEÚDO DO TEMPLATE VAZIO QUE FOI USADO, Ex: Prompt_Severino_v1.1.md]
    ```

3.  **Documentos Fonte (usados para preencher):**
    ```markdown
    # --- Conteúdo de [ARQUIVO_FONTE_1.md] (Ex: Output_Tocrisna_Blueprint.md) ---
    [COLE AQUI O CONTEÚDO DO PRIMEIRO DOCUMENTO FONTE]

    # --- Conteúdo de [ARQUIVO_FONTE_2.md] (Ex: Veredito_Stack.md) ---
    [COLE AQUI O CONTEÚDO DO SEGUNDO DOCUMENTO FONTE, SE HOUVER]

    # --- [Adicionar mais fontes conforme necessário] ---
    ```

**Instruções Detalhadas para Validação:**

1.  **Comparação Seção por Seção:** Para cada seção preenchida no `Prompt Preenchido`, compare seu conteúdo com as informações correspondentes nos `Documentos Fonte`.
2.  **Identificar Discrepâncias:** Aponte *qualquer* diferença, incluindo:
    *   **Informação Incorreta:** Dados no prompt preenchido que contradizem a fonte.
    *   **Informação Omitida:** Dados relevantes da fonte que *deveriam* estar no prompt preenchido, mas não estão.
    *   **Alucinação/Invenção:** Informações presentes no prompt preenchido que *não* têm base nos documentos fonte.
    *   **Interpretação Errada:** Informação da fonte que foi distorcida ou mal aplicada no prompt preenchido.
3.  **Verificar Completude:** Certifique-se de que *todos* os placeholders relevantes do `Template Original` foram adequadamente preenchidos no `Prompt Preenchido`.
4.  **Validação Estrutural (Mapeamento Fonte -> Destino):** Para cada seção principal preenchida no `Prompt Preenchido`, tente identificar e declarar *qual documento fonte* (e, se possível, qual parte dele) foi usado para preencher aquela seção específica. Isso ajuda a verificar se o Preenchedor usou as fontes corretas para cada parte.
5.  **Consistência Geral:** Avalie se o prompt preenchido como um todo faz sentido lógico e está internamente consistente.

**Resultado Esperado:**

Um **Relatório de Validação Detalhado** em Markdown, contendo:

1.  **Resumo Geral:** Uma avaliação sucinta (ex: "Preenchimento correto", "Preenchimento com pequenas inconsistências", "Preenchimento com erros significativos").
2.  **Lista de Achados (Discrepâncias e Confirmações):**
    *   Para cada discrepância encontrada (incorreção, omissão, alucinação, interpretação errada):
        *   Indique a seção do `Prompt Preenchido` afetada.
        *   Descreva o problema específico.
        *   Referencie a informação correta/faltante no `Documento Fonte`.
    *   Mencione seções importantes que foram preenchidas *corretamente*.
3.  **Relatório de Validação Estrutural (Mapeamento):**
    *   Liste as seções principais do `Prompt Preenchido` e indique a fonte provável para cada uma. (Ex: "Seção 'Dependências Diretas' preenchida com base na Seção 3.X do `Output_Tocrisna_Blueprint.md`").
4.  **Recomendação:** Indique se o `Prompt Preenchido` está pronto para ser usado na próxima fase do AGV ou se precisa de correções (e quais).