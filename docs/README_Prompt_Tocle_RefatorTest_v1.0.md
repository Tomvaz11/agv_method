```markdown
# README: Prompt_Tocle_RefatorTest_v1.0.md

## 1. Propósito Principal

Este prompt modelo foi projetado para guiar uma LLM (atuando como o agente "Tocle" com o "chapéu" de testador) na tarefa de **refatorar e/ou atualizar código de teste Python existente**. Os objetivos principais são:
1.  **Alinhar** os testes com quaisquer mudanças recentes ocorridas no código de produção associado (interfaces, comportamento, tratamento de erros).
2.  **Melhorar** a qualidade interna dos próprios testes (clareza, manutenibilidade, robustez, aderência a boas práticas de teste).

## 2. Agente AGV Associado

*   **Tocle** (Engenheiro) - Responsável pela qualidade e manutenção dos testes associados ao código que ele (ou Tolete) modifica.

## 3. Fase do Fluxo AGV

*   Este prompt é utilizado principalmente na **Fase 4 (Revisão & Teste)**, após o código de produção ter sido modificado (seja por implementação do Tocle ou refatoração do Tolete), ou na **Fase 5 (Manutenção & Evolução)** para melhorar a qualidade de suítes de teste existentes.

## 4. Inputs Chave Necessários (Placeholders a Preencher no Prompt)

O usuário deve preencher as seguintes seções no arquivo `Prompt_Tocle_RefatorTest_v1.0.md`:

*   `[NOME_DO_ARQUIVO_DE_TESTE(S).py]`: Nome(s) completo(s) do(s) arquivo(s) de teste a serem processados.
*   `[NOME_DO_PROJETO]`: Nome do projeto.
*   `[BREVE DESCRIÇÃO DO PROPÓSITO GERAL DO PROJETO]`: Contexto geral.
*   `[NOME_DO_FRAMEWORK_DE_TESTE]`: Framework utilizado (ex: pytest, unittest).
*   `[CAMINHO/DO/ARQUIVO/DE_PRODUCAO_TESTADO.py]`: Identificação do código que está sendo testado.
*   **`[Resumo das Mudanças Recentes no Código de Produção]`:** **CRUCIAL** se o objetivo for atualizar os testes. Descrever claramente o que mudou no código de produção. Se for apenas refatoração interna dos testes, indicar isso.
*   `[ESTRUTURA DE PASTAS RELEVANTE]`: Opcional, se ajudar a entender a localização.
*   `[CÓDIGO COMPLETO DO(S) ARQUIVO(S) DE TESTE]`: O código de teste atual a ser modificado.
*   `[CÓDIGO DE PRODUÇÃO RELEVANTE]`: Opcional, mas altamente recomendado fornecer trechos do código de produção *alterado* para que a IA entenda precisamente o que precisa ser refletido nos testes.

## 5. Outputs Esperados da LLM

A execução bem-sucedida deste prompt deve gerar:

1.  **Código de Teste Atualizado/Refatorado:** O conteúdo final e completo do(s) arquivo(s) de teste `.py` modificados.
2.  **Relatório Detalhado de Alterações:** Uma explicação clara das mudanças realizadas nos testes, justificadas pelas diretrizes do prompt (ex: atualização de chamada, melhoria de asserção, refatoração de setup).

## 6. Diretrizes e Princípios AGV Enfatizados

Este prompt foca em diretrizes específicas para testes, alinhadas com os princípios AGV:

*   **Alinhamento Teste-Código:** Garantir que os testes reflitam o estado *atual* do código de produção (Diretriz 1).
*   **Clareza e Intenção:** Testes devem ser fáceis de entender, com nomes e asserções descritivas (Diretrizes 2, 3).
*   **Isolamento (Unitário):** Uso correto de mocks/stubs para isolar o código sob teste (Diretriz 4), fundamental para a abordagem de Integração Incremental (ver `docs/principios_chave_agv.md`).
*   **Manutenibilidade do Teste:** Aplicação de DRY (especialmente em setups), organização lógica (Diretrizes 5, 6).
*   **Eficiência da Suíte:** Remover testes redundantes ou obsoletos (Diretriz 7).
*   **Robustez do Teste:** Evitar testes "flaky" (Diretriz 8).
*   **Qualidade Geral:** PEP 8, Type Hints (Diretriz 9).

## 7. Notas de Uso e Otimização

*   Use este prompt sempre que o código de produção coberto por testes for modificado.
*   Use-o também periodicamente para refatorar suítes de teste que se tornaram complexas ou repetitivas.
*   Fornecer um resumo claro das mudanças no código de produção é essencial para a tarefa de *atualização*.
*   Fornecer trechos do código de produção alterado pode melhorar significativamente a precisão da IA.
*   **Validação Humana e Execução:** Sempre revise o código de teste gerado e, **fundamentalmente, execute a suíte de testes** para garantir que os testes passam, falham quando deveriam, e que a cobertura não foi negativamente impactada de forma inesperada.

```