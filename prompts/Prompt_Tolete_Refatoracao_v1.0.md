```markdown
# AGV Prompt Template: Tolete v1.0 - Refatoração de Código

**Tarefa Principal:** Refatorar o arquivo de código Python (`[NOME_DO_ARQUIVO_COM_EXTENSÃO]`) fornecido abaixo.

**Contexto do Projeto:**

*   **Nome do Projeto:** `[NOME_DO_PROJETO]`
*   **Objetivo Geral do Projeto:** `[BREVE DESCRIÇÃO DO PROPÓSITO GERAL DO PROJETO - Ex: Ferramenta para encontrar e gerenciar fotos duplicadas]`
*   **Papel deste Arquivo no Projeto:** `[BREVE DESCRIÇÃO DA RESPONSABILIDADE ESPECÍFICA DESTE ARQUIVO - Ex: Implementa a cópia assíncrona de arquivos usando threads]`
*   **Estrutura Relevante do Projeto:**
    ```
    [COLE AQUI A ESTRUTURA DE PASTAS RELEVANTE, COM DESCRIÇÕES SE AJUDAR.
     Exemplo:
    photo_duplicate/
    ├── main.py                         # Ponto de entrada
    ├── core/
    │   ├── duplicate_detector.py       # Lógica de detecção
    │   └── async_file_copier.py        <-- Arquivo a ser refatorado
    ├── gui/
    │   └── main_window.py              # Interface gráfica
    └── utils/
        └── helpers.py                  # Funções utilitárias
    ...]
    ```

**Arquivo a ser Refatorado (`[NOME_DO_ARQUIVO_COM_EXTENSÃO]`):**

```python
# COLE AQUI O CÓDIGO COMPLETO DO ARQUIVO QUE VOCÊ QUER REFATORAR
# ... seu código python aqui ...
```

**Objetivos Gerais da Refatoração:**

O objetivo é melhorar a qualidade geral do código, tornando-o mais legível, manutenível, robusto e extensível, **sem alterar sua funcionalidade externa observável**.

**Diretrizes Específicas de Refatoração:**

1.  **Manter Funcionalidade Externa:** **CRÍTICO:** O comportamento observável do código (saídas para as mesmas entradas, efeitos colaterais esperados) deve permanecer **idêntico** após a refatoração.
2.  **Aplicar Princípio DRY (Don't Repeat Yourself):** Identifique e elimine a duplicação de código extraindo lógica repetida para funções, métodos ou classes reutilizáveis. Considere mover lógica genérica para módulos `utils` apropriados, se o contexto permitir.
3.  **Remover Código Morto/Desnecessário:** Exclua quaisquer variáveis, funções, classes, imports ou blocos de código que não são utilizados ou são inalcançáveis.
4.  **Simplificar Lógica Complexa:** Refatore condicionais aninhadas, loops complexos ou expressões booleanas complicadas para torná-los mais claros e diretos, mantendo a mesma lógica.
5.  **Melhorar Nomenclatura e Clareza:** Garanta que nomes de variáveis, funções, classes e módulos sejam descritivos, claros e consistentes, seguindo as convenções do PEP 8. (Veja também a Diretriz 14 sobre renomeação de interfaces públicas).
6.  **Aumentar a Modularidade e Coesão (SRP):**
    *   Garanta que classes e funções tenham uma única responsabilidade bem definida.
    *   Agrupe funcionalidades relacionadas (alta coesão).
    *   Reduza dependências desnecessárias entre diferentes partes do código (baixo acoplamento).
7.  **Seguir Diretrizes de Estilo (PEP 8):** Aplique rigorosamente as convenções de estilo do PEP 8 (indentação, espaços, limites de linha, etc.).
8.  **Type Hints (PEP 484):** Adicione ou melhore type hints para todas as funções, métodos e variáveis importantes para aumentar a clareza e permitir análise estática.
9.  **Melhorar Tratamento de Erros:**
    *   Use exceções específicas quando apropriado.
    *   Garanta que os erros sejam tratados de forma robusta ou propagados claramente.
    *   Utilize `try/except/finally` de forma eficaz, especialmente para liberar recursos.
10. **Melhorar Legibilidade Geral:** O código resultante deve ser significativamente mais fácil de ler e entender. Use comentários apenas onde necessário para explicar o *porquê*, não o *o quê*.
11. **Adicionar/Melhorar Docstrings (PEP 257):** Garanta que módulos, classes, funções e métodos públicos tenham docstrings claras e completas explicando propósito, argumentos (`Args`), retornos (`Returns`) e exceções levantadas (`Raises`).
12. **Considerar Princípios de Design (KISS):** Prefira soluções mais simples e diretas quando a complexidade não for justificada.
13. **Refatorações Pontuais e Justificadas:** Realize modificações direcionadas. Evite reescritas massivas desnecessárias. O foco é na melhoria incremental.
14. **Cuidado ao Renomear Interfaces Públicas:** **IMPORTANTE:** Evite renomear funções, métodos ou classes públicas a menos que o nome atual seja *significativamente* inadequado ou confuso. Priorize a manutenção da compatibilidade com testes existentes e outros módulos que possam depender desta interface. Se uma renomeação pública for *essencial* para clareza, justifique-a explicitamente no relatório de alterações. Renomear variáveis ou funções *internas* (com escopo local ou prefixadas com `_`) para melhorar a clareza é encorajado.

---
***[NOTA HISTÓRICA - REMOVER ANTES DE USAR O PROMPT EM PRODUÇÃO]***
*A Diretriz 14 foi adicionada com base em experiências anteriores onde a renomeação agressiva de interfaces públicas pela IA, embora tecnicamente melhorasse o nome localmente, causava quebras significativas em arquivos de teste e código dependente, exigindo esforço manual considerável para correção. Esta diretriz visa mitigar esse problema, equilibrando a melhoria da nomenclatura com a estabilidade da API pública do módulo.*
***[FIM DA NOTA HISTÓRICA]***
---

**Resultado Esperado:**

1.  **Código Refatorado Completo:** A versão final e completa do arquivo (`[NOME_DO_ARQUIVO_COM_EXTENSÃO]`) após a aplicação das diretrizes, pronta para ser usada.
2.  **Relatório Detalhado de Alterações:**
    *   Um resumo das principais melhorias realizadas.
    *   Uma lista das alterações significativas, explicando *o quê* foi mudado e *por quê*, fazendo referência às diretrizes acima (ex: "Extraída função `X` para seguir DRY (Diretriz 2)", "Adicionados type hints ao método `Y` (Diretriz 8)", "Simplificada condicional na linha Z (Diretriz 4)", "Renomeada variável interna `abc` para `xyz` para clareza (Diretriz 5)", "**Justificativa para renomear função pública Z (se aplicável - Diretriz 14)**").
    *   Mencione brevemente como princípios como SRP ou KISS foram aplicados.

```