## Cenários de Teste de Aceitação do Usuário (UAT) para Fotix

Aqui estão os cenários de teste manuais para validar as funcionalidades principais do Fotix da perspectiva do usuário final:

---

**ID do Cenário:** UAT_FTX_001
**Título do Cenário:** Fluxo Completo - Scan Básico, Identificação, Seleção Manual, Backup e Deleção Segura
**Objetivo do Teste:** Validar o fluxo principal da aplicação: selecionar um diretório, escanear por duplicatas, visualizar os resultados, selecionar manualmente um arquivo para manter, e confirmar a ação de backup e deleção segura (lixeira) dos demais.
**Módulos/Funcionalidades Principais Envolvidas:**
*   `fotix.ui.main_window`
*   `fotix.application.services.scan_service`
*   `fotix.application.services.duplicate_management_service`
*   `fotix.core.duplicate_finder`
*   `fotix.infrastructure.file_system`
*   `fotix.infrastructure.backup`
*   `fotix.core.models`
**Pré-condições:**
1.  A aplicação Fotix está instalada e em execução.
2.  O diretório de backup está configurado (ou um padrão é usado e é conhecido).
3.  Existe um diretório de teste (`C:\FotixTestData\Scenario001`) contendo:
    *   `imageA.jpg` (ex: 1MB, foto de um gato)
    *   `imageB.jpg` (cópia exata de `imageA.jpg`)
    *   `documentX.pdf` (ex: 500KB, um PDF qualquer)
    *   `imageA_copy.jpg` (outra cópia exata de `imageA.jpg`, em um subdiretório `C:\FotixTestData\Scenario001\Subfolder`)
**Dados de Teste Sugeridos:** Conforme descrito nas pré-condições.
**Passos para Execução:**
1.  Na interface principal do Fotix, clique no botão "Adicionar Diretório para Scan".
2.  Navegue e selecione o diretório `C:\FotixTestData\Scenario001`.
3.  Verifique se o caminho `C:\FotixTestData\Scenario001` aparece na lista de locais a serem escaneados.
4.  Clique no botão "Iniciar Scan".
5.  Observe a barra de progresso (se houver) e/ou mensagens de status.
6.  Após a conclusão do scan, verifique a área de resultados.
7.  Selecione o conjunto de duplicatas que contém `imageA.jpg`, `imageB.jpg` e `Subfolder\imageA_copy.jpg`.
8.  Na lista de arquivos deste conjunto, marque `imageA.jpg` como o arquivo a ser mantido (ex: através de um checkbox ou botão "Manter este").
9.  Clique no botão "Processar Duplicatas Selecionadas" ou similar.
10. Confirme a ação na caixa de diálogo de confirmação, que deve informar sobre backup e envio para lixeira.
**Resultado Esperado:**
1.  Um diálogo de seleção de diretório é exibido.
2.  O diretório `C:\FotixTestData\Scenario001` é adicionado à lista de locais.
3.  A UI indica que o scan está em andamento. Logs (se visíveis/configurados) mostram atividade de scan.
4.  A UI exibe um conjunto de duplicatas contendo os três arquivos de imagem idênticos. O arquivo `documentX.pdf` não deve ser listado como duplicata (a menos que haja outra cópia dele).
5.  `imageA.jpg` é claramente marcado como "a manter", enquanto `imageB.jpg` e `Subfolder\imageA_copy.jpg` são marcados como "a remover/processar".
6.  Uma caixa de diálogo de confirmação é exibida.
7.  Após a confirmação:
    *   `imageA.jpg` permanece em `C:\FotixTestData\Scenario001`.
    *   `imageB.jpg` e `Subfolder\imageA_copy.jpg` não existem mais em seus locais originais.
    *   Verifique o diretório de backup configurado: ele deve conter cópias de `imageB.jpg` e `Subfolder\imageA_copy.jpg` (com metadados apropriados, se possível inspecionar).
    *   Verifique a lixeira do sistema: ela deve conter `imageB.jpg` e `Subfolder\imageA_copy.jpg`.
    *   A UI atualiza o status do conjunto de duplicatas como processado ou o remove da lista de ativos.
**Critério de Passagem Geral:** O scan identifica corretamente as duplicatas, a seleção manual é respeitada, os arquivos não selecionados são copiados para o backup e movidos para a lixeira, e o arquivo selecionado para manter permanece intacto.

