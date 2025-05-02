# AGV Prompt Template: PreenchedorGenerico v1.1 - Preenchimento Assistido de Prompt AGV

**Tarefa Principal:** Preencher de forma **cirúrgica e precisa** todos os campos/placeholders necessários no template de prompt AGV fornecido (`[NOME_DO_ARQUIVO_TEMPLATE_ALVO.md]`), utilizando **exclusivamente** as informações contidas nos documentos fonte listados (`[LISTAR_ARQUIVOS_FONTE.md]`).

**Instruções Detalhadas:**

1.  **Análise das Fontes:** Estude cuidadosamente o conteúdo de todos os `[LISTAR_ARQUIVOS_FONTE.md]` para extrair as informações relevantes.
2.  **Análise do Template Alvo:** Identifique todos os placeholders (ex: `[PLACEHOLDER]`) e seções que precisam ser preenchidas no `[NOME_DO_ARQUIVO_TEMPLATE_ALVO.md]`.
3.  **Preenchimento Preciso:** Substitua cada placeholder no template alvo pela informação correspondente encontrada **exatamente** nos documentos fonte.
    *   **NÃO invente informações.** Se uma informação específica para um placeholder não for encontrada nas fontes, deixe o placeholder como está ou indique explicitamente `[INFORMAÇÃO NÃO ENCONTRADA NAS FONTES]`.
    *   **Use apenas as fontes fornecidas.** Não consulte fontes externas ou conhecimento prévio.
4.  **Formatação:** Mantenha a estrutura e formatação Markdown original do template alvo.

**Arquivos de Referência:**

1.  **Template Alvo (a ser preenchido):**
    ```markdown
    # --- Conteúdo de [NOME_DO_ARQUIVO_TEMPLATE_ALVO.md] ---
    [COLE AQUI O CONTEÚDO DO TEMPLATE VAZIO, Ex: Prompt_Severino_v1.1.md]
    ```

2.  **Documentos Fonte (para consulta):**
    ```markdown
    # --- Conteúdo de [ARQUIVO_FONTE_1.md] (Ex: Output_Tocrisna_Blueprint.md) ---
    [COLE AQUI O CONTEÚDO DO PRIMEIRO DOCUMENTO FONTE]

    # --- Conteúdo de [ARQUIVO_FONTE_2.md] (Ex: Veredito_Stack.md) ---
    [COLE AQUI O CONTEÚDO DO SEGUNDO DOCUMENTO FONTE, SE HOUVER]

    # --- [Adicionar mais fontes conforme necessário] ---
    ```

**Resultado Esperado:**

1.  **Prompt Preenchido Completo:** O conteúdo completo do `[NOME_DO_ARQUIVO_TEMPLATE_ALVO.md]` com todos os placeholders possíveis preenchidos com base nas fontes, formatado em Markdown e pronto para uso.
2.  **Relatório de Preenchimento (Validação Estrutural):** Uma breve seção ao final do output (ou como comentário) detalhando como as seções principais foram preenchidas:
    *   Liste cada seção principal preenchida.
    *   Indique qual(is) `Documento(s) Fonte` foi(ram) usado(s) para preencher aquela seção.
    *   Mencione quaisquer placeholders que não puderam ser preenchidos por falta de informação nas fontes.
    *   **Exemplo de Relatório de Preenchimento:**
        ```
        ---
        **Relatório de Preenchimento:**
        *   Seção 'Contexto Arquitetural > Dependências Diretas': Preenchida usando a Seção 3.1 do `Output_Tocrisna_Blueprint.md`.
        *   Seção 'Contexto Arquitetural > Interfaces de Dependências': Preenchida usando a Seção 4 do `Output_Tocrisna_Blueprint.md`.
        *   Seção 'Stack Tecnológica': Preenchida usando `Veredito_Stack.md`.
        *   Placeholder `[NOME_DO_PROJETO]`: Preenchido usando `Output_Tocrisna_Blueprint.md`.
        *   Placeholder `[PLACEHOLDER_EXEMPLO_NAO_ENCONTRADO]`: Informação não encontrada nas fontes fornecidas.
        ---
        ```