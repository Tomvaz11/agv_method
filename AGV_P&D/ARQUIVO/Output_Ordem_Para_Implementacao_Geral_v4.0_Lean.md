# Ordem de Implementação e Pontos de Teste de Integração (TI)

Este documento define a ordem de construção e os pontos de verificação para os testes de integração do projeto `Fotix`, derivado do `Blueprint Arquitetural`.

## Módulos Base para Implementação

*   `fotix.core.models`
*   `fotix.core.duplicate_finder`
*   `fotix.core.selection_strategy`
*   `fotix.application.interfaces` (Arquivo virtual contendo as definições de interface)
*   `fotix.application.scanning_service`
*   `fotix.application.action_service`
*   `fotix.infrastructure.file_system_service`
*   `fotix.infrastructure.zip_scanner_service`
*   `fotix.infrastructure.hashing_service`
*   `fotix.infrastructure.concurrency_service`
*   `fotix.infrastructure.backup_service`
*   `fotix.infrastructure.logging_service`
*   `fotix.ui` (Representando toda a camada de apresentação)

## Ordem de Implementação e Pontos de Teste

1.  `fotix.core.models`
2.  `fotix.application.interfaces`
3.  `fotix.core.duplicate_finder`
4.  `fotix.core.selection_strategy`
>>> **PARADA PARA TESTES DE INTEGRAÇÃO (LÓGICA CORE)** <<<
*   **Módulos no Grupo:** `fotix.core.models`, `fotix.application.interfaces`, `fotix.core.duplicate_finder`, `fotix.core.selection_strategy`.
*   **Objetivo do Teste:** Validar que a lógica de negócio pura, operando sobre modelos de dados em memória (`FileRecord`), consegue agrupar corretamente os duplicados (`DuplicateSet`) e aplicar a estratégia de seleção para determinar o arquivo a ser mantido (`keeper`).
*   **Cenários Chave:**
    1.  **Agrupamento de Duplicatas:** Fornecer uma lista de `FileRecord` (com hashes pré-definidos) para o `DuplicateFinder` e verificar se ele gera o número correto de `DuplicateSet`, agrupando os arquivos com hashes idênticos.
    2.  **Estratégia de Seleção:** Fornecer um `DuplicateSet` para a `SelectionStrategy` e confirmar que o `keeper` é selecionado corretamente com base nos critérios de resolução, data e nome definidos no blueprint.
    3.  **Cenário sem Duplicatas:** Fornecer ao `DuplicateFinder` uma lista de `FileRecord` onde todos os hashes são únicos e garantir que o resultado seja uma lista vazia de `DuplicateSet`.
5.  `fotix.infrastructure.logging_service`
6.  `fotix.infrastructure.hashing_service`
7.  `fotix.infrastructure.concurrency_service`
8.  `fotix.infrastructure.file_system_service`
9.  `fotix.infrastructure.zip_scanner_service`
10. `fotix.application.scanning_service`
>>> **PARADA PARA TESTES DE INTEGRAÇÃO (SUBSISTEMA DE ESCANEAMENTO)** <<<
*   **Módulos no Grupo:** `fotix.infrastructure.logging_service`, `fotix.infrastructure.hashing_service`, `fotix.infrastructure.concurrency_service`, `fotix.infrastructure.file_system_service`, `fotix.infrastructure.zip_scanner_service`, `fotix.application.scanning_service`.
*   **Objetivo do Teste:** Validar que o `ScanningService` consegue orquestrar com sucesso os serviços de infraestrutura e a lógica do core para executar um fluxo completo de escaneamento, desde a leitura do sistema de arquivos até a produção de uma lista final de `DuplicateSet` com os `keepers` definidos.
*   **Cenários Chave:**
    1.  **Fluxo Padrão:** Preparar um diretório com arquivos de imagem duplicados. Invocar o `ScanningService` para escanear este diretório. Verificar se o serviço retorna os `DuplicateSet` corretos, com todos os `FileRecord` preenchidos (hash, tamanho, etc.) e o `keeper` selecionado.
    2.  **Inclusão de Arquivo ZIP:** Preparar um diretório contendo imagens e um arquivo ZIP que também contém duplicatas dessas imagens. Executar o `ScanningService` com a opção `include_zip_files=True`. Verificar se os arquivos de dentro do ZIP são corretamente identificados e agrupados com seus duplicados externos.
    3.  **Exclusão de Diretório:** Preparar um diretório com uma subpasta contendo arquivos duplicados. Executar o escaneamento configurando a exclusão dessa subpasta. Validar que os arquivos dentro da pasta excluída não aparecem nos resultados.
11. `fotix.infrastructure.backup_service`
12. `fotix.application.action_service`
>>> **PARADA PARA TESTES DE INTEGRAÇÃO (SUBSISTEMA DE AÇÕES)** <<<
*   **Módulos no Grupo:** `fotix.infrastructure.backup_service`, `fotix.application.action_service`.
*   **Objetivo do Teste:** Validar que o `ActionService` pode, a partir de um conjunto de duplicatas, orquestrar de forma segura as operações de backup e remoção de arquivos, e também a restauração a partir de um backup existente.
*   **Cenários Chave:**
    1.  **Backup e Remoção Segura:** Criar um `DuplicateSet` manualmente, apontando para arquivos temporários. Passá-lo para o `ActionService` para exclusão. Verificar se os arquivos marcados como `to_delete` são movidos para a lixeira do sistema e se uma pasta de backup correspondente (contendo os arquivos e um `manifest.json`) é criada.
    2.  **Restauração de Backup:** Após executar o cenário anterior, usar o `ActionService` (ou diretamente o `BackupService`) para restaurar o backup pelo ID gerado. Verificar se os arquivos são retornados aos seus locais originais e se a pasta de backup é removida.
    3.  **Manifesto de Backup:** Inspecionar o arquivo `manifest.json` criado pelo `BackupService` para garantir que ele contém a lista correta de `FileRecord` serializados, incluindo seus caminhos originais.
13. `fotix.ui`
>>> **PARADA PARA TESTES DE INTEGRAÇÃO (APLICAÇÃO COMPLETA - E2E)** <<<
*   **Módulos no Grupo:** `fotix.ui` (integrado com todos os serviços de aplicação já testados).
*   **Objetivo do Teste:** Validar o fluxo completo da aplicação do ponto de vista do usuário, garantindo que a camada de apresentação (UI) interage corretamente com os serviços de aplicação (`ScanningService`, `ActionService`) e que a interface permanece responsiva durante operações longas.
*   **Cenários Chave:**
    1.  **Ciclo de Vida Completo:** Utilizar a UI para: (a) selecionar um diretório com duplicatas, (b) iniciar o escaneamento, (c) visualizar os resultados na tabela, (d) confirmar a ação de exclusão. Verificar se os arquivos são movidos para a lixeira e a UI é atualizada.
    2.  **Responsividade e Feedback de Progresso:** Iniciar um escaneamento em um diretório grande. Verificar se a `ProgressView` (ou componente similar) exibe atualizações de progresso em tempo real (ex: "Hashing 50/100") sem que a janela principal da aplicação trave.
    3.  **Fluxo de Restauração via UI:** Navegar até a tela de restauração (`RestoreView`), selecionar um backup criado anteriormente e acionar a restauração. Verificar se os arquivos são restaurados no sistema de arquivos e a lista de backups na UI é atualizada.