---

**ID do Cenário:** UAT_FTX_002
**Título do Cenário:** Restauração de Arquivos a partir do Backup
**Objetivo do Teste:** Validar a funcionalidade de listar backups e restaurar arquivos previamente "deletados" (e backupeados).
**Módulos/Funcionalidades Principais Envolvidas:**
*   `fotix.ui.main_window` (seção de gerenciamento de backup)
*   `fotix.application.services.backup_restore_service`
*   `fotix.infrastructure.backup`
*   `fotix.infrastructure.file_system`
**Pré-condições:**
1.  O Cenário UAT_FTX_001 foi executado com sucesso, resultando em arquivos (`imageB.jpg`, `Subfolder\imageA_copy.jpg`) sendo enviados para backup.
2.  A aplicação Fotix está em execução.
**Dados de Teste Sugeridos:** O backup criado no UAT_FTX_001.
**Passos para Execução:**
1.  Na interface principal do Fotix, navegue para a seção de "Gerenciamento de Backups" ou "Restaurar Arquivos".
2.  A UI deve listar os backups disponíveis. Identifique o backup criado durante o UAT_FTX_001 (pode ser por data/hora ou ID).
3.  Selecione o backup correspondente.
4.  A UI deve mostrar os arquivos contidos nesse backup (`imageB.jpg`, `Subfolder\imageA_copy.jpg`).
5.  Selecione `imageB.jpg` para restauração.
6.  Escolha a opção de restaurar para o local original (se disponível) ou especifique `C:\FotixTestData\RestoredFiles` como novo local.
7.  Clique no botão "Restaurar Selecionados".
8.  Confirme a ação, se solicitado.
**Resultado Esperado:**
1.  A lista de backups é exibida, contendo o backup do UAT_FTX_001.
2.  Os detalhes do backup selecionado são mostrados, incluindo `imageB.jpg` e `Subfolder\imageA_copy.jpg`.
3.  Após a confirmação da restauração:
    *   Se restaurado para o local original: `imageB.jpg` reaparece em `C:\FotixTestData\Scenario001`.
    *   Se restaurado para novo local: `imageB.jpg` aparece em `C:\FotixTestData\RestoredFiles`.
    *   O arquivo restaurado deve ser idêntico ao original.
    *   O arquivo permanece no backup (restauração é uma cópia do backup).
    *   A UI informa o sucesso da restauração.
**Critério de Passagem Geral:** O usuário consegue listar backups, selecionar arquivos de um backup e restaurá-los com sucesso para o local desejado, com integridade de dados.

---

**ID do Cenário:** UAT_FTX_003
**Título do Cenário:** Scan Incluindo Arquivos ZIP e Detecção de Duplicatas Trans-arquivo/ZIP
**Objetivo do Teste:** Validar que o Fotix pode escanear o conteúdo de arquivos ZIP e identificar duplicatas entre arquivos normais e arquivos dentro de ZIPs.
**Módulos/Funcionalidades Principais Envolvidas:**
*   `fotix.ui.main_window`
*   `fotix.application.services.scan_service`
*   `fotix.core.duplicate_finder`
*   `fotix.infrastructure.zip_handler`
*   `fotix.infrastructure.file_system`
**Pré-condições:**
1.  A aplicação Fotix está instalada e em execução.
2.  Existe um diretório de teste (`C:\FotixTestData\Scenario003`) contendo:
    *   `photo_XYZ.png` (ex: 2MB, uma imagem qualquer)
    *   `archive.zip` contendo:
        *   `inner_photo_XYZ.png` (cópia exata de `photo_XYZ.png`)
        *   `another_file.txt` (um arquivo de texto qualquer)
    *   `unique_video.mp4` (um arquivo de vídeo qualquer)
**Dados de Teste Sugeridos:** Conforme descrito nas pré-condições.
**Passos para Execução:**
1.  Na UI do Fotix, adicione o diretório `C:\FotixTestData\Scenario003` para scan.
2.  Certifique-se de que a opção "Incluir arquivos ZIP" (ou similar) esteja habilitada (geralmente por padrão ou configurável).
3.  Inicie o scan.
4.  Após a conclusão, examine os resultados.
**Resultado Esperado:**
1.  O scan é concluído.
2.  A UI exibe um conjunto de duplicatas contendo:
    *   `C:\FotixTestData\Scenario003\photo_XYZ.png`
    *   `C:\FotixTestData\Scenario003\archive.zip -> inner_photo_XYZ.png` (ou uma representação similar indicando o arquivo dentro do ZIP).
