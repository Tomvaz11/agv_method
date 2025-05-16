# Cenários de Teste de Aceitação do Usuário (UAT) - Fotix

## Visão Geral do Projeto

**Nome do Projeto:** Fotix  
**Objetivo Principal:** Gerenciar e eliminar arquivos duplicados, permitindo ao usuário identificar, visualizar e remover duplicatas de forma segura com opções de backup.  
**Interface Principal:** Interface Gráfica de Usuário (GUI) desenvolvida com PySide6 (Qt)

## Cenários de Teste

### UAT_FOTIX_001

**Título do Cenário:** Inicialização da Aplicação e Verificação da Interface Principal

**Objetivo do Teste:** Verificar se a aplicação Fotix inicia corretamente e apresenta todos os elementos principais da interface.

**Módulos/Funcionalidades Principais Envolvidas:**
- UI (main_window.py)
- Configuração (config.py)
- Infraestrutura (logging_config.py)

**Pré-condições:**
- Fotix está instalado no sistema
- O usuário tem permissões para executar a aplicação

**Dados de Teste Sugeridos:**
- N/A (Não são necessários dados específicos para este teste)

**Passos para Execução:**
1. Iniciar a aplicação Fotix através do comando `python -m fotix.main` ou atalho do sistema
2. Observar a janela principal que é exibida
3. Verificar a presença da barra de menus (Arquivo, Backup, Ajuda)
4. Verificar a presença da barra de ferramentas com os botões principais
5. Verificar a presença da área principal onde serão exibidas as duplicatas
6. Verificar a presença da barra de status na parte inferior da janela

**Resultado Esperado:**
- A aplicação deve iniciar sem erros
- A janela principal deve ser exibida com o título "Fotix - Gerenciador de Duplicatas"
- A barra de menus deve conter os menus Arquivo, Backup e Ajuda
- A barra de ferramentas deve conter botões para Escanear Diretórios, Gerenciar Backups, Restaurar Backup, Configurações e Ajuda
- A área principal deve estar vazia (sem duplicatas listadas)
- A barra de status deve exibir a mensagem "Pronto"

**Critério de Passagem Geral:**
O teste é considerado bem-sucedido se a aplicação iniciar sem erros e todos os elementos da interface mencionados estiverem presentes e visíveis.

### UAT_FOTIX_002

**Título do Cenário:** Escaneamento de Diretório em Busca de Duplicatas

**Objetivo do Teste:** Verificar se a aplicação consegue escanear um diretório e identificar arquivos duplicados corretamente.

**Módulos/Funcionalidades Principais Envolvidas:**
- UI (main_window.py, widgets/progress_dialog.py)
- Application (services/scan_service.py)
- Core (duplicate_finder.py, models.py)
- Infrastructure (file_system.py, zip_handler.py, concurrency.py)

**Pré-condições:**
- Fotix está em execução
- Existe um diretório com pelo menos dois arquivos duplicados (mesmo conteúdo)

**Dados de Teste Sugeridos:**
- Criar um diretório de teste com alguns arquivos duplicados:
  - Copiar uma mesma imagem várias vezes com nomes diferentes
  - Colocar cópias em subdiretórios diferentes
  - Incluir alguns arquivos únicos (não duplicados)

**Passos para Execução:**
1. Clicar no botão "Escanear Diretórios" na barra de ferramentas
2. No diálogo de seleção de diretório, navegar até o diretório de teste preparado
3. Selecionar o diretório e clicar em "Selecionar Pasta"
4. Observar o diálogo de progresso durante o escaneamento
5. Aguardar a conclusão do escaneamento

**Resultado Esperado:**
- O diálogo de seleção de diretório deve ser exibido
- Após selecionar o diretório, o diálogo de progresso deve ser exibido mostrando o andamento do escaneamento
- Após a conclusão, a lista de duplicatas deve ser exibida na área principal
- Cada conjunto de duplicatas deve mostrar o hash parcial, tamanho e número de arquivos
- Ao expandir um conjunto, todos os arquivos duplicados devem ser listados
- A barra de status deve exibir uma mensagem indicando o número de conjuntos de duplicatas encontrados

**Critério de Passagem Geral:**
O teste é considerado bem-sucedido se a aplicação conseguir escanear o diretório, identificar corretamente os arquivos duplicados e exibi-los na interface.

