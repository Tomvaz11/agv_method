# Princípios Chave do Método AGV v2.0 (Pós-Fotix)

Este documento descreve os princípios fundamentais de design, arquitetura e processo que norteiam o Método AGV para desenvolvimento de software assistido por IA, atualizados após a conclusão do projeto piloto Fotix.

## 1. Qualidade Intrínseca Desde o Início

**Conceito:** O foco primário do Método AGV é guiar a IA para produzir software cujo código e arquitetura sejam de **qualidade excepcional**, comparáveis (ou superiores em consistência e documentação) aos de um desenvolvedor sênior humano. Isso implica em:
    *   Definição de uma arquitetura robusta e modular antes da implementação.
    *   Adesão a boas práticas de engenharia de software (SOLID, DRY, KISS, etc.).
    *   Geração de código claro, legível, bem documentado e com tratamento de erros robusto.
    *   Minimização de débito técnico desde as fases iniciais.

**Filosofia:** A velocidade de desenvolvimento é secundária à qualidade intrínseca do software. Um produto de alta qualidade é inerentemente mais fácil de manter, escalar e evoluir, resultando em maior velocidade e menor custo a longo prazo.

## 2. Integração Incremental via Interfaces Explícitas

**Conceito:** Em vez de implementar módulos isoladamente e tentar conectá-los em uma grande fase final ("big bang integration"), o Método AGV adota uma abordagem incremental onde as conexões entre módulos são definidas *antecipadamente* através de interfaces explícitas (contratos) e a integração ocorre continuamente durante a implementação.

**Filosofia:** Esta abordagem espelha as melhores práticas de engenharia de software para construir sistemas robustos e manuteníveis, focando em baixo acoplamento e alta coesão. Ela direciona a IA (especificamente os agentes Tocrisna e ImplementadorMestre) a construir componentes que se encaixam corretamente desde o início.

**Como Funciona no Fluxo AGV (v3.0):**
1.  **Definição pela Tocrisna:** Durante a fase de arquitetura (`Prompt_F1_Tocrisna_Architecture_v1.1d`), a Tocrisna especifica as interfaces públicas chave (assinaturas de métodos, estruturas de dados) e dependências diretas entre módulos. O Blueprint Arquitetural torna-se a fonte da verdade.
2.  **Implementação pelo ImplementadorMestre:** Ao implementar um módulo (`Prompt_Implementador_Mestre_v2.7`), a IA recebe o contexto arquitetural relevante (incluindo interfaces e dependências) e é instruída a aderir estritamente a esses contratos. Testes unitários usam mocks/stubs para simular as interfaces de dependência externa.
3.  **Validação pelos Testes de Integração:** O `IntegradorTester` (`Prompt_IntegradorTester_v1.0`) gera testes que verificam a colaboração real entre os módulos implementados, sem mocks para suas interconexões diretas, validando os contratos.

**Vantagens:** Redução de acoplamento, manutenibilidade, previsibilidade na integração, eficiência de contexto para IA, testabilidade.

## 3. Colaboração Humano-IA Estruturada e Orientada por Prompts

**Conceito:** O Método AGV estrutura a colaboração através de fases bem definidas, com "agentes" (representados por prompts modelo especializados e versionados) responsáveis por tarefas específicas. O Coordenador humano guia, valida e toma decisões críticas.

**Filosofia:** A IA é uma ferramenta poderosa, mas requer direcionamento preciso e validação humana para produzir resultados de alta qualidade. Prompts detalhados e bem elaborados são o principal mecanismo de instrução e controle.

**Como Funciona no Fluxo AGV (v3.0):** Cada fase utiliza um prompt específico (ex: `Prompt_Implementador_Mestre_v2.7`) que contém instruções detalhadas, contexto necessário, e a estrutura esperada do output. O Coordenador prepara e executa esses prompts.

## 4. Validação Humana Crítica e Contínua

**Conceito:** O Coordenador humano desempenha um papel indispensável em todas as etapas críticas do processo, desde a definição inicial até a aprovação final do código e dos testes.

**Filosofia:** Nenhuma saída da IA é aceita sem escrutínio. A validação humana garante que os resultados estejam alinhados com os objetivos do projeto, os padrões de qualidade e os princípios do Método AGV.