3.  `unique_video.mp4` e `archive.zip -> another_file.txt` não devem ser listados como parte deste conjunto de duplicatas (a menos que tenham outras cópias).
**Critério de Passagem Geral:** O Fotix escaneia corretamente o conteúdo de arquivos ZIP e identifica duplicatas entre arquivos no sistema de arquivos e arquivos dentro de ZIPs.

---

**ID do Cenário:** UAT_FTX_004
**Título do Cenário:** Aplicação de Estratégia de Seleção Automática (Ex: Manter Mais Antigo)
**Objetivo do Teste:** Validar que o usuário pode aplicar uma estratégia de seleção automática e que ela seleciona corretamente o arquivo a ser mantido.
**Módulos/Funcionalidades Principais Envolvidas:**
*   `fotix.ui.main_window`
*   `fotix.application.services.duplicate_management_service`
*   `fotix.core.selection_strategy` (implementação específica, ex: `KeepOldestStrategy`)
*   `fotix.core.models.FileInfo` (com metadados de data)
**Pré-condições:**
1.  A aplicação Fotix está em execução.
2.  Existe um diretório de teste (`C:\FotixTestData\Scenario004`) com arquivos duplicados criados/modificados em datas diferentes:
    *   `report_final.docx` (Modificado: 01/01/2023)
    *   `report_final_backup.docx` (Cópia de `report_final.docx`, Modificado: 15/01/2023)
    *   `report_final_v2.docx` (Cópia de `report_final.docx`, Modificado: 01/02/2023)
    *(Nota: O Coordenador precisará garantir que os metadados de data de modificação/criação sejam distintos e verificáveis.)*
3.  O diretório `C:\FotixTestData\Scenario004` foi escaneado e o conjunto de duplicatas dos três arquivos `report_*.docx` é exibido.
**Dados de Teste Sugeridos:** Conforme descrito nas pré-condições.
**Passos para Execução:**
1.  Selecione o conjunto de duplicatas contendo os arquivos `report_*.docx`.
2.  Na UI, localize a opção de aplicar uma estratégia de seleção (ex: um menu dropdown).
3.  Selecione a estratégia "Manter o arquivo mais antigo".
4.  Clique em "Aplicar Estratégia" ou a seleção ocorra automaticamente.
5.  Observe qual arquivo é marcado para ser mantido.
6.  (Opcional, mas recomendado) Prossiga com o processamento das duplicatas (backup e lixeira) e verifique o resultado.
**Resultado Esperado:**
1.  A estratégia "Manter o arquivo mais antigo" é aplicada.
2.  O arquivo `report_final.docx` (com data de modificação 01/01/2023) é automaticamente marcado como o arquivo a ser mantido.
3.  Os arquivos `report_final_backup.docx` e `report_final_v2.docx` são marcados para remoção/processamento.
4.  Se o processamento for continuado: `report_final.docx` permanece, os outros dois são backupeados e enviados à lixeira.
**Critério de Passagem Geral:** A estratégia de seleção automática "Manter o arquivo mais antigo" identifica e seleciona corretamente o arquivo apropriado com base nos metadados de data.

---

