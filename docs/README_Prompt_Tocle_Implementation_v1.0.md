```markdown
# README: Prompt_Tocle_Implementation_v1.0.md

## 1. Propósito Principal

Este prompt modelo foi projetado para guiar uma LLM (atuando como o agente "Tocle") na tarefa de **implementar código Python funcional para uma nova feature ou módulo**, seguindo rigorosamente uma especificação técnica detalhada e um contexto arquitetural pré-definido. Além do código de produção, o prompt também exige a geração de **testes unitários básicos** para a funcionalidade implementada, garantindo qualidade e testabilidade desde o início.

## 2. Agente AGV Associado

*   **Tocle** (Engenheiro)

## 3. Fase do Fluxo AGV

*   Este é o prompt central da **Fase 3 (Implementação e Teste Unitário)** do fluxo AGV. Ele é utilizado após a arquitetura ter sido definida (Fase 2 - Tocrisna) e a funcionalidade específica ter sido detalhada (Fase 2.5 - Severino).

## 4. Inputs Chave Necessários (Placeholders a Preencher no Prompt)

O usuário deve preencher cuidadosamente as seguintes seções no arquivo `Prompt_Tocle_Implementation_v1.0.md`:

*   `[NOME_DO_ARQUIVO_A_SER_CRIADO_OU_MODIFICADO.py]`: O nome do arquivo onde o código será implementado.
*   `[NOME_DO_PROJETO]`: Nome do projeto.
*   `[BREVE DESCRIÇÃO DO PROPÓSITO GERAL DO PROJETO]`: Contexto geral.
*   **Contexto Arquitetural (Definido por Tocrisna / Fase Anterior):** Esta seção é **vital** e deve ser preenchida com as informações relevantes do Blueprint Arquitetural, incluindo:
    *   Localização e responsabilidades do módulo/arquivo.
    *   **Interfaces de Dependências (Contratos a serem Usados):** Assinaturas/descrições exatas que o Tocle deve chamar.
    *   **Interfaces Expostas (Contratos a serem Fornecidos):** Assinaturas/descrições exatas que o Tocle deve implementar.
    *   Padrões de design e estruturas de dados relevantes.
*   **Especificação da Funcionalidade/Módulo a ser Implementada:** Esta seção deve ser preenchida com o **output detalhado gerado pelo Severino (Fase 2.5)** e validado por você. Contém os passos lógicos, regras, inputs/outputs.
*   `[Stack Tecnológica Permitida]`: Linguagem, versão, libs essenciais.
*   `[NOME_DO_FRAMEWORK_DE_TESTE]`: Framework a ser usado para os testes unitários (ex: pytest, unittest).

## 5. Outputs Esperados da LLM

A execução bem-sucedida deste prompt deve gerar:

1.  **Código Python Completo:** O conteúdo final do arquivo `.py` com a funcionalidade implementada conforme a especificação e arquitetura.
2.  **Código de Testes Unitários:** O conteúdo do arquivo `test_*.py` correspondente, contendo testes que cobrem a funcionalidade básica e utilizam **mocks/stubs** para isolar o código das dependências externas (conforme interfaces fornecidas).
3.  **(Opcional) Breve Relatório:** Explicações sobre a implementação, se necessário.

## 6. Diretrizes e Princípios AGV Enfatizados

Este prompt reforça múltiplos princípios AGV, instruindo a LLM a:

*   **Seguir a Arquitetura e Especificação:** Aderência estrita às interfaces e à funcionalidade detalhada (Diretriz 1).
*   **Código de Alta Qualidade:** PEP 8, Clareza, KISS, SRP, Type Hints, Docstrings (Diretrizes 2, 3, 4, 7).
*   **Robustez:** Tratamento de erros adequado (Diretriz 5).
*   **Segurança Básica:** Validação de inputs e práticas seguras (Diretriz 6).
*   **Testabilidade:** Geração **obrigatória** de testes unitários que **usam mocks** para dependências, alinhado com a Integração Incremental (Diretriz 9 e `docs/principios_chave_agv.md`).
*   **Eficiência Razoável:** Evitar código obviamente ineficiente (Diretriz 10).

## 7. Notas de Uso e Otimização

*   A qualidade do código gerado depende diretamente da clareza e precisão dos inputs (arquitetura da Tocrisna e especificação do Severino). "Garbage in, garbage out" aplica-se aqui.
*   **Revisão Humana Essencial:** Revise o código de produção E os testes unitários gerados. Os testes passam? Eles realmente testam os cenários corretos? Os mocks estão sendo usados adequadamente?
*   Pode ser necessário iterar com o Tocle, fornecendo feedback ou pedindo ajustes no código ou nos testes.
*   Execute os testes unitários no seu ambiente local para confirmar que eles passam e funcionam como esperado.
*   Lembre-se de executar testes de integração separadamente (conforme definido no fluxo AGV) após implementar módulos que interagem.

```