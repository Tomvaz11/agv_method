```markdown
# README: Prompt_Tolete_Refatoracao_v1.0.md

## 1. Propósito Principal

Este prompt modelo foi projetado para guiar uma LLM (atuando como o agente "Tolete") na tarefa de **refatorar código Python existente**. O objetivo principal é melhorar significativamente a qualidade interna do código – como legibilidade, manutenibilidade, robustez, e aderência a boas práticas – **preservando estritamente o comportamento externo observável** do código original. Não deve ser usado para adicionar novas funcionalidades ou corrigir bugs lógicos (a menos que a correção seja um efeito colateral de uma refatoração clara, como remover código morto).

## 2. Agente AGV Associado

*   **Tolete** (Refatorador)

## 3. Fase do Fluxo AGV

*   Este prompt é tipicamente utilizado na **Fase 4 (Revisão & Teste)** do fluxo principal do AGV, após a implementação inicial pelo Tocle, ou na **Fase 5 (Manutenção & Evolução)**, para melhorar código legado ou código que decaiu em qualidade ao longo do tempo.

## 4. Inputs Chave Necessários (Placeholders a Preencher no Prompt)

O usuário deve preencher os seguintes placeholders no arquivo `Prompt_Tolete_Refatoracao_v1.0.md` antes de usá-lo:

*   `[NOME_DO_ARQUIVO_COM_EXTENSÃO]`: Nome completo do arquivo Python a ser refatorado.
*   `[NOME_DO_PROJETO]`: Nome do projeto para fornecer contexto geral.
*   `[BREVE DESCRIÇÃO DO PROPÓSITO GERAL DO PROJETO]`: Contexto funcional do projeto.
*   `[BREVE DESCRIÇÃO DA RESPONSABILIDADE ESPECÍFICA DESTE ARQUIVO]`: O papel deste arquivo dentro do projeto.
*   `[ESTRUTURA DE PASTAS RELEVANTE]`: Representação da estrutura de diretórios para dar contexto arquitetural e de localização.
*   `[CÓDIGO COMPLETO DO ARQUIVO]`: O código-fonte Python exato a ser processado.
*   **Importante:** A seção `[NOTA HISTÓRICA]` dentro do prompt deve ser **removida** antes de submeter à LLM para uso real. Ela serve apenas para documentação interna do motivo da Diretriz 14.

## 5. Outputs Esperados da LLM

A execução bem-sucedida deste prompt deve gerar:

1.  **Código Refatorado Completo:** O conteúdo integral e final do arquivo `.py` refatorado.
2.  **Relatório Detalhado de Alterações:** Uma explicação clara e justificada das modificações realizadas, vinculando cada mudança significativa a uma ou mais das "Diretrizes Específicas de Refatoração" presentes no prompt. Deve incluir justificativa explícita se alguma interface pública foi renomeada.

## 6. Diretrizes e Princípios AGV Enfatizados

Este prompt encapsula vários princípios chave do Método AGV, instruindo a LLM a focar em:

*   **Preservação Rigorosa da Funcionalidade Externa:** A diretriz mais crítica (Diretriz 1).
*   **Melhora da Qualidade Interna:** Aplicação de DRY, SRP, KISS (Diretrizes 2, 6, 12).
*   **Conformidade com Padrões:** PEP 8, Type Hints (PEP 484), Docstrings (PEP 257) (Diretrizes 7, 8, 11).
*   **Robustez:** Melhoria no tratamento de erros (Diretriz 9).
*   **Clareza e Legibilidade:** Nomenclatura, estrutura lógica, comentários adequados (Diretrizes 5, 4, 10).
*   **Estabilidade da API:** A Diretriz 14 instrui especificamente cautela ao renomear interfaces públicas para minimizar quebras em código dependente e testes, reforçando o princípio de baixo acoplamento (detalhado em `docs/principios_chave_agv.md`).

## 7. Notas de Uso e Otimização

*   Este prompt é mais eficaz quando aplicado a um código que já *funciona* mas cuja qualidade interna pode ser aprimorada.
*   Fornecer um contexto arquitetural preciso (estrutura de pastas) ajuda a IA a tomar melhores decisões sobre modularidade e potenciais extrações para módulos `utils`.
*   **Validação Humana é Crucial:** Sempre revise cuidadosamente o código refatorado e o relatório. Execute a suíte de testes completa associada ao código refatorado para verificar empiricamente que nenhuma regressão funcional foi introduzida.

```