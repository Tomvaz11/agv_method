# AGV Prompt Template: Severino v1.1 - Especificação Funcional Detalhada

**Tarefa Principal:** Detalhar a especificação técnica para a funcionalidade/módulo descrito na seção **"Descrição de Alto Nível da Funcionalidade (Fornecida por Você)"** abaixo, baseando-se estritamente no contexto arquitetural fornecido. O resultado deve ser formatado de forma clara e precisa, pronto para ser usado na seção "Especificação da Funcionalidade/Módulo a ser Implementada" do prompt do agente Tocle.

**Contexto do Projeto e Arquitetura (Definido por Fases Anteriores):**

*   **Nome do Projeto:** `Fotix`
*   **Objetivo Geral do Projeto:** Aplicativo desktop para localizar e remover arquivos duplicados (imagens/vídeos) em diretórios e ZIPs, selecionando automaticamente qual manter com base em critérios (resolução, data, nome), com backup e restauração, otimizado para grandes volumes.
*   **Blueprint Arquitetural Relevante (Extraído do Output da Tocrisna):**
    *   **Módulo/Arquivo Alvo desta Especificação:** `fotix/src/fotix/core/decision_logic.py`
    *   **Principais Responsabilidades deste Módulo/Arquivo (Conforme Arquitetura):** Implementar o algoritmo de decisão para escolher qual arquivo manter dentro de um grupo de duplicatas, baseado em regras de negócio (resolução, data, nome, etc.).
    *   **Dependências Diretas deste Módulo (Conforme Arquitetura):**
        *   `fotix.domain.models` (para as estruturas de dados `FileMetadata`, `DuplicateGroup`)
    *   **Interfaces de Dependências (Contratos a serem Usados por este Módulo):**
        *   `[Nenhuma interface de serviço externo explicitamente chamada por este módulo, conforme a arquitetura.]` (O módulo opera sobre os dados recebidos como parâmetros).
    *   **Interfaces Expostas (Contratos Fornecidos por este Módulo):**
        *   `decide_file_to_keep(group: DuplicateGroup) -> FileMetadata`: Aplica as regras de negócio (resolução, data, nome) para selecionar o melhor arquivo dentro de um grupo de duplicatas.
    *   **Estruturas de Dados Relevantes (Definidas pela Arquitetura):**
        ```python
        from dataclasses import dataclass, field
        from pathlib import Path
        from typing import List, Dict, Optional, Iterator

        @dataclass(frozen=True)
        class FileMetadata:
            path: Path
            size: int
            creation_time: float # Timestamp UTC
            # Potencialmente outros metadados úteis para decisão (resolução, etc. - a serem extraídos seletivamente)
            # hash: Optional[str] = None # Preenchido durante o processamento

        @dataclass
        class DuplicateGroup:
            files: List[FileMetadata] # Lista de arquivos idênticos
            file_to_keep: Optional[FileMetadata] = None # Decidido pelo Core
            hash_value: str # Hash que identifica o grupo
        ```

**Descrição de Alto Nível da Funcionalidade (Fornecida por Você):**

A funcionalidade esperada neste módulo (`decision_logic.py`) é permitir que, após a identificação de arquivos duplicados agrupados em um `DuplicateGroup`, o sistema seja capaz de aplicar uma lógica de decisão clara para escolher qual arquivo deve ser mantido.

O critério de decisão segue três níveis de prioridade:
1. **Resolução da imagem/vídeo**: manter o arquivo com a maior resolução (largura × altura).
2. **Data de modificação**: em caso de empate na resolução, manter o arquivo mais recentemente modificado.
3. **Nome do arquivo**: se ainda houver empate, manter o arquivo com o nome mais curto.

Esse processo deve ser totalmente isolado de operações de entrada e saída (I/O) e ser implementado de forma pura dentro da camada `core`, permitindo testes unitários precisos. O arquivo selecionado como “a manter” deve ser retornado como um objeto `FileMetadata`, e essa decisão será usada posteriormente pela aplicação para mover os demais arquivos para backup ou exclusão.

**Diretrizes para Geração da Especificação:**

1.  **Base na Descrição de Alto Nível:** A especificação deve implementar fielmente a funcionalidade descrita por você acima.
2.  **Clareza e Precisão:** A especificação deve ser inequívoca e fácil de entender por um desenvolvedor (ou pelo agente Tocle).
3.  **Detalhamento:** Descreva os passos lógicos necessários para implementar a funcionalidade.
4.  **Referência às Interfaces:** Quando o processamento envolver a interação com outros módulos, refira-se explicitamente às interfaces listadas no "Contexto Arquitetural". (Neste caso, focar na interface exposta e nas estruturas de dados).
5.  **Inputs e Outputs:** Detalhe claramente os inputs esperados (parâmetros: `DuplicateGroup`, tipos de dados: definidos em `fotix.domain.models`) e os outputs (valor de retorno: `FileMetadata`).
6.  **Regras de Negócio:** Incorpore todas as regras de negócio mencionadas na descrição de alto nível (ex: critérios de resolução, data, nome).
7.  **Tratamento de Erros:** Especifique os principais cenários de erro razoáveis para a funcionalidade descrita e como devem ser tratados (ex: o que fazer se o `DuplicateGroup` estiver vazio ou contiver menos de dois arquivos? O que fazer se os metadados necessários para a decisão estiverem faltando em alguns arquivos?). Sugira exceções apropriadas (ex: `ValueError`).
8.  **Casos de Borda:** Mencione casos de borda óbvios (ex: grupo com apenas dois arquivos, todos os arquivos com metadados idênticos segundo os critérios, arquivos sem metadados de resolução/data).
9.  **Formato Adequado:** Use linguagem clara, listas ou passos numerados. A saída deve ser adequada para colar diretamente na seção "Especificação..." do `Prompt_Tocle`.

**Resultado Esperado:**

Um bloco de texto contendo a **Especificação Técnica Detalhada** da funcionalidade, pronta para ser usada no prompt do Tocle, detalhando inputs, passos lógicos (referenciando interfaces), outputs, regras de negócio, tratamento de erro e casos de borda, **baseado na descrição de alto nível fornecida**.