**Como Funciona no Fluxo AGV (v3.0):** Pontos de "Validação Humana" explícitos ocorrem após a geração do Blueprint Arquitetural, da Ordem de Implementação (opcionalmente assistida), de cada implementação de módulo e TU pelo `ImplementadorMestre`, e de cada conjunto de TIs pelo `IntegradorTester`.

## 5. Testes Abrangentes e Estruturados

**Conceito:** A qualidade é verificada através de uma estratégia de testes multifacetada, com responsabilidades claras para cada tipo de teste.
    *   **Testes Unitários (TUs):** Gerados obrigatoriamente pelo `ImplementadorMestre` para todo novo código de produção. Devem ter alta cobertura (meta >95-100%) e seguir uma estrutura espelhada em `tests/unit/`.
    *   **Testes de Integração (TIs):** Gerados pelo `IntegradorTester` em pontos estratégicos definidos pelo `OrchestratorHelper`. Verificam a colaboração entre grupos de módulos.
    *   **Framework de Testes:** Definido pelo Coordenador na Fase 1 (ex: `pytest`).

**Filosofia:** Testes não são um adendo, mas uma parte integral do processo de desenvolvimento, garantindo robustez e facilitando refatorações futuras.

## 6. Documentação Curada na Codebase para Bibliotecas Específicas/Complexas (NOVO/EVOLUÍDO)

**Conceito:** Para bibliotecas que são parte da stack tecnológica definida, mas que são menos comuns, possuem APIs complexas, ou para as quais a IA demonstrou dificuldade em encontrar/aplicar informações corretas via busca web, o Coordenador deve prover documentação relevante e exemplos de uso diretamente na codebase (ou como parte do contexto do prompt).

**Filosofia:** Esta abordagem dá ao Coordenador controle sobre a fonte de verdade que a IA utiliza para bibliotecas desafiadoras, reduzindo a probabilidade de a IA "alucinar", usar APIs obsoletas, ou desviar-se da stack. Isso força a IA a trabalhar dentro das restrições e com o conhecimento fornecido, levando a soluções mais precisas e aderentes.

**Como Funciona no Fluxo AGV (v3.0):**
1.  **Identificação pelo Coordenador:** O Coordenador antecipa ou identifica (durante uma iteração) que uma biblioteca designada (ex: `stream-unzip`, `PySide6`) pode ser problemática para a IA.
2.  **Curadoria de Documentação:** O Coordenador obtém e organiza trechos relevantes da documentação oficial, exemplos de código, ou até mesmo cria pequenos exemplos de uso e os adiciona à codebase do projeto (ex: em um diretório `docs/lib_specific_guides/`) ou os anexa ao prompt.
3.  **Diretriz no Prompt:** O `Prompt_Implementador_Mestre_v2.7` (Diretriz 4) instrui a IA a:
    *   **Consultar OBRIGATORIAMENTE** esta documentação fornecida na codebase/contexto PRIMEIRO ao encontrar dificuldades com a biblioteca.
    *   Se a documentação fornecida for insuficiente ou ausente para resolver o problema, a IA deve **PARAR a implementação e SOLICITAR explicitamente ao Coordenador** que forneça a documentação/exemplos adicionais ou novas instruções.
    *   É **PROIBIDO** à IA usar bibliotecas alternativas não designadas como fallback ou buscar autonomamente na web por soluções para essas bibliotecas problemáticas sem instrução explícita.

**Resultado (Validado no Projeto Fotix):** Esta estratégia demonstrou ser altamente eficaz para garantir que a IA utilize corretamente bibliotecas desafiadoras, superando obstáculos que anteriormente levavam a falhas ou desvios da stack.

## 7. Iteração e Aprendizado Contínuo

**Conceito:** O Método AGV, seus prompts e seus processos são considerados "vivos". Eles são refinados continuamente com base na experiência prática e nos resultados obtidos em projetos piloto.

**Filosofia:** A colaboração humano-IA é um campo em evolução. A capacidade de aprender com cada interação, identificar o que funciona (e o que não funciona) e ajustar a metodologia é crucial para o sucesso a longo prazo. Os "Snapshots Detalhados e Contextualizados" servem como um registro dessa evolução.
```

---

Por favor, revise estes dois documentos com atenção. Eles tentam capturar a essência do nosso método AGV evoluído. Estou pronto para discutir quaisquer ajustes, acréscimos ou refinamentos que você julgar necessários!