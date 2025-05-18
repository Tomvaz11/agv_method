# AGV Prompt Template: Tradução de Cenários UAT para Testes de Backend Automatizados (Pytest) v1.0

**Tarefa Principal:** Analisar os cenários de teste de aceitação do usuário (UAT) fornecidos no arquivo `@NOME_DO_ARQUIVO_UAT.MD` para a aplicação especificada. Para cada cenário UAT, gerar um script de teste `pytest` correspondente que valide a funcionalidade descrita, interagindo **diretamente com os serviços da camada de aplicação e infraestrutura (backend)** da aplicação, sem usar a interface gráfica do usuário (UI).

**Contexto e Artefatos Essenciais (A SER PREENCHIDO PELO COORDENADOR - APENAS NOMES DOS ARQUIVOS):**

1.  **Cenários UAT para Tradução:** `@teste_h.md` [ALTERAR AQUI COM O NOME DO ARQUIVO UAT]
    *   *(Instrução para Coordenador: Substitua pelo nome exato do arquivo Markdown contendo os cenários UAT.)*
2.  **Blueprint Arquitetural:** `@Output_BluePrint_Arquitetural_Tocrisna_v3.md` [ALTERAR AQUI COM O NOME DO ARQUIVO BLUEPRINT]
    *   *(Instrução para Coordenador: Substitua pelo nome exato do arquivo do Blueprint Arquitetural validado do projeto atual.)*
3.  **Código Fonte do Projeto:** `@` (ou `@CAMINHO_PARA_RAIZ_DO_CODIGO_FONTE` se a IA precisar de uma referência mais explícita ou se o contexto `@` não for suficiente/claro para a ferramenta).
    *   *(Instrução para Coordenador: Garanta que a IA tenha acesso à codebase completa do projeto para entender a implementação dos serviços, modelos de dados e interfaces que precisará chamar e instanciar.)*

**Instruções Detalhadas para a IA:**

1.  **Análise Individual de Cenários UAT:**
    *   Para cada cenário UAT presente no `@NOME_DO_ARQUIVO_UAT.MD`:
        *   Identifique o **objetivo principal** e o **fluxo funcional** que o cenário visa testar.
        *   Extraia as **pré-condições** e os **dados de teste sugeridos**.
        *   Entenda os **passos de execução** do ponto de vista da interação do usuário e traduza-os para operações que seriam realizadas pelos serviços de backend.
        *   Identifique os **resultados esperados** que podem ser verificados programaticamente (estado do sistema de arquivos, conteúdo de arquivos de metadados de backup, valores de retorno de serviços, etc.).

2.  **Geração de Scripts de Teste `pytest`:**
    *   Para cada cenário UAT, crie uma ou mais funções de teste `pytest` (ex: `def test_uat_cenario_XXX_descricao_curta():`).
    *   **Organização:** Recomenda-se criar um único arquivo Python (ex: `test_backend_uats_[NOME_PROJETO].py`) contendo todas as funções de teste. Se o número de testes se tornar muito grande, considere organizá-los em um subdiretório dentro da estrutura de testes do projeto (ex: `tests/backend_uats/`).

3.  **Implementação de Cada Função de Teste `pytest`:**
    *   **a. Setup do Ambiente de Teste:**
        *   Utilize fixtures `pytest` (ex: `tmp_path` para diretórios temporários) para configurar o ambiente descrito nas "Pré-condições" e "Dados de Teste Sugeridos" de cada cenário UAT. Isso inclui:
            *   Criar estruturas de diretórios e arquivos de teste com conteúdo específico (se relevante).
            *   Preparar arquivos ZIP com conteúdo específico (se o cenário envolver ZIPs).
            *   Garantir que quaisquer caminhos configuráveis (como diretórios de backup) usem locais temporários e limpos para cada teste.
    *   **b. Instanciação de Serviços do Backend:**
        *   Com base no `@NOME_DO_ARQUIVO_BLUEPRINT.MD` e no código fonte (`@`), instancie as classes de serviço necessárias das camadas de aplicação e infraestrutura do projeto.
        *   Resolva as dependências entre os serviços corretamente (ex: via injeção de dependência, conforme o design do projeto).
    *   **c. Execução da Lógica Funcional via Chamadas de Serviço:**
        *   Traduza os "Passos para Execução" do cenário UAT em chamadas de métodos aos serviços instanciados. Evite qualquer código relacionado à UI.
    *   **d. Mocking de Dependências Externas ou da UI:**
        *   Se os serviços de backend tiverem dependências que não devem ser acionadas neste nível de teste (ex: chamadas a APIs externas reais, interações diretas com hardware específico, ou callbacks para componentes da UI), essas dependências **DEVEM SER MOCKADAS** usando `unittest.mock.patch` ou fixtures `pytest-mock`.
    *   **e. Asserções e Verificações Programáticas:**
        *   Traduza os "Resultados Esperados" do cenário UAT em asserções `pytest` (`assert`).
        *   Verifique o estado do sistema de arquivos, o conteúdo de arquivos, valores retornados por serviços, ou se exceções esperadas são levantadas (`pytest.raises`).
    *   **f. Teardown (Limpeza Automática):**
        *   Priorize o uso de fixtures `pytest` (como `tmp_path`) que gerenciam automaticamente a limpeza de recursos temporários (arquivos, diretórios) após cada teste, garantindo o isolamento dos testes.

4.  **Boas Práticas de Código de Teste:**
    *   Mantenha os testes independentes e sem efeitos colaterais entre si.
    *   Use nomes descritivos para as funções de teste, variáveis e fixtures.
    *   Adicione comentários concisos no código de teste onde a lógica for complexa ou a tradução do UAT não for óbvia.
    *   Siga as convenções de estilo do Python (PEP 8).

5.  **Formato do Output:**
    *   Gere o(s) arquivo(s) `.py` contendo os scripts de teste `pytest` completos e executáveis.
    *   Se encontrar dificuldades intransponíveis para traduzir um cenário UAT específico, ou se uma suposição crítica precisar ser feita para a implementação do teste de backend, documente isso claramente como um comentário no código de teste correspondente ou em uma seção de notas separada no final do output.

**Lembretes para a IA:**

*   O objetivo é testar a lógica do **backend** da aplicação, simulando os fluxos que um usuário realizaria através da UI, mas sem depender ou interagir com a UI.
*   Foque em replicar a *essência funcional* descrita no UAT.
*   A precisão na configuração do ambiente de teste e nas asserções é crucial.
*   Consulte extensivamente o Blueprint Arquitetural e o código fonte para entender como os serviços devem ser chamados e como interagem.