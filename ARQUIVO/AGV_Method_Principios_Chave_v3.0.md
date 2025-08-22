# Princípios Chave do Método AGV v3.0 (Lean & Strategic)

Este documento descreve os princípios fundamentais de design, arquitetura e processo que norteiam o Método AGV, atualizados para refletir a filosofia "Lean & Strategic" validada no projeto Fotix.

## 1. Qualidade Intrínseca Como Fundamento

*   **Conceito:** O foco primário do Método AGV é guiar a IA para produzir software cujo código e arquitetura sejam de **qualidade profissional sênior**. A velocidade é um resultado da qualidade, não um objetivo que a substitui.
*   **Implicações:**
    *   Definição de uma arquitetura robusta e modular antes da implementação.
    *   Adesão rigorosa a boas práticas (SOLID, DRY, KISS).
    *   Geração de código claro, legível, bem documentado e com tratamento de erros robusto.
    *   Minimização de débito técnico desde o início.

## 2. Direção Estratégica vs. Microgerenciamento (NOVO)

*   **Conceito:** Este é o pilar da abordagem "Lean & Strategic". Em vez de fornecer prompts excessivamente detalhados que soletram cada passo, nós focamos em dar à IA uma direção clara e estratégica.
*   **Implicações:**
    *   **Confiança na Capacidade Latente da IA:** Partimos do pressuposto que LLMs de ponta já conhecem os padrões de codificação e design. Não precisamos ensiná-los, apenas guiá-los.
    *   **Foco no "O Quê", Não no "Como":** Nossos prompts se concentram em definir os **objetivos, requisitos e critérios de qualidade**. Damos à IA a autonomia para determinar a melhor forma de implementar a solução, desde que ela cumpra os critérios.
    *   **Redução da Carga Cognitiva:** Prompts mais enxutos reduzem a chance de a IA "esquecer" instruções ou "alucinar", resultando em outputs mais estáveis e de maior qualidade.

## 3. Fonte Única da Verdade - SSOT (NOVO)

*   **Conceito:** Para evitar conflitos de contexto e garantir a consistência, cada artefato principal do método possui uma responsabilidade única e é a autoridade máxima para um aspecto específico do projeto.
*   **Implicações:**
    *   O **Blueprint Arquitetural (F1)** é a fonte única da verdade para **toda a arquitetura**: estrutura de diretórios, responsabilidades dos componentes, interfaces e dependências.
    *   A **Ordem de Implementação (F2)** é a fonte única da verdade para a **sequência de trabalho**. Ela é uma "lista de tarefas" que aponta para o Blueprint, sem replicar informações de design.
    *   O **Implementador (F4)** usa a Ordem para saber *o que* fazer em seguida e o Blueprint para saber *como* construí-lo (quais dependências usar, qual interface implementar, etc.).

## 4. Integração Incremental via Interfaces Explícitas

*   **Conceito:** A conexão entre os módulos é definida *antecipadamente* através de interfaces (contratos) no Blueprint. A implementação ocorre de forma incremental, com os componentes sendo construídos para se encaixarem perfeitamente desde o início.
*   **Implicações:**
    *   Promove baixo acoplamento e alta coesão.
    *   Facilita a testabilidade, permitindo o uso de mocks/stubs para as dependências.
    *   Reduz drasticamente os riscos e a complexidade da fase de integração.

## 5. Validação Humana Crítica e Ciclo de Auditoria

*   **Conceito:** O Coordenador humano é a peça mais importante do processo. Nenhum output da IA é aceito sem escrutínio.
*   **Implicações:**
    *   **Validação Contínua:** O Coordenador valida o Blueprint, a Ordem de Implementação, cada implementação de módulo e cada suíte de testes.
    *   **Ciclo de Auditoria Explícito:** Reconhecemos que a IA não é uma pesquisadora proativa. Para componentes que utilizam bibliotecas externas complexas, o Coordenador pode iniciar uma fase de **"Auditoria de Conformidade" (F4.2)**, onde a IA é explicitamente instruída a comparar o código gerado com a documentação oficial para encontrar oportunidades de otimização e garantir o uso correto da API.

## 6. Testes Abrangentes e Estruturados

*   **Conceito:** A qualidade é verificada através de uma estratégia de testes multifacetada, com responsabilidades claras para cada tipo de teste.
*   **Implicações:**
    *   **Testes Unitários (TUs):** Gerados obrigatoriamente pelo `ImplementadorMestre` para todo o código de produção, com meta de 100% de cobertura da lógica.
    *   **Testes de Integração (TIs):** Gerados pelo `IntegradorTester` em pontos estratégicos para verificar a colaboração entre subsistemas.
    *   **Testes de Contrato:** Testes específicos para as interfaces (ABCs) para garantir que os contratos sejam sólidos e bem definidos.

## 7. Documentação Curada Como Ferramenta de Precisão

*   **Conceito:** Em vez de depender do conhecimento geral da IA, que pode estar desatualizado, nós fornecemos documentação oficial e exemplos de uso para bibliotecas complexas ou menos comuns.
*   **Implicações:**
    *   **Controle da Base de Conhecimento:** O Coordenador assume o controle da fonte de verdade que a IA utiliza, garantindo que ela trabalhe com APIs atuais e siga as melhores práticas.
    *   **Ativação na Fase de Auditoria:** Esta documentação curada torna-se especialmente poderosa quando usada como input para a fase de **Auditoria de Conformidade (F4.2)**, permitindo uma análise precisa e direcionada.

## 8. Iteração e Aprendizado Contínuo

*   **Conceito:** O Método AGV é um sistema "vivo". Seus prompts, fluxos e princípios são refinados com base na experiência prática e nos resultados obtidos.
*   **Implicações:**
    *   A evolução do "Pré-Lean" para o "Lean & Strategic" é o maior exemplo deste princípio em ação.
    *   Os "Snapshots" e relatórios de desvio são ferramentas cruciais para registrar os aprendizados e guiar a evolução futura do método.
```