**ID do Cenário:** UAT_FTX_005
**Título do Cenário:** Tratamento de Erro - Diretório de Scan Inválido/Inacessível
**Objetivo do Teste:** Validar como a aplicação lida com a tentativa de escanear um diretório que não existe ou ao qual não tem permissão de acesso.
**Módulos/Funcionalidades Principais Envolvidas:**
*   `fotix.ui.main_window`
*   `fotix.application.services.scan_service`
*   `fotix.infrastructure.file_system` (tratamento de exceções)
**Pré-condições:**
1.  A aplicação Fotix está instalada e em execução.
**Dados de Teste Sugeridos:** Um caminho para um diretório sabidamente inexistente (ex: `C:\NaoExisteEsteDir123`) ou um diretório para o qual o usuário atual não tenha permissões de leitura.
**Passos para Execução:**
1.  Na interface principal do Fotix, clique no botão "Adicionar Diretório para Scan".
2.  Digite manualmente ou tente navegar para o caminho inválido/inacessível (ex: `C:\NaoExisteEsteDir123`).
3.  Tente adicionar este caminho à lista de scan.
4.  Se o caminho for adicionado, prossiga e clique em "Iniciar Scan".
**Resultado Esperado:**
*   **Idealmente na adição:** A UI deve impedir a adição de um caminho claramente inválido ou exibir um erro imediato.
*   **Se a adição for permitida e o scan iniciado:**
    *   A aplicação NÃO deve travar ou fechar inesperadamente.
    *   Uma mensagem de erro clara e amigável deve ser exibida ao usuário, informando que o diretório `C:\NaoExisteEsteDir123` não pôde ser acessado/escaneado.
    *   O log da aplicação (se acessível) deve registrar o erro (ex: `FileNotFoundError`, `PermissionError`).
    *   A aplicação deve permanecer em um estado estável, permitindo que o usuário continue outras operações (ex: adicionar um diretório válido).
**Critério de Passagem Geral:** A aplicação lida graciosamente com caminhos de scan inválidos ou inacessíveis, informando o usuário do problema sem travar e permitindo a continuidade do uso.

---

**ID do Cenário:** UAT_FTX_006
**Título do Cenário:** Operação com Grande Volume de Arquivos - Desempenho e Feedback ao Usuário
**Objetivo do Teste:** Avaliar a responsividade da UI, o feedback de progresso e o uso de recursos ao escanear um diretório com um grande número de arquivos e/ou arquivos grandes.
**Módulos/Funcionalidades Principais Envolvidas:**
*   `fotix.ui.main_window` (feedback de progresso, responsividade)
*   `fotix.application.services.scan_service`
*   `fotix.infrastructure.concurrency` (para processamento paralelo/concorrente)
*   `fotix.core.duplicate_finder`
**Pré-condições:**
1.  A aplicação Fotix está instalada e em execução.
2.  Existe um diretório de teste (`C:\FotixTestData\LargeVolume`) contendo uma grande quantidade de arquivos (ex: 10.000+ arquivos, totalizando vários GBs). Podem ser arquivos reais ou cópias de um conjunto menor de arquivos para simular volume e potenciais duplicatas.
**Dados de Teste Sugeridos:** Conforme descrito nas pré-condições.
**Passos para Execução:**
1.  Na UI do Fotix, adicione o diretório `C:\FotixTestData\LargeVolume` para scan.
2.  Inicie o scan.
3.  Durante o scan:
    *   Observe a barra de progresso ou indicadores de status. Eles estão atualizando?
    *   Tente interagir minimamente com a UI (ex: mover a janela, tentar clicar em um menu desabilitado). A UI permanece responsiva ou congela?
    *   Monitore (opcionalmente, usando o Gerenciador de Tarefas do SO) o uso de CPU e memória da aplicação.
4.  Aguarde a conclusão do scan.
**Resultado Esperado:**
1.  O scan é iniciado.
2.  A UI fornece feedback de progresso contínuo e razoavelmente preciso (ex: percentual concluído, número de arquivos processados).
3.  A UI permanece razoavelmente responsiva, não congelando completamente durante o processamento intensivo. (Pequenos atrasos podem ser aceitáveis, mas congelamento total não.)
4.  O uso de CPU e memória é significativo, mas não excessivo ao ponto de desestabilizar o sistema (considerando a natureza da tarefa).
5.  O scan é concluído com sucesso, e os resultados (mesmo que muitos) são eventualmente exibidos ou um resumo é fornecido.
**Critério de Passagem Geral:** A aplicação consegue lidar com um grande volume de arquivos, fornecendo feedback adequado ao usuário, mantendo a UI responsiva e completando a operação sem uso excessivo de recursos ou travamentos.

---

