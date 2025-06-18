# Output_Ordem_Para_Implementacao_Geral.md

**Instruções para o Coordenador:**

Este documento fornece a ordem de implementação sequencial e os pontos de verificação para testes de integração.

*   A seção "Módulos Base" lista componentes estruturais que serão criados sob demanda durante a implementação dos "Módulos Principais".
*   Siga a "Ordem de Implementação Sugerida" numerada abaixo. Para cada item, use o `Prompt_Implementador_Mestre` correspondente.
*   **Para obter os detalhes de CADA tarefa (responsabilidades, dependências, tecnologias), consulte SEMPRE e EXCLUSIVAMENTE o `@Blueprint_Arquitetural.md`, que é a nossa fonte única da verdade arquitetural.**

---

### Módulos Base (Para Ciência do Coordenador)

Os seguintes componentes fundamentais serão criados conforme necessário durante o desenvolvimento dos módulos principais. Eles não fazem parte da sequência de implementação numerada.

*   `fotix.domain.models` (Todos os modelos Pydantic)
*   `fotix.infrastructure.interfaces` (Todas as interfaces/ABCs)
*   `fotix.utils`
*   `fotix.app_config.py`

---

### Ordem de Implementação Sugerida (Módulos Principais e Pontos de Teste de Integração)

1.  `fotix.infrastructure.implementations.logging_service.LoggingService`
2.  `fotix.infrastructure.implementations.file_system_service.FileSystemService`
3.  `fotix.infrastructure.implementations.hashing_service.HashingService`
4.  `fotix.infrastructure.implementations.concurrency_service.ConcurrencyService`
5.  `fotix.infrastructure.implementations.zip_service.ZipService`
>>> PARADA PARA TESTES DE INTEGRAÇÃO (INFRAESTRUTURA DE PROCESSAMENTO DE ARQUIVOS) <<<
6.  `fotix.domain.core.duplicate_finder.DuplicateFinderEngine`
7.  `fotix.application.services.scan_service.ScanService`
>>> PARADA PARA TESTES DE INTEGRAÇÃO (FLUXO DE ESCANEAMENTO DE BACKEND) <<<
8.  `fotix.infrastructure.implementations.backup_service.BackupService`
9.  `fotix.domain.core.selection_strategy.SelectionStrategy`
10. `fotix.application.services.duplicate_management_service.DuplicateManagementService`
>>> PARADA PARA TESTES DE INTEGRAÇÃO (FLUXO DE GERENCIAMENTO DE DUPLICATAS) <<<
11. `fotix.application.services.restore_service.RestoreService`
12. `fotix.application.services.configuration_service.ConfigurationService`
13. `fotix.application.services.reporting_service.ReportingService`
>>> PARADA PARA TESTES DE INTEGRAÇÃO (FLUXOS DE RESTAURAÇÃO E CONFIGURAÇÃO) <<<
14. `fotix.ui.main_window.MainWindow`
15. `fotix.ui.dialogs.settings_dialog.SettingsDialog`
16. `fotix.ui.views.directory_selection_view.DirectorySelectionView`
17. `fotix.ui.views.scan_progress_view.ScanProgressView`
>>> PARADA PARA TESTES DE INTEGRAÇÃO (UI - FLUXO DE INÍCIO DE ESCANEAMENTO) <<<
18. `fotix.ui.views.results_view.ResultsView`
>>> PARADA PARA TESTES DE INTEGRAÇÃO (UI - FLUXO DE REVISÃO E REMOÇÃO) <<<
19. `fotix.ui.views.backup_restore_view.BackupRestoreView`
20. `fotix.ui.views.log_view.LogView`
>>> PARADA PARA TESTES DE INTEGRAÇÃO (UI - FLUXOS DE RESTAURAÇÃO E LOGS) <<<