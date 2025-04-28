```markdown
# README: Prompt_Tocrisna_Architecture_v1.0.md

## 1. Propósito Principal

Este prompt modelo foi projetado para guiar uma LLM (atuando como a agente "Tocrisna") na tarefa de **definir e documentar uma proposta de arquitetura técnica de alto nível** para um novo projeto de software. O foco é estabelecer uma estrutura sólida, modular, manutenível e alinhada com boas práticas desde o início, com ênfase na definição clara dos componentes principais e, crucialmente, das **interfaces de comunicação (contratos)** entre eles.

## 2. Agente AGV Associado

*   **Tocrisna** (Arquiteta)

## 3. Fase do Fluxo AGV

*   Este é o prompt central da **Fase 2 (Arquitetura Técnica)** do fluxo AGV. Ele é utilizado logo após a Fase 1 (Definição e Preparação), onde a visão do produto e a stack tecnológica são definidas.

## 4. Inputs Chave Necessários (Placeholders a Preencher no Prompt)

O usuário deve preencher a seção "Contexto e Definições Iniciais do Projeto" no arquivo `Prompt_Tocrisna_Architecture_v1.0.md` com informações da Fase 1:

*   `[NOME_DO_PROJETO]`: Nome oficial do projeto.
*   `[DESCRIÇÃO CLARA DO PROPÓSITO GERAL DO SOFTWARE...]`: A visão do produto.
*   `[LISTA (BULLET POINTS) DAS PRINCIPAIS CAPACIDADES...]`: Funcionalidades chave em alto nível.
*   `[QUEM USARÁ O SOFTWARE E EM QUE CONTEXTO?]`: Público alvo e ambiente.
*   `[Stack Tecnológica Definida]`: Linguagem, frameworks, bibliotecas, BD, etc.
*   `[Requisitos Não Funcionais Iniciais]`: Expectativas de performance, escalabilidade, segurança, etc. (Opcional, mas útil).
*   `[Principais Restrições]`: Limitações conhecidas (Opcional).

## 5. Outputs Esperados da LLM

A execução bem-sucedida deste prompt deve gerar um **Blueprint Arquitetural Detalhado**, preferencialmente em Markdown, contendo no mínimo:

1.  **Visão Geral da Arquitetura:** Abordagem escolhida (ex: Camadas, Microserviços) e justificativa.
2.  **Diagrama de Componentes (Simplificado):** Representação visual ou textual dos módulos principais e suas conexões.
3.  **Descrição dos Componentes/Módulos:** Nome, responsabilidade e tecnologias chave para cada componente.
4.  **Definição das Interfaces Principais:** Detalhamento crucial dos contratos entre componentes (assinaturas, estruturas de dados, propósito).
5.  **Gerenciamento de Dados:** Como os dados serão tratados.
6.  **Estrutura de Diretórios Proposta:** Sugestão inicial de organização de pastas.
7.  **Considerações de Segurança:** Princípios aplicados no design.
8.  **Justificativas e Trade-offs:** Explicação das decisões chave.

## 6. Diretrizes e Princípios AGV Enfatizados

Este prompt instrui a LLM a priorizar:

*   **Modularidade e SRP:** Divisão clara de responsabilidades.
*   **Baixo Acoplamento e Alta Coesão:** Módulos independentes, mas internamente focados.
*   **Interfaces Explícitas:** A definição clara de contratos é uma diretriz CRÍTICA deste prompt e central para o princípio AGV de Integração Incremental (ver `docs/principios_chave_agv.md`).
*   **Clareza, Manutenibilidade e Testabilidade:** A arquitetura deve ser compreensível e facilitar o desenvolvimento e testes futuros.
*   **Segurança Fundamental:** Incorporar considerações básicas de segurança no design.
*   **Aderência à Stack e Padrões:** Usar a stack definida e aplicar padrões de design relevantes com justificativa.

## 7. Notas de Uso e Otimização

*   Este é um dos prompts mais críticos do fluxo AGV. A qualidade do Blueprint Arquitetural gerado impactará todas as fases subsequentes.
*   **Validação Humana é Essencial:** Revise *cuidadosamente* a arquitetura proposta pela IA. Ela faz sentido para o seu projeto? As interfaces estão claras e completas? Os trade-offs são aceitáveis? Não hesite em iterar, ajustando o prompt ou pedindo clarificações/alternativas à IA até que a arquitetura seja aprovada.
*   Quanto mais claros e detalhados forem os inputs da Fase 1 (visão, funcionalidades, requisitos não funcionais), melhor será a arquitetura gerada.

```