**ID do Cenário:** UAT_FTX_007
**Título do Cenário:** Cancelamento de uma Operação de Scan em Andamento
**Objetivo do Teste:** Validar que uma operação de scan longa pode ser cancelada pelo usuário e que a aplicação retorna a um estado estável.
**Módulos/Funcionalidades Principais Envolvidas:**
*   `fotix.ui.main_window` (botão de cancelar)
*   `fotix.application.services.scan_service` (lógica de cancelamento)
*   `fotix.infrastructure.concurrency` (gerenciamento de tarefas canceláveis)
**Pré-condições:**
1.  A aplicação Fotix está instalada e em execução.
2.  O scan do diretório `C:\FotixTestData\LargeVolume` (do UAT_FTX_006) está configurado para ser iniciado, ou qualquer scan que se espera demorar um tempo razoável (ex: > 30 segundos).
**Dados de Teste Sugeridos:** O diretório `C:\FotixTestData\LargeVolume`.
**Passos para Execução:**
1.  Inicie o scan do diretório `C:\FotixTestData\LargeVolume`.
2.  Enquanto o scan estiver em progresso (ex: após alguns segundos, mas antes da conclusão), clique no botão "Cancelar Scan" (ou similar).
3.  Observe a resposta da aplicação.
**Resultado Esperado:**
1.  O scan é iniciado e o progresso é visível.
2.  Após clicar em "Cancelar Scan":
    *   A operação de scan para em um tempo razoável (não instantaneamente, mas não continua indefinidamente).
    *   A UI atualiza seu estado para indicar que o scan foi cancelado (ex: barra de progresso para, status muda para "Cancelado").
    *   Nenhum resultado parcial (ou resultados claramente marcados como parciais/incompletos) é exibido, ou os resultados anteriores são limpos.
    *   A aplicação permanece estável e pronta para novas operações (ex: iniciar um novo scan, fechar a aplicação).
    *   Não há erros inesperados ou travamentos.
**Critério de Passagem Geral:** O usuário pode cancelar uma operação de scan em andamento, e a aplicação responde adequadamente, interrompendo a tarefa e retornando a um estado utilizável sem erros.

---

**ID do Cenário:** UAT_FTX_008
**Título do Cenário:** Scan de Diretório Sem Duplicatas
**Objetivo do Teste:** Validar que a aplicação se comporta corretamente quando nenhum arquivo duplicado é encontrado.
**Módulos/Funcionalidades Principais Envolvidas:**
*   `fotix.ui.main_window`
*   `fotix.application.services.scan_service`
*   `fotix.core.duplicate_finder`
**Pré-condições:**
1.  A aplicação Fotix está instalada e em execução.
2.  Existe um diretório de teste (`C:\FotixTestData\Scenario008`) contendo apenas arquivos únicos:
    *   `unique_text.txt`
    *   `another_image.png`
    *   `different_doc.pdf`
**Dados de Teste Sugeridos:** Conforme descrito nas pré-condições.
**Passos para Execução:**
1.  Na UI do Fotix, adicione o diretório `C:\FotixTestData\Scenario008` para scan.
2.  Inicie o scan.
3.  Após a conclusão do scan, observe a área de resultados.
**Resultado Esperado:**
1.  O scan é concluído.
2.  A UI exibe uma mensagem clara indicando que "Nenhum arquivo duplicado foi encontrado" ou similar.
3.  A área de listagem de duplicatas está vazia ou exibe essa mensagem.
4.  A aplicação permanece estável.
**Critério de Passagem Geral:** O Fotix identifica corretamente a ausência de duplicatas e informa o usuário de forma clara.

---

**ID do Cenário:** UAT_FTX_009
**Título do Cenário:** Aplicação de Estratégia de Seleção Automática (Ex: Manter Mais Recente por Nome)
**Objetivo do Teste:** Validar uma estratégia de seleção diferente, por exemplo, manter o arquivo com o nome lexicograficamente maior (ou que pareça ser uma versão mais recente por um sufixo numérico, se a estratégia for sofisticada). Usaremos "Manter por Nome (Ordem Alfabética Descendente)" como exemplo simples.
**Módulos/Funcionalidades Principais Envolvidas:**
*   `fotix.ui.main_window`
*   `fotix.application.services.duplicate_management_service`
*   `fotix.core.selection_strategy` (implementação específica, ex: `KeepByNameStrategy` com critério de ordem)
**Pré-condições:**
1.  A aplicação Fotix está em execução.
2.  Existe um diretório de teste (`C:\FotixTestData\Scenario009`) com arquivos duplicados com nomes diferentes:
    *   `photo_final.jpg` (Cópia X)
    *   `photo_final_v2.jpg` (Cópia X)
    *   `photo_candidate.jpg` (Cópia X)
