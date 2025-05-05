**Arquivo: `AGV_Method_Principios_Chave_v1.0.md`**
*(Versão revisada, referenciando os prompts corretos e adicionando a nota sobre Framework de Testes)*

```markdown
# Princípios Chave do Método AGV v1.0

Este documento descreve os princípios fundamentais de design, arquitetura e processo que norteiam o Método AGV para desenvolvimento de software assistido por IA. *(Nota: Embora os princípios sejam v1.0, o Workflow que os aplica pode ter evoluído para v1.2 ou superior)*.

## 1. Integração Incremental via Interfaces Explícitas

**Conceito:** Em vez de implementar módulos isoladamente e tentar conectá-los em uma grande fase final ("big bang integration"), o Método AGV adota uma abordagem incremental onde as conexões entre módulos são definidas *antecipadamente* através de interfaces explícitas (contratos) e a integração ocorre continuamente durante a implementação.

**Filosofia:** Esta abordagem espelha as melhores práticas de engenharia de software para construir sistemas robustos e manuteníveis, focando em baixo acoplamento e alta coesão. Ela direciona a IA (especificamente o agente Tocle) a construir componentes que se encaixam corretamente desde o início, em vez de depender de inferências complexas sobre como os módulos devem interagir baseadas apenas na análise do código existente.

**Como Funciona no Fluxo AGV:**

1.  **Definição pela Tocrisna (Arquiteta):** Durante a fase de arquitetura (usando `Prompts/Templates/Prompt_Tocrisna_Architecture_v1.1b.md`), além de definir os módulos e suas responsabilidades, a Tocrisna **deve** especificar as **interfaces públicas chave** para a comunicação entre eles e suas **dependências diretas**. Isso inclui:
    *   Assinaturas de funções/métodos (nomes, parâmetros com tipos, tipo de retorno).
    *   Estruturas de dados (Dataclasses, NamedTuples, etc.) usadas para troca de informações.
    *   Uma breve descrição do propósito de cada elemento da interface.
    *   Uma lista explícita dos outros módulos internos dos quais este depende.
    *   O output da Tocrisna (Blueprint Arquitetural) torna-se a fonte da verdade para esses contratos e dependências.

2.  **Uso pelo Severino (Especificador):** Ao detalhar a funcionalidade de um módulo (usando `Prompts/Templates/Prompt_Severino_EspeciFi_v1.2.md`), o Severino **deve** receber o contexto arquitetural relevante (incluindo interfaces e dependências) do Blueprint e referenciar explicitamente as interfaces definidas pela Tocrisna quando descrever os passos de processamento que envolvem chamadas a outros módulos.

3.  **Implementação pelo Tocle (Engenheiro):** Ao implementar um módulo (usando `Prompts/Templates/Prompt_Tocle_Implementation_v1.2b.md`):
    *   O **Contexto Arquitetural** fornecido no prompt incluirá as interfaces e dependências relevantes.
    *   Tocle é instruído a **aderir estritamente** a essas interfaces e a **usar o contexto** dos arquivos listados em "Dependências Diretas".
    *   Chamar outros módulos *apenas* através das interfaces de dependência fornecidas ou importando diretamente das dependências listadas.
    *   Implementar as interfaces expostas conforme especificado.
    *   Os **testes unitários** gerados pelo Tocle **devem usar mocks/stubs** para simular as interfaces de dependência externa ao módulo, garantindo que o teste foque apenas na lógica interna do módulo atual.

4.  **Validação Incremental (Você + Testes de Integração):**
    *   Após Tocle implementar módulos que interagem (ex: Módulo A que chama Módulo B), você (como coordenador) deve validar essa interação.
    *   Isso idealmente envolve a criação e execução de **Testes de Integração**, que *não* usam mocks para a conexão entre A e B, verificando se a chamada real funciona conforme o contrato definido pela Tocrisna. (A criação desses testes pode ser uma tarefa separada, talvez assistida por IA com um prompt específico ou usando `Prompts/Templates/Prompt_Tocle_RefatorTest_v1.0.md` adaptado).

**Vantagens Desta Abordagem:**

*   **Redução de Acoplamento:** Os módulos dependem dos *contratos* (interfaces), não dos detalhes internos de implementação uns dos outros.
*   **Manutenibilidade:** Mudanças internas em um módulo são menos propensas a quebrar outros módulos, desde que a interface seja mantida.
*   **Previsibilidade:** A integração torna-se mais previsível, pois os pontos de conexão são definidos e implementados de forma explícita.
*   **Eficiência de Contexto para IA:** O Tocle precisa apenas da definição da interface de um dependente ou do código de sua dependência direta, não do código completo de módulos indiretamente relacionados.
*   **Testabilidade:** Facilita testes unitários isolados e define claramente o que precisa ser verificado nos testes de integração.

**Desafios:**

*   Exige uma definição de interfaces e dependências clara e bem pensada na fase de arquitetura (trabalho crítico da Tocrisna e validação sua).
*   Mudanças nas interfaces ou dependências fundamentais requerem coordenação para atualizar todos os módulos envolvidos.

*Este princípio é fundamental para construir sistemas complexos de forma gerenciável e robusta com o auxílio da IA.*

## 2. (Placeholder) Qualidade de Código e Boas Práticas

*Esta seção pode ser expandida futuramente para detalhar os padrões específicos de código (além do PEP 8), tratamento de erros, logging, etc., esperados em todas as implementações.*

## 3. (Placeholder) Abordagem de Testes AGV

*Esta seção pode detalhar a estratégia geral de testes (unitários, integração, E2E), ferramentas preferidas, e expectativas de cobertura.*
***Nota:** A escolha do **Framework de Testes** principal (ex: pytest, unittest) é uma decisão de stack definida na Fase 1 pelo Coordenador.*