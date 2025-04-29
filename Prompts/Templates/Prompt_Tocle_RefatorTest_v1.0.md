Este prompt foca em melhorar a qualidade dos testes existentes ou atualizá-los para refletir mudanças no código de produção.

```markdown
# AGV Prompt Template: Tocle v1.0 - Refatoração e Atualização de Testes

**Tarefa Principal:** Refatorar e/ou atualizar o(s) arquivo(s) de teste Python (`[NOME_DO_ARQUIVO_DE_TESTE(S).py]`) fornecido(s) abaixo, considerando as mudanças recentes no código de produção associado e aplicando as melhores práticas para testes.

**Contexto do Projeto:**

*   **Nome do Projeto:** `[NOME_DO_PROJETO]`
*   **Objetivo Geral do Projeto:** `[BREVE DESCRIÇÃO DO PROPÓSITO GERAL DO PROJETO]`
*   **Framework de Teste Utilizado:** `[Ex: pytest, unittest]`
*   **Módulo/Arquivo de Produção Associado:** `[CAMINHO/DO/ARQUIVO/DE_PRODUCAO_TESTADO.py]`
*   **Resumo das Mudanças Recentes no Código de Produção (se aplicável):**
    ```
    [DESCRIÇÃO CONCISA DAS ALTERAÇÕES FEITAS NO CÓDIGO DE PRODUÇÃO QUE MOTIVAM A ATUALIZAÇÃO DOS TESTES.
    Ex: "A função `calcular_preco` agora aceita um argumento opcional `discount_code: str`."
    Ex: "A classe `UserRepo` foi refatorada para usar injeção de dependência para a conexão com o banco de dados."
    Ex: "O método `process_file` agora levanta uma exceção `InvalidFormatError` específica em vez de `ValueError`."]
    [Se for apenas refatoração do teste sem mudança no código de produção, indicar: "Refatoração interna dos testes para melhorar clareza/DRY."]
    ```
*   **Estrutura Relevante do Projeto (Opcional, se ajudar):**
    ```
    [COLE AQUI A ESTRUTURA DE PASTAS RELEVANTE, DESTACANDO ARQUIVOS DE TESTE E PRODUÇÃO]
    ```

**Arquivo(s) de Teste a ser(em) Refatorado(s)/Atualizado(s):**

```python
# --- [NOME_DO_ARQUIVO_DE_TESTE_1.py] ---
# COLE AQUI O CÓDIGO COMPLETO DO PRIMEIRO ARQUIVO DE TESTE
# ... seu código de teste aqui ...

# --- [NOME_DO_ARQUIVO_DE_TESTE_2.py (se houver mais de um)] ---
# COLE AQUI O CÓDIGO COMPLETO DO SEGUNDO ARQUIVO DE TESTE
# ... seu código de teste aqui ...
```

**Código de Produção Relevante (Opcional - Fornecer se for útil para a IA entender as mudanças):**

```python
# COLE AQUI TRECHOS RELEVANTES DO CÓDIGO DE PRODUCAO ALTERADO OU A SER TESTADO
# ... código de produção relevante ...
```

**Objetivos Gerais da Refatoração/Atualização dos Testes:**

O objetivo é garantir que os testes sejam claros, eficazes, fáceis de manter, robustos e **corretamente alinhados com o comportamento atual** do código de produção.

**Diretrizes Específicas para Testes:**

1.  **Alinhamento com Código de Produção:** **CRÍTICO:** Atualizar os testes (assinaturas de chamadas, asserções, mocks) para refletir precisamente quaisquer mudanças nas interfaces ou no comportamento do código de produção descrito. Testes devem falhar se o código de produção estiver incorreto e passar se estiver correto.
2.  **Clareza da Intenção:** Cada teste deve ter um propósito claro e testar **uma coisa específica** (ou um fluxo muito bem definido). Nomes de funções de teste devem ser descritivos (ex: `test_calcula_preco_com_desconto_valido`, `test_process_file_levanta_InvalidFormatError_para_extensao_ruim`).
3.  **Clareza das Asserções:** Use asserções específicas e informativas do framework de teste (ex: `assertEqual`, `assertTrue`, `assertRaises`). Evite asserções genéricas ou complexas demais. Verifique não apenas o valor de retorno, mas também efeitos colaterais esperados (se aplicável e testável com mocks).
4.  **Isolamento (Testes Unitários):** Garanta que os testes unitários **não tenham dependências externas reais** (rede, banco de dados, sistema de arquivos). Use **mocks, stubs ou fakes** de forma eficaz para isolar o código sob teste. Refatore para melhorar o uso de mocks se necessário.
5.  **DRY (Don't Repeat Yourself) em Testes:** Identifique e refatore código repetido nos testes, especialmente em seções de setup (arrange). Utilize fixtures (`pytest`) ou métodos `setUp/tearDown` (`unittest`) de forma apropriada para compartilhar setup comum.
6.  **Manutenibilidade:** Organize os testes de forma lógica. Evite testes excessivamente longos ou complexos. Dados de teste devem ser claros e relevantes para o caso testado.
7.  **Remover Testes Mortos/Redundantes:** Elimine testes que se tornaram obsoletos devido a mudanças no código de produção ou que testam exatamente a mesma coisa que outro teste de forma menos eficaz.
8.  **Robustez do Teste:** Testes não devem ser "flaky" (falhar intermitentemente sem mudanças no código). Evite dependências de tempo (a menos que seja o objeto do teste) ou de ordem de execução.
9.  **PEP 8 e Type Hints:** Aplique PEP 8 ao código de teste. Adicionar type hints pode melhorar a clareza, embora possa ser menos crítico que no código de produção.
10. **Cobertura (Consideração):** Embora não seja solicitado gerar *novos* testes para aumentar a cobertura aqui (a menos que seja para cobrir código *alterado*), as refatorações não devem *diminuir* a cobertura existente de forma não intencional. Garanta que os caminhos críticos do código de produção alterado continuem sendo testados.

**Resultado Esperado:**

1.  **Código de Teste Atualizado/Refatorado:** A versão final e completa do(s) arquivo(s) de teste (`[NOME_DO_ARQUIVO_DE_TESTE(S).py]`) após a aplicação das diretrizes.
2.  **Relatório Detalhado de Alterações:**
    *   Um resumo das principais modificações realizadas nos testes.
    *   Uma lista das alterações significativas, explicando *o quê* foi mudado e *por quê* (ex: "Atualizada chamada no teste X para refletir nova assinatura da função Y (Diretriz 1)", "Refatorado setup dos testes A, B, C usando fixture `pytest` para seguir DRY (Diretriz 5)", "Melhorada asserção no teste Z para ser mais específica (Diretriz 3)", "Removido teste D por ser redundante com teste E (Diretriz 7)").

```