3.  O diretório `C:\FotixTestData\Scenario009` foi escaneado e o conjunto de duplicatas é exibido.
**Dados de Teste Sugeridos:** Conforme descrito nas pré-condições.
**Passos para Execução:**
1.  Selecione o conjunto de duplicatas contendo os arquivos `photo_*.jpg`.
2.  Na UI, localize a opção de aplicar uma estratégia de seleção.
3.  Selecione a estratégia "Manter por Nome (Mais Recente/Maior Alfabeticamente)" (ou a estratégia de nome disponível que escolher o arquivo com "v2" ou o maior nome).
4.  Clique em "Aplicar Estratégia" ou a seleção ocorra automaticamente.
5.  Observe qual arquivo é marcado para ser mantido.
**Resultado Esperado:**
1.  A estratégia de nome é aplicada.
2.  O arquivo `photo_final_v2.jpg` (assumindo que é o "maior" nome na ordem lexicográfica ou pela lógica da estratégia) é automaticamente marcado como o arquivo a ser mantido.
3.  Os arquivos `photo_final.jpg` e `photo_candidate.jpg` são marcados para remoção/processamento.
**Critério de Passagem Geral:** A estratégia de seleção automática baseada em nome (ou um critério similar disponível) identifica e seleciona corretamente o arquivo apropriado.

---

**ID do Cenário:** UAT_FTX_010
**Título do Cenário:** Deleção de um Backup Existente
**Objetivo do Teste:** Validar a funcionalidade de deletar um backup específico previamente criado.
**Módulos/Funcionalidades Principais Envolvidas:**
*   `fotix.ui.main_window` (seção de gerenciamento de backup)
*   `fotix.application.services.backup_restore_service` (indiretamente, se a UI usar um serviço que chama `IBackupService.delete_backup`)
*   `fotix.infrastructure.backup.IBackupService`
**Pré-condições:**
1.  O Cenário UAT_FTX_001 (ou outro que crie um backup) foi executado com sucesso. Pelo menos um backup existe.
2.  A aplicação Fotix está em execução.
**Dados de Teste Sugeridos:** Um ID de backup existente, visível na lista de backups.
**Passos para Execução:**
1.  Na interface principal do Fotix, navegue para a seção de "Gerenciamento de Backups".
2.  A UI deve listar os backups disponíveis. Identifique um backup para deletar.
3.  Selecione o backup.
4.  Clique no botão "Deletar Backup Selecionado" (ou similar).
5.  Confirme a ação na caixa de diálogo de confirmação.
**Resultado Esperado:**
1.  A lista de backups é exibida.
2.  Uma caixa de diálogo de confirmação é exibida antes da deleção.
3.  Após a confirmação:
    *   O backup selecionado não é mais listado na UI.
    *   Os arquivos físicos do backup são removidos do diretório de backup no sistema de arquivos.
    *   A UI informa o sucesso da deleção.
**Critério de Passagem Geral:** O usuário consegue deletar um backup existente, e tanto a representação na UI quanto os arquivos físicos do backup são removidos.

---

**ID do Cenário:** UAT_FTX_011
**Título do Cenário:** Múltiplos Conjuntos de Duplicatas e Navegação
**Objetivo do Teste:** Validar a capacidade da aplicação de lidar e exibir múltiplos conjuntos de arquivos duplicados e permitir que o usuário navegue entre eles.
**Módulos/Funcionalidades Principais Envolvidas:**
*   `fotix.ui.main_window` (exibição e navegação de resultados)
*   `fotix.application.services.scan_service`
*   `fotix.core.duplicate_finder`
**Pré-condições:**
1.  A aplicação Fotix está instalada e em execução.
2.  Existe um diretório de teste (`C:\FotixTestData\Scenario011`) contendo múltiplos conjuntos de duplicatas:
    *   `docA_v1.pdf`, `docA_v2.pdf` (cópias idênticas)
    *   `imageX_small.jpg`, `imageX_large.jpg` (cópias idênticas)
    *   `song_draft.mp3`, `song_final.mp3` (cópias idênticas)
    *   `unique_file.txt`
