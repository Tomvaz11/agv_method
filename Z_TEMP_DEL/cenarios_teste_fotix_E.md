Okay, Coordenador! Com base nos artefatos fornecidos, aqui estão os cenários de teste de aceitação do usuário (UAT) / End-to-End (E2E) manuais para o projeto Fotix.

---

## Cenários de Teste de Aceitação do Usuário (UAT) / E2E Manuais para Fotix

**Nome do Projeto (Inferido):** Fotix
**Objetivo Principal do Projeto (Inferido):** Aplicação desktop para identificar e gerenciar arquivos duplicados, com funcionalidades de backup e restauração para garantir a segurança dos dados do usuário.
**Tipo de Interface Principal com o Usuário (Inferido):** GUI (Graphical User Interface) Desktop.

---

**ID do Cenário:** `UAT_FOTIX_001`
**Título do Cenário:** Escaneamento Básico, Identificação, Seleção Manual e Remoção de Duplicatas com Backup.
**Objetivo do Teste:** Validar o fluxo principal: escanear um diretório, identificar arquivos duplicados, permitir que o usuário selecione manualmente qual arquivo manter, mover os outros para a lixeira e verificar se um backup dos arquivos removidos foi criado.
**Módulos/Funcionalidades Principais Envolvidas:** `fotix.ui` (Interação do Usuário), `fotix.application.services.ScanService`, `fotix.application.services.DuplicateManagementService`, `fotix.core.DuplicateFinder`, `fotix.core.SelectionStrategy` (implícita na seleção manual), `fotix.infrastructure.FileSystemService`, `fotix.infrastructure.BackupService`, `fotix.infrastructure.ConcurrencyService`.
**Pré-condições:**
1.  A aplicação Fotix está instalada e pode ser iniciada.
2.  O diretório de backup está configurado e acessível (ex: `C:\FotixBackups` ou similar).
3.  O usuário preparou um diretório de teste com a seguinte estrutura e arquivos:
    *   `C:\FotixTestData\ScanDir1\`
        *   `imageA.jpg` (ex: 1MB, foto de um gato)
        *   `documentX.txt` (ex: 1KB, texto "Arquivo único")
    *   `C:\FotixTestData\ScanDir1\SubfolderA\`
        *   `imageA_copy.jpg` (cópia exata de `C:\FotixTestData\ScanDir1\imageA.jpg`)
    *   `C:\FotixTestData\ScanDir1\SubfolderB\`
        *   `imageA_another_copy.png` (cópia exata de `C:\FotixTestData\ScanDir1\imageA.jpg`, mas com nome e extensão diferentes para testar hash)
        *   `archive.zip` (contendo `imageZ.jpg` - um arquivo diferente dos imageA)

**Dados de Teste Sugeridos:** Conforme descrito nas Pré-condições.
**Passos para Execução:**
1.  Inicie a aplicação Fotix.
2.  Na interface principal, localize a funcionalidade para adicionar um diretório para escaneamento.
3.  Adicione o diretório `C:\FotixTestData\ScanDir1` à lista de escaneamento.
4.  Inicie o processo de escaneamento (ex: clicando em um botão "Escanear" ou "Procurar Duplicatas").
5.  Aguarde a conclusão do escaneamento. A UI deve indicar o progresso e a finalização.
6.  A UI deve exibir uma lista ou visualização dos conjuntos de arquivos duplicados encontrados.
7.  Localize o conjunto de duplicatas que contém `imageA.jpg`, `imageA_copy.jpg`, e `imageA_another_copy.png`.
8.  Dentro deste conjunto, selecione `imageA.jpg` (o original em `ScanDir1`) como o arquivo a ser mantido. Os outros (`imageA_copy.jpg`, `imageA_another_copy.png`) devem ser marcados para remoção.
9.  Inicie o processo de remoção das duplicatas selecionadas (ex: botão "Processar Selecionados", "Remover Duplicatas Marcadas").
10. Se uma caixa de diálogo de confirmação aparecer, confirme a ação.
11. Aguarde a conclusão do processo. A UI deve indicar que a operação foi finalizada.

**Resultado Esperado (para cada passo ou grupo de passos chave):**
*   (Passo 4-5): O escaneamento é concluído com sucesso. Logs (se visíveis ou verificáveis) indicam varredura, hashing e comparação.
*   (Passo 6-7):
    *   O conjunto de duplicatas contendo `imageA.jpg`, `imageA_copy.jpg`, e `imageA_another_copy.png` é corretamente identificado e exibido.
    *   O arquivo `documentX.txt` não é listado como duplicata.
    *   O arquivo `imageZ.jpg` (dentro do `archive.zip`) não é listado como duplicata de `imageA` (a menos que a opção de escanear ZIPs não esteja habilitada ou seja um teste separado). *Nota: Ajustar se o escaneamento de ZIPs é padrão ou opcional.*
*   (Passo 8): A seleção do usuário é refletida na UI (ex: `imageA.jpg` marcado como "manter", os outros como "remover/excluir").
*   (Passo 9-11):
    *   Os arquivos `C:\FotixTestData\ScanDir1\SubfolderA\imageA_copy.jpg` e `C:\FotixTestData\ScanDir1\SubfolderB\imageA_another_copy.png` são movidos para a lixeira do sistema operacional.
    *   O arquivo `C:\FotixTestData\ScanDir1\imageA.jpg` permanece em seu local original.
    *   No diretório de backup configurado (ex: `C:\FotixBackups`), um novo backup é criado contendo cópias de `imageA_copy.jpg` e `imageA_another_copy.png`, junto com quaisquer metadados que o Fotix salve.
    *   A UI é atualizada, possivelmente removendo o conjunto processado da lista de duplicatas ou marcando-o como resolvido.

**Critério de Passagem Geral:** O sistema identificou corretamente as duplicatas, permitiu a seleção do usuário, moveu os arquivos selecionados para a lixeira, manteve o arquivo escolhido, e criou um backup dos arquivos removidos. Nenhuma perda de dados não intencional ocorreu.

---

**ID do Cenário:** `UAT_FOTIX_002`
**Título do Cenário:** Escaneamento Incluindo Arquivos ZIP e Detecção de Duplicatas entre ZIP e Sistema de Arquivos.
**Objetivo do Teste:** Validar que o Fotix pode escanear arquivos dentro de arquivos ZIP e identificar duplicatas tanto entre arquivos dentro de diferentes ZIPs quanto entre um arquivo em um ZIP e um arquivo solto no sistema de arquivos.
**Módulos/Funcionalidades Principais Envolvidas:** `fotix.ui`, `fotix.application.services.ScanService`, `fotix.core.DuplicateFinder`, `fotix.infrastructure.ZipHandlerService`, `fotix.infrastructure.FileSystemService`.
**Pré-condições:**
1.  Fotix instalado e executando.
2.  Opção para escanear dentro de arquivos ZIP está habilitada (se for uma opção configurável na UI).
3.  Diretório de teste preparado:
    *   `C:\FotixTestData\ZipScan\`
        *   `photo_alpha.jpg` (ex: imagem de um carro)
        *   `archive1.zip` contendo:
            *   `photo_alpha_in_zip.jpg` (cópia exata de `C:\FotixTestData\ZipScan\photo_alpha.jpg`)
            *   `unique_doc_in_zip.pdf`
        *   `archive2.zip` contendo:
            *   `photo_alpha_in_another_zip.jpg` (cópia exata de `C:\FotixTestData\ZipScan\photo_alpha.jpg`)

**Dados de Teste Sugeridos:** Conforme descrito nas Pré-condições.
**Passos para Execução:**
1.  Inicie o Fotix.
2.  Configure o Fotix para escanear dentro de arquivos ZIP (se houver uma opção na UI; caso contrário, assume-se que é o comportamento padrão).
3.  Adicione o diretório `C:\FotixTestData\ZipScan\` para escaneamento.
4.  Inicie o escaneamento.
5.  Aguarde a conclusão.

**Resultado Esperado (para cada passo ou grupo de passos chave):**
*   (Passo 4-5): O escaneamento é concluído. Logs (se disponíveis) devem mostrar a interação com `ZipHandlerService`.
*   (Passo 5): A UI deve exibir um conjunto de duplicatas contendo:
    *   `C:\FotixTestData\ZipScan\photo_alpha.jpg`
    *   `archive1.zip -> photo_alpha_in_zip.jpg` (ou representação similar do caminho dentro do ZIP)
    *   `archive2.zip -> photo_alpha_in_another_zip.jpg` (ou representação similar)
*   O arquivo `unique_doc_in_zip.pdf` não deve ser listado como duplicata.

**Critério de Passagem Geral:** O sistema identificou corretamente as duplicatas, incluindo aquelas dentro de arquivos ZIP e entre arquivos ZIP e o sistema de arquivos regular.

---

**ID do Cenário:** `UAT_FOTIX_003`
**Título do Cenário:** Aplicação de Estratégia de Seleção Automática (Ex: Manter o Arquivo Mais Recente).
**Objetivo do Teste:** Validar que o Fotix pode aplicar uma estratégia de seleção automática (ex: manter o arquivo com data de modificação mais recente) para escolher qual arquivo manter de um conjunto de duplicatas.
**Módulos/Funcionalidades Principais Envolvidas:** `fotix.ui`, `fotix.application.services.DuplicateManagementService`, `fotix.core.SelectionStrategy` (implementação específica), `fotix.core.models.FileInfo`.
**Pré-condições:**
1.  Fotix instalado e executando.
2.  Um conjunto de duplicatas já identificado (pode ser resultado do UAT_FOTIX_001 ou um novo scan).
3.  Os arquivos no conjunto de duplicatas têm datas de modificação diferentes. Exemplo:
    *   `file_dup.txt` (Modificado: 01/01/2023 10:00)
    *   `file_dup_copy1.txt` (Modificado: 01/01/2023 12:00) <- Mais recente
    *   `file_dup_copy2.txt` (Modificado: 01/01/2023 09:00)
4.  A UI permite ao usuário escolher ou aplicar uma estratégia de seleção (ex: "Manter o mais recente").

**Dados de Teste Sugeridos:** Preparar 3 arquivos idênticos em conteúdo, mas com datas de modificação distintas conforme acima. Escaneá-los para que apareçam como um conjunto de duplicatas.
**Passos para Execução:**
1.  Com o conjunto de duplicatas (contendo `file_dup.txt`, `file_dup_copy1.txt`, `file_dup_copy2.txt`) exibido na UI.
2.  Localize e ative a funcionalidade para aplicar uma estratégia de seleção automática.
3.  Se houver múltiplas estratégias, selecione a estratégia "Manter o arquivo mais recente" (ou similar).
4.  Aplique a estratégia ao conjunto de duplicatas.
5.  Observe na UI qual arquivo foi automaticamente marcado para ser mantido e quais foram marcados para remoção.
6.  (Opcional, mas recomendado) Prossiga com a remoção (como no UAT_FOTIX_001, passos 9-11) para confirmar o resultado.

**Resultado Esperado (para cada passo ou grupo de passos chave):**
*   (Passo 4-5): A UI deve mostrar que `file_dup_copy1.txt` (o mais recente) está marcado para ser mantido, enquanto `file_dup.txt` e `file_dup_copy2.txt` estão marcados para remoção.
*   (Passo 6, se executado): `file_dup_copy1.txt` é mantido; os outros são movidos para a lixeira e backupeados.

**Critério de Passagem Geral:** A estratégia de seleção automática "Manter o mais recente" foi aplicada corretamente, identificando o arquivo correto para manter com base na sua data de modificação.

---

**ID do Cenário:** `UAT_FOTIX_004`
**Título do Cenário:** Listagem de Backups e Restauração de Arquivos de um Backup.
**Objetivo do Teste:** Validar que o usuário pode listar os backups existentes e restaurar arquivos de um backup específico para seu local original (ou um novo local, se suportado).
**Módulos/Funcionalidades Principais Envolvidas:** `fotix.ui`, `fotix.application.services.BackupRestoreService`, `fotix.infrastructure.BackupService`, `fotix.infrastructure.FileSystemService`.
**Pré-condições:**
1.  Fotix instalado e executando.
2.  Pelo menos um backup foi criado anteriormente (ex: como resultado do UAT_FOTIX_001). Suponha que o backup `BKUP_ID_XYZ` contém `imageA_copy.jpg` (originalmente em `C:\FotixTestData\ScanDir1\SubfolderA\`) e `imageA_another_copy.png` (originalmente em `C:\FotixTestData\ScanDir1\SubfolderB\`).
3.  Os arquivos originais (`imageA_copy.jpg` e `imageA_another_copy.png`) não existem mais em seus locais originais (foram movidos para a lixeira).

**Dados de Teste Sugeridos:** Utilizar um backup criado em um teste anterior.
**Passos para Execução:**
1.  Inicie o Fotix.
2.  Navegue até a seção de gerenciamento de backups na UI.
3.  A UI deve exibir uma lista dos backups disponíveis, incluindo `BKUP_ID_XYZ` com informações como data e número de arquivos.
4.  Selecione o backup `BKUP_ID_XYZ`.
5.  Escolha a opção para restaurar este backup.
6.  Se a aplicação perguntar, escolha restaurar para os locais originais. (Se permitir novo local, este seria um teste alternativo).
7.  Confirme a ação de restauração.
8.  Aguarde a conclusão do processo.

**Resultado Esperado (para cada passo ou grupo de passos chave):**
*   (Passo 3): A lista de backups é exibida corretamente, mostrando detalhes do `BKUP_ID_XYZ`.
*   (Passo 5-8):
    *   Os arquivos `imageA_copy.jpg` e `imageA_another_copy.png` são restaurados para seus respectivos diretórios originais:
        *   `C:\FotixTestData\ScanDir1\SubfolderA\imageA_copy.jpg`
        *   `C:\FotixTestData\ScanDir1\SubfolderB\imageA_another_copy.png`
    *   Verifique o conteúdo dos arquivos restaurados para garantir que são idênticos aos originais.
    *   A UI indica que a restauração foi bem-sucedida.

**Critério de Passagem Geral:** O usuário conseguiu listar os backups, selecionar um específico e restaurar com sucesso os arquivos contidos nele para seus locais originais. Os arquivos restaurados estão íntegros.

---

**ID do Cenário:** `UAT_FOTIX_005`
**Título do Cenário:** Exclusão de um Backup Específico.
**Objetivo do Teste:** Validar que o usuário pode selecionar e excluir permanentemente um backup específico do sistema.
**Módulos/Funcionalidades Principais Envolvidas:** `fotix.ui`, `fotix.application.services.BackupRestoreService`, `fotix.infrastructure.BackupService`.
**Pré-condições:**
1.  Fotix instalado e executando.
2.  Pelo menos dois backups existem, por exemplo, `BKUP_ID_XYZ` e `BKUP_ID_ABC`.

**Dados de Teste Sugeridos:** Utilizar backups criados em testes anteriores.
**Passos para Execução:**
1.  Inicie o Fotix.
2.  Navegue até a seção de gerenciamento de backups na UI.
3.  A lista de backups é exibida, mostrando `BKUP_ID_XYZ` e `BKUP_ID_ABC`.
4.  Selecione o backup `BKUP_ID_XYZ` para exclusão.
5.  Escolha a opção para excluir o backup selecionado.
6.  Confirme a ação de exclusão na caixa de diálogo (geralmente com um aviso de que a ação é irreversível).
7.  Aguarde a conclusão.

**Resultado Esperado (para cada passo ou grupo de passos chave):**
*   (Passo 6-7):
    *   O backup `BKUP_ID_XYZ` é removido da lista de backups na UI.
    *   Verifique no sistema de arquivos que o diretório/arquivos correspondentes a `BKUP_ID_XYZ` no local de armazenamento de backups foram removidos.
    *   O backup `BKUP_ID_ABC` permanece intacto e listado.

**Critério de Passagem Geral:** O backup selecionado foi excluído com sucesso tanto da UI quanto do sistema de armazenamento de backups, enquanto os outros backups não foram afetados.

---

**ID do Cenário:** `UAT_FOTIX_006`
**Título do Cenário:** Escaneamento de Diretório Vazio ou Sem Duplicatas.
**Objetivo do Teste:** Validar o comportamento da aplicação ao escanear um diretório que está vazio ou que contém apenas arquivos únicos (sem duplicatas).
**Módulos/Funcionalidades Principais Envolvidas:** `fotix.ui`, `fotix.application.services.ScanService`, `fotix.core.DuplicateFinder`.
**Pré-condições:**
1.  Fotix instalado e executando.
2.  Um diretório de teste preparado, `C:\FotixTestData\NoDuplicatesDir\`, contendo:
    *   `unique1.txt`
    *   `unique2.jpg`
    *   (Ou o diretório pode estar completamente vazio).

**Dados de Teste Sugeridos:** Conforme descrito nas Pré-condições.
**Passos para Execução:**
1.  Inicie o Fotix.
2.  Adicione o diretório `C:\FotixTestData\NoDuplicatesDir\` para escaneamento.
3.  Inicie o escaneamento.
4.  Aguarde a conclusão.

**Resultado Esperado (para cada passo ou grupo de passos chave):**
*   (Passo 3-4): O escaneamento é concluído.
*   (Passo 4): A UI deve indicar claramente que nenhuma duplicata foi encontrada (ex: uma mensagem "Nenhuma duplicata encontrada", ou uma lista de duplicatas vazia). A aplicação não deve travar ou apresentar erros.

**Critério de Passagem Geral:** A aplicação lida graciosamente com diretórios sem duplicatas, informando o usuário corretamente e sem erros.

---

**ID do Cenário:** `UAT_FOTIX_007`
**Título do Cenário:** Tentativa de Escanear um Caminho Inválido ou Inacessível.
**Objetivo do Teste:** Validar o tratamento de erro da aplicação quando o usuário tenta escanear um caminho de diretório que não existe ou para o qual não tem permissão de leitura.
**Módulos/Funcionalidades Principais Envolvidas:** `fotix.ui`, `fotix.application.services.ScanService`, `fotix.infrastructure.FileSystemService`.
**Pré-condições:**
1.  Fotix instalado e executando.

**Dados de Teste Sugeridos:**
*   Um caminho que definitivamente não existe: `C:\NonExistentPathXYZ123\`
*   (Opcional, mais difícil de simular consistentemente) Um caminho para o qual o usuário atual não tem permissões de leitura.

**Passos para Execução:**
1.  Inicie o Fotix.
2.  Tente adicionar o caminho `C:\NonExistentPathXYZ123\` à lista de escaneamento.
3.  (Se a adição for permitida) Tente iniciar o escaneamento.

**Resultado Esperado (para cada passo ou grupo de passos chave):**
*   (Passo 2 ou 3): A aplicação deve:
    *   Idealmente, impedir a adição de um caminho inválido com uma mensagem de erro clara na UI (ex: "Caminho não encontrado ou inválido.").
    *   Ou, se permitir a adição, ao tentar escanear, deve exibir uma mensagem de erro clara indicando que o caminho não pôde ser acessado/escaneado.
    *   A aplicação não deve travar ou se comportar de forma inesperada. Os logs devem registrar o erro.

**Critério de Passagem Geral:** A aplicação lida corretamente com caminhos inválidos ou inacessíveis, informando o usuário sobre o problema sem travar.

---

Estes cenários cobrem os principais fluxos de trabalho e algumas condições de borda para o Fotix. O Coordenador deve adaptá-los conforme necessário, com base na interface exata e nas funcionalidades implementadas.