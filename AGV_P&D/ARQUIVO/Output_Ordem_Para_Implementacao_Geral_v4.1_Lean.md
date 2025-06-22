### **Instruções para o Coordenador de Projeto**

Este documento define a sequência de implementação dos módulos e os pontos de parada para Testes de Integração (TI). Cada parada de TI inclui o objetivo e os cenários chave necessários para validar a coesão do subsistema recém-desenvolvido.

### **Módulos Base do Projeto (Fonte da Verdade)**

*   `fotix.core.models`
*   `fotix.core.duplicate_finder`
*   `fotix.core.selection_strategy`
*   `fotix.infrastructure.file_system_service`
*   `fotix.infrastructure.hash_service`
*   `fotix.infrastructure.zip_service`
*   `fotix.infrastructure.concurrency_service`
*   `fotix.infrastructure.log_service`
*   `fotix.application.scan_service`
*   `fotix.application.backup_service`
*   `fotix.ui.MainWindow`
*   `fotix.ui.SettingsView`
*   `fotix.ui.ProgressView`
*   `fotix.ui.ResultsView`
*   `fotix.ui.RestoreView`

---

### **Ordem de Implementação e Pontos de Teste**

1.  `fotix.core.models`
2.  `fotix.core.duplicate_finder`
3.  `fotix.core.selection_strategy`

`>>> PARADA PARA TESTES DE INTEGRAÇÃO (SUBSISTEMA DE LÓGICA DE DOMÍNIO) <<<`
*   **Módulos no Grupo:** `fotix.core.models`, `fotix.core.duplicate_finder`, `fotix.core.selection_strategy`.
*   **Objetivo do Teste:** Validar que a lógica de negócio principal para identificar duplicatas e selecionar o melhor arquivo funciona corretamente em isolamento, usando estruturas de dados em memória (`FileRecord`, `DuplicateSet`), sem qualquer dependência de UI ou sistema de arquivos.
*   **Cenários Chave:**
    1.  **Identificação Correta:** Fornecer uma lista de objetos `FileRecord` (com alguns com mesmo hash e tamanho) para o `duplicate_finder` e verificar se ele agrupa corretamente os arquivos nos `DuplicateSet`s esperados.
    2.  **Estratégia de Seleção:** Passar um `DuplicateSet` para o `selection_strategy` e confirmar que ele retorna o `FileRecord` correto como o "melhor" arquivo, com base nas regras de negócio (ex: maior resolução, data mais recente).
    3.  **Cenário Sem Duplicatas:** Fornecer uma lista de `FileRecord`s onde nenhum arquivo é duplicado e garantir que o `duplicate_finder` retorne uma lista vazia de `DuplicateSet`s.

---
4.  `fotix.infrastructure.log_service`
5.  `fotix.infrastructure.file_system_service`
6.  `fotix.application.backup_service`

`>>> PARADA PARA TESTES DE INTEGRAÇÃO (SUBSISTEMA DE BACKUP E RESTAURAÇÃO) <<<`
*   **Módulos no Grupo:** `fotix.core.models`, `fotix.infrastructure.log_service`, `fotix.infrastructure.file_system_service`, `fotix.application.backup_service`.
*   **Objetivo do Teste:** Validar que o fluxo completo de backup e restauração funciona, provando que o `BackupService` pode orquestrar o `FileSystemService` para mover arquivos, criar manifestos de backup e restaurá-los com base nesses manifestos.
*   **Cenários Chave:**
    1.  **Fluxo de Backup:** Chamar o `backup_service` para fazer backup de um arquivo de teste. Verificar se (a) o arquivo original foi movido para o diretório de backup, (b) um arquivo `BackupManifest` em JSON foi criado no local correto e (c) o conteúdo do manifesto está correto (caminho original, novo caminho, timestamp).
    2.  **Fluxo de Restauração:** Chamar o `backup_service` para restaurar o arquivo do cenário anterior. Verificar se o arquivo foi movido de volta para sua localização original e se o arquivo de backup foi removido do diretório de backup.
    3.  **Leitura de Manifestos:** Criar múltiplos arquivos de manifesto de backup manualmente no diretório de backup. Chamar a função do serviço que lê todos os manifestos e verificar se ela retorna a lista correta de objetos `BackupManifest` Pydantic.

---
7.  `fotix.infrastructure.hash_service`
8.  `fotix.infrastructure.concurrency_service`
9.  `fotix.infrastructure.zip_service`
10. `fotix.application.scan_service`

`>>> PARADA PARA TESTES DE INTEGRAÇÃO (FLUXO DE VARREDURA E LIMPEZA - HEADLESS) <<<`
*   **Módulos no Grupo:** Todos os módulos de `core` e `infrastructure`, mais `fotix.application.scan_service` e `fotix.application.backup_service`.
*   **Objetivo do Teste:** Validar o caso de uso mais crítico da aplicação de ponta a ponta, sem a interface gráfica. O teste deve confirmar que o `ScanService` orquestra corretamente todos os outros serviços (sistema de arquivos, hash, concorrência, lógica de domínio, backup) para executar uma varredura e limpeza completa.
*   **Cenários Chave:**
    1.  **Caminho Feliz E2E:** Preparar um diretório de teste com subpastas e arquivos duplicados conhecidos. Executar o `scan_service.execute_scan()`. Verificar se o `ScanResult` retornado contém as estatísticas corretas e se os arquivos redundantes foram movidos para o backup, confirmando com o `backup_service`.
    2.  **Integração da Concorrência:** Executar uma varredura em um diretório com vários arquivos. Verificar (via logs ou tempo de execução) que o processo de hashing foi paralelizado e que o resultado final está correto, validando a integração do `concurrency_service`.
    3.  **Filtro de Varredura:** Executar uma varredura com `ScanSettings` que definem um `min_file_size_mb`. Verificar se os arquivos menores que o limite são corretamente ignorados e não aparecem nos `duplicate_sets` do resultado.

---
11. `fotix.ui.MainWindow`
12. `fotix.ui.SettingsView`
13. `fotix.ui.ProgressView`
14. `fotix.ui.ResultsView`
15. `fotix.ui.RestoreView`

`>>> PARADA PARA TESTES DE INTEGRAÇÃO (SISTEMA COMPLETO - E2E COM UI) <<<`
*   **Módulos no Grupo:** Todos os módulos do projeto, incluindo a camada `fotix.ui`.
*   **Objetivo do Teste:** Validar que a interface do usuário (UI) se integra corretamente com os serviços da camada de aplicação (`ScanService`, `BackupService`), respondendo a ações do usuário e refletindo o estado do sistema de forma precisa e reativa.
*   **Cenários Chave:**
    1.  **Fluxo de Limpeza via UI:** Simular um usuário que: seleciona um diretório na `SettingsView`, clica em "Escanear", observa a `ProgressView`, visualiza os resultados na `ResultsView` e clica em "Limpar". Verificar se os arquivos corretos foram movidos para a lixeira/backup.
    2.  **Fluxo de Restauração via UI:** Simular um usuário que: abre a `RestoreView`, vê a lista de backups da ação anterior, seleciona um item e clica em "Restaurar". Verificar se o arquivo reaparece em seu local original.
    3.  **Intervenção do Usuário:** Na `ResultsView`, o usuário manualmente altera a seleção padrão de qual arquivo manter em um `DuplicateSet`. Após confirmar a limpeza, verificar se a escolha do usuário foi respeitada, em vez da sugestão automática da `selection_strategy`.