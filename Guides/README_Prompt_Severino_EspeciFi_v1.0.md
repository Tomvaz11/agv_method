```markdown
# README: Prompt_Severino_EspeciFi_v1.0.md

## 1. Propósito Principal

Este prompt modelo foi projetado para guiar uma LLM (atuando como o agente "Severino") na tarefa de **traduzir uma descrição de alto nível de uma funcionalidade ou módulo específico em uma especificação técnica detalhada**. Ele serve como uma ponte crucial entre a visão funcional do coordenador humano e as instruções precisas necessárias para o agente de implementação (Tocle), garantindo que a implementação esteja alinhada com a arquitetura previamente definida.

## 2. Agente AGV Associado

*   **Severino** (Especificador Funcional)

## 3. Fase do Fluxo AGV

*   Este prompt opera na **Fase 2.5 (Especificação Funcional Detalhada)** do fluxo AGV. Ele é utilizado após a arquitetura ter sido definida e aprovada (Fase 2 - Tocrisna) e *antes* da implementação do código (Fase 3 - Tocle). Ele é tipicamente executado para cada funcionalidade ou módulo principal a ser desenvolvido.

## 4. Inputs Chave Necessários (Placeholders a Preencher no Prompt)

O usuário deve preencher as seguintes seções no arquivo `Prompt_Severino_EspeciFi_v1.0.md`:

*   `[NOME_DO_PROJETO]`: Nome do projeto.
*   `[BREVE DESCRIÇÃO DO PROPÓSITO GERAL DO PROJETO]`: Contexto geral.
*   **Blueprint Arquitetural Relevante:** Esta seção é **fundamental** e deve ser preenchida com as informações relevantes extraídas do output da Tocrisna (Fase 2), incluindo:
    *   `[CAMINHO/COMPLETO/DO/ARQUIVO_ALVO.py]`: Onde esta funcionalidade será implementada.
    *   `[COPIAR DESCRIÇÃO DA RESPONSABILIDADE DA ARQUITETURA]`: O papel deste módulo conforme a arquitetura.
    *   `[COPIAR AS INTERFACES RELEVANTES DO BLUEPRINT DA TOCRISNA - Dependências]`: Contratos que este módulo *usará*.
    *   `[COPIAR AS INTERFACES RELEVANTES DO BLUEPRINT DA TOCRISNA - Expostas]`: Contratos que este módulo *fornecerá*.
    *   `[COPIAR DEFINIÇÕES DE DATACLASSES/NAMEDTUPLES RELEVANTES...]`: Estruturas de dados pertinentes.
*   **Descrição de Alto Nível da Funcionalidade (Fornecida por Você):** A descrição em linguagem natural do *quê* a funcionalidade deve fazer.

## 5. Outputs Esperados da LLM

A execução bem-sucedida deste prompt deve gerar um **bloco de texto contendo a Especificação Técnica Detalhada** da funcionalidade. Este output é projetado para ser copiado e colado diretamente na seção correspondente do `Prompt_Tocle_Implementation_v1.0.md`. A especificação deve detalhar:

*   Inputs exatos para a funcionalidade/método principal.
*   Passos lógicos de processamento, incluindo *quando e como chamar as interfaces de dependência* definidas na arquitetura.
*   Outputs exatos ou efeitos colaterais esperados.
*   Aplicação das regras de negócio fornecidas.
*   Tratamento de erros e casos de borda relevantes.

## 6. Diretrizes e Princípios AGV Enfatizados

Este prompt guia a IA a:

*   **Traduzir Intenção:** Converter linguagem natural em passos técnicos acionáveis.
*   **Respeitar a Arquitetura:** Basear a especificação estritamente nas interfaces e responsabilidades definidas pela Tocrisna.
*   **Foco na Funcionalidade:** Detalhar o *comportamento* esperado, não a implementação de baixo nível (isso é tarefa do Tocle).
*   **Clareza e Precisão:** Gerar uma especificação inequívoca.
*   **Antecipar Necessidades:** Considerar tratamento de erros e casos de borda básicos.

## 7. Notas de Uso e Otimização

*   A qualidade da especificação gerada depende fortemente da clareza da sua descrição de alto nível e da precisão do contexto arquitetural fornecido.
*   **Validação Humana é Importante:** Revise a especificação gerada pelo Severino. Ela realmente captura o fluxo e o comportamento que você pretendia? Faz sentido em relação à arquitetura? É crucial validar *antes* de passar para o Tocle, para evitar que ele implemente algo incorreto.
*   Pode ser necessário iterar com o Severino (ajustar a descrição de alto nível ou o prompt) para obter uma especificação satisfatória.

```