**Dados de Teste Sugeridos:** Conforme descrito nas pré-condições.
**Passos para Execução:**
1.  Na UI do Fotix, adicione o diretório `C:\FotixTestData\Scenario011` para scan.
2.  Inicie o scan.
3.  Após a conclusão do scan, observe a área de resultados.
4.  Verifique se todos os três conjuntos de duplicatas são listados.
5.  Tente selecionar o primeiro conjunto (`docA_*.pdf`), visualizar seus arquivos.
6.  Tente selecionar o segundo conjunto (`imageX_*.jpg`), visualizar seus arquivos.
7.  Tente selecionar o terceiro conjunto (`song_*.mp3`), visualizar seus arquivos.
**Resultado Esperado:**
1.  O scan é concluído.
2.  A UI exibe três conjuntos de duplicatas distintos, correspondentes aos arquivos PDF, JPG e MP3.
3.  O usuário consegue selecionar cada conjunto de duplicatas individualmente.
4.  Ao selecionar um conjunto, os arquivos membros desse conjunto são exibidos corretamente para inspeção e seleção.
5.  A navegação entre os conjuntos é clara e funcional.
**Critério de Passagem Geral:** O Fotix identifica e exibe corretamente múltiplos conjuntos de duplicatas, permitindo que o usuário navegue e inspecione cada conjunto de forma independente.

---

**ID do Cenário:** UAT_FTX_012
**Título do Cenário:** Tratamento de Erro - Falha ao Mover para Lixeira/Backup
**Objetivo do Teste:** Validar como a aplicação lida com uma falha ao tentar mover um arquivo para a lixeira ou realizar o backup (ex: permissão negada no destino do backup, lixeira cheia/desabilitada, arquivo bloqueado).
**Módulos/Funcionalidades Principais Envolvidas:**
*   `fotix.ui.main_window`
*   `fotix.application.services.duplicate_management_service`
*   `fotix.infrastructure.file_system` (operações de mover/copiar e tratamento de exceções)
*   `fotix.infrastructure.backup` (operações de cópia e tratamento de exceções)
**Pré-condições:**
1.  A aplicação Fotix está em execução.
2.  Um scan foi realizado e um conjunto de duplicatas está pronto para processamento.
3.  O Coordenador deve tentar simular uma condição de falha (isso pode ser difícil de fazer de forma controlada e segura):
    *   *Para falha de backup:* Tornar o diretório de backup somente leitura temporariamente (se possível e seguro).
    *   *Para falha de lixeira:* Tentar excluir um arquivo que está atualmente aberto/bloqueado por outro programa. (Nota: `send2trash` pode ter seu próprio tratamento para isso).
    *   *Alternativa:* Este cenário pode ser mais focado em observar se a aplicação tem mecanismos de log/feedback para erros inesperados nessas operações, mesmo que a simulação seja imperfeita.
**Dados de Teste Sugeridos:** Um conjunto de duplicatas qualquer. Um arquivo que possa ser bloqueado (ex: abrir um dos arquivos a serem "deletados" em outro aplicativo).
**Passos para Execução:**
1.  Prepare o ambiente para a potencial falha (ex: bloqueie um arquivo, altere permissões do diretório de backup se souber como e for seguro).
2.  No Fotix, selecione um arquivo para manter e marque os outros para processamento no conjunto de duplicatas.
3.  Clique para processar as duplicatas (backup e lixeira).
4.  Observe a resposta da aplicação.
**Resultado Esperado:**
1.  A aplicação NÃO deve travar ou fechar inesperadamente.
2.  Uma mensagem de erro clara e amigável deve ser exibida ao usuário, informando sobre a falha na operação de backup ou envio para lixeira para o(s) arquivo(s) específico(s).
3.  Os arquivos que puderam ser processados com sucesso são processados. Os arquivos que falharam devem permanecer em seus locais originais (ou o estado deve ser claramente comunicado).
4.  O log da aplicação (se acessível) deve registrar o erro específico (ex: `PermissionError` no backup, erro do `send2trash`).
5.  A aplicação deve permanecer em um estado estável, permitindo que o usuário tente outras operações ou corrija o problema subjacente.
**Critério de Passagem Geral:** A aplicação lida graciosamente com falhas durante as operações de backup ou envio para lixeira, informando o usuário do problema específico sem travar, e deixando os arquivos não processados em um estado consistente.