### UAT_FOTIX_003

**Título do Cenário:** Visualização e Seleção de Arquivos Duplicados

**Objetivo do Teste:** Verificar se a aplicação permite visualizar detalhes dos arquivos duplicados e selecionar qual arquivo manter.

**Módulos/Funcionalidades Principais Envolvidas:**
- UI (widgets/duplicate_list_widget.py, widgets/file_info_widget.py)
- Core (models.py)

**Pré-condições:**
- Fotix está em execução
- Um escaneamento foi realizado e duplicatas foram encontradas

**Dados de Teste Sugeridos:**
- Conjunto de duplicatas já identificado no cenário UAT_FOTIX_002

**Passos para Execução:**
1. Na lista de duplicatas, clicar em um conjunto para expandir e mostrar os arquivos
2. Clicar em um dos arquivos duplicados na lista
3. Observar as informações detalhadas do arquivo no painel lateral
4. Clicar em outro arquivo do mesmo conjunto
5. Observar as informações detalhadas do novo arquivo selecionado
6. Clicar com o botão direito em um dos arquivos
7. Verificar se o menu de contexto é exibido com a opção "Manter este arquivo"

**Resultado Esperado:**
- Ao clicar em um conjunto, ele deve expandir e mostrar todos os arquivos duplicados
- Ao selecionar um arquivo, o painel lateral deve mostrar informações detalhadas como:
  - Nome do arquivo
  - Caminho completo
  - Tamanho
  - Data de criação
  - Data de modificação
  - Outras informações relevantes (como resolução, se for uma imagem)
- Ao clicar com o botão direito em um arquivo, o menu de contexto deve ser exibido com a opção "Manter este arquivo"
- O botão "Processar Selecionado" deve ficar habilitado quando um arquivo estiver selecionado

**Critério de Passagem Geral:**
O teste é considerado bem-sucedido se a aplicação exibir corretamente os detalhes dos arquivos duplicados e permitir a seleção de qual arquivo manter.

### UAT_FOTIX_004

**Título do Cenário:** Processamento de Duplicatas (Manter um Arquivo e Remover Outros)

**Objetivo do Teste:** Verificar se a aplicação permite processar um conjunto de duplicatas, mantendo um arquivo selecionado e removendo os outros com backup.

**Módulos/Funcionalidades Principais Envolvidas:**
- UI (main_window.py, widgets/duplicate_list_widget.py, widgets/progress_dialog.py)
- Application (services/duplicate_management_service.py)
- Core (models.py, selection_strategy.py)
- Infrastructure (file_system.py, backup.py)

**Pré-condições:**
- Fotix está em execução
- Um escaneamento foi realizado e duplicatas foram encontradas
- O usuário tem permissões para excluir arquivos no diretório escaneado

**Dados de Teste Sugeridos:**
- Conjunto de duplicatas já identificado no cenário UAT_FOTIX_002

**Passos para Execução:**
1. Na lista de duplicatas, clicar em um conjunto para expandir e mostrar os arquivos
2. Clicar em um dos arquivos duplicados para selecioná-lo
3. Clicar no botão "Processar Selecionado"
4. No diálogo de confirmação, clicar em "Sim" para confirmar a ação
5. Observar o diálogo de progresso durante o processamento
6. Aguardar a conclusão do processamento
7. Verificar a mensagem de sucesso exibida
8. Verificar se o conjunto processado foi removido da lista de duplicatas

**Resultado Esperado:**
- Ao clicar em "Processar Selecionado", um diálogo de confirmação deve ser exibido
- Após confirmar, o diálogo de progresso deve ser exibido
- Após a conclusão, uma mensagem de sucesso deve ser exibida mostrando:
  - O arquivo que foi mantido
  - O número de arquivos removidos
  - O ID do backup criado
- O conjunto processado deve ser removido da lista de duplicatas
- A barra de status deve exibir uma mensagem indicando o sucesso da operação
- Os arquivos duplicados (exceto o selecionado) devem ser movidos para a lixeira do sistema

**Critério de Passagem Geral:**
O teste é considerado bem-sucedido se a aplicação processar corretamente o conjunto de duplicatas, mantendo o arquivo selecionado, removendo os outros para a lixeira e criando um backup.

### UAT_FOTIX_005

**Título do Cenário:** Configuração das Preferências da Aplicação

**Objetivo do Teste:** Verificar se a aplicação permite configurar as preferências e se as alterações são aplicadas corretamente.

**Módulos/Funcionalidades Principais Envolvidas:**
- UI (main_window.py, widgets/settings_dialog.py)
- Configuração (config.py)
- Infrastructure (concurrency.py)

**Pré-condições:**
- Fotix está em execução

**Dados de Teste Sugeridos:**
- Valor para número máximo de workers: 8 (ou outro valor diferente do padrão)
- Diretório personalizado para backups

**Passos para Execução:**
1. Clicar no botão "Configurações" na barra de ferramentas
2. No diálogo de configurações, alterar o número máximo de workers para 8
3. Alterar o diretório de backup para um diretório personalizado
4. Clicar em "Salvar" para aplicar as alterações
5. Fechar e reabrir a aplicação
6. Abrir novamente o diálogo de configurações
7. Verificar se as configurações alteradas foram mantidas

**Resultado Esperado:**
- O diálogo de configurações deve ser exibido com os valores atuais
- Deve ser possível alterar as configurações
- Ao salvar, a barra de status deve exibir a mensagem "Configurações atualizadas"
- Ao reabrir a aplicação e o diálogo de configurações, as alterações devem ser mantidas
- As configurações alteradas devem afetar o comportamento da aplicação (ex: número de workers durante o escaneamento)

**Critério de Passagem Geral:**
O teste é considerado bem-sucedido se a aplicação permitir alterar as configurações, salvar as alterações e aplicá-las corretamente.

### UAT_FOTIX_006

**Título do Cenário:** Visualização e Gerenciamento de Backups

**Objetivo do Teste:** Verificar se a aplicação permite visualizar e gerenciar os backups criados durante o processamento de duplicatas.

**Módulos/Funcionalidades Principais Envolvidas:**
- UI (main_window.py)
- Application (services/backup_restore_service.py)
- Infrastructure (backup.py, file_system.py)

**Pré-condições:**
- Fotix está em execução
- Pelo menos um backup foi criado (através do processamento de duplicatas)

**Dados de Teste Sugeridos:**
- Backup criado no cenário UAT_FOTIX_004

**Passos para Execução:**
1. Clicar no botão "Gerenciar Backups" na barra de ferramentas
2. Observar a lista de backups disponíveis
3. Verificar as informações exibidas para cada backup (ID, data, número de arquivos)
4. Fechar o diálogo de gerenciamento de backups

**Resultado Esperado:**
- O diálogo de gerenciamento de backups deve ser exibido
- A lista de backups deve incluir o backup criado anteriormente
- Para cada backup, devem ser exibidas informações como ID, data e número de arquivos
- Deve ser possível fechar o diálogo

**Critério de Passagem Geral:**
O teste é considerado bem-sucedido se a aplicação exibir corretamente a lista de backups disponíveis com suas informações.

### UAT_FOTIX_007

**Título do Cenário:** Restauração de Arquivos a partir de um Backup

**Objetivo do Teste:** Verificar se a aplicação permite restaurar arquivos a partir de um backup criado anteriormente.

**Módulos/Funcionalidades Principais Envolvidas:**
- UI (main_window.py)
- Application (services/backup_restore_service.py)
- Infrastructure (backup.py, file_system.py)

**Pré-condições:**
- Fotix está em execução
- Pelo menos um backup foi criado (através do processamento de duplicatas)
- Os arquivos originais foram removidos (estão na lixeira ou foram excluídos)

**Dados de Teste Sugeridos:**
- Backup criado no cenário UAT_FOTIX_004

**Passos para Execução:**
1. Clicar no botão "Restaurar Backup" na barra de ferramentas
2. Observar a mensagem informando o número de backups disponíveis
3. Verificar se é possível selecionar um backup para restauração

**Resultado Esperado:**
- Uma mensagem deve ser exibida informando o número de backups disponíveis para restauração
- (Nota: Como mencionado no código, a funcionalidade completa de restauração ainda não está implementada, então este teste verifica apenas a exibição da mensagem)

**Critério de Passagem Geral:**
O teste é considerado bem-sucedido se a aplicação exibir corretamente a mensagem sobre backups disponíveis para restauração.

### UAT_FOTIX_008

**Título do Cenário:** Cancelamento de Escaneamento em Progresso

**Objetivo do Teste:** Verificar se a aplicação permite cancelar um escaneamento em progresso e retorna ao estado anterior corretamente.

**Módulos/Funcionalidades Principais Envolvidas:**
- UI (main_window.py, widgets/progress_dialog.py)
- Application (services/scan_service.py)
- Infrastructure (concurrency.py)

**Pré-condições:**
- Fotix está em execução
- Existe um diretório grande o suficiente para que o escaneamento demore alguns segundos

**Dados de Teste Sugeridos:**
- Um diretório com muitos arquivos (ex: diretório de fotos ou documentos)

**Passos para Execução:**
1. Clicar no botão "Escanear Diretórios" na barra de ferramentas
2. No diálogo de seleção de diretório, selecionar o diretório grande
3. Observar o diálogo de progresso durante o escaneamento
4. Antes que o escaneamento seja concluído, clicar no botão "Cancelar"
5. Verificar se o escaneamento é interrompido
6. Verificar a mensagem na barra de status

**Resultado Esperado:**
- O diálogo de progresso deve ser exibido durante o escaneamento
- Ao clicar em "Cancelar", o escaneamento deve ser interrompido
- O diálogo de progresso deve ser fechado
- A barra de status deve exibir a mensagem "Varredura cancelada pelo usuário"
- A interface deve voltar ao estado anterior, sem exibir resultados parciais

**Critério de Passagem Geral:**
O teste é considerado bem-sucedido se a aplicação permitir cancelar o escaneamento em progresso e retornar ao estado anterior corretamente.

### UAT_FOTIX_009

**Título do Cenário:** Verificação da Ajuda e Informações Sobre a Aplicação

**Objetivo do Teste:** Verificar se a aplicação fornece informações de ajuda e sobre a aplicação corretamente.

**Módulos/Funcionalidades Principais Envolvidas:**
- UI (main_window.py)

**Pré-condições:**
- Fotix está em execução

**Dados de Teste Sugeridos:**
- N/A (Não são necessários dados específicos para este teste)

**Passos para Execução:**
1. Clicar no botão "Ajuda" na barra de ferramentas
2. Verificar as informações de ajuda exibidas
3. Fechar o diálogo de ajuda
4. Clicar no menu "Ajuda" na barra de menus
5. Clicar na opção "Sobre"
6. Verificar as informações sobre a aplicação exibidas
7. Fechar o diálogo "Sobre"

**Resultado Esperado:**
- O diálogo de ajuda deve exibir informações sobre como usar a aplicação, incluindo:
  - Como escanear diretórios
  - Como selecionar e processar duplicatas
  - Como gerenciar backups
- O diálogo "Sobre" deve exibir informações sobre a aplicação, incluindo:
  - Nome da aplicação
  - Versão
  - Breve descrição

**Critério de Passagem Geral:**
O teste é considerado bem-sucedido se a aplicação exibir corretamente as informações de ajuda e sobre a aplicação.

### UAT_FOTIX_010

**Título do Cenário:** Saída da Aplicação

**Objetivo do Teste:** Verificar se a aplicação permite sair corretamente, com confirmação do usuário.

**Módulos/Funcionalidades Principais Envolvidas:**
- UI (main_window.py)

**Pré-condições:**
- Fotix está em execução

**Dados de Teste Sugeridos:**
- N/A (Não são necessários dados específicos para este teste)

**Passos para Execução:**
1. Clicar no menu "Arquivo" na barra de menus
2. Clicar na opção "Sair"
3. Verificar se um diálogo de confirmação é exibido
4. Clicar em "Não" para cancelar a saída
5. Verificar se a aplicação continua em execução
6. Repetir os passos 1 e 2
7. No diálogo de confirmação, clicar em "Sim" para confirmar a saída
8. Verificar se a aplicação é encerrada

**Resultado Esperado:**
- Ao clicar em "Sair", um diálogo de confirmação deve ser exibido com a mensagem "Tem certeza que deseja sair?"
- Ao clicar em "Não", o diálogo deve ser fechado e a aplicação deve continuar em execução
- Ao clicar em "Sim", a aplicação deve ser encerrada corretamente

**Critério de Passagem Geral:**
O teste é considerado bem-sucedido se a aplicação exibir o diálogo de confirmação ao tentar sair e responder corretamente às escolhas do usuário.
