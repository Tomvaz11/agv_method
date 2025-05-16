# Cenários de Teste de Aceitação do Usuário (UAT) - Fotix

Este documento contém cenários de teste manuais para validação das funcionalidades principais do Fotix, uma aplicação para gerenciamento de arquivos de fotos, incluindo detecção de duplicatas, backup e restauração.

## Cenários de Teste

### ID do Cenário: UAT_FOTIX_001
**Título do Cenário:** Inicialização da Aplicação e Verificação da Interface Principal  
**Objetivo do Teste:** Validar que a aplicação inicia corretamente e apresenta todos os elementos principais da interface.  
**Módulos/Funcionalidades Principais Envolvidas:** UI (main_window), Application (inicialização de serviços)  
**Pré-condições:** Aplicação Fotix instalada no sistema.  
**Dados de Teste Sugeridos:** N/A  
**Passos para Execução:**  
1. Iniciar a aplicação Fotix.
2. Verificar a presença da janela principal.
3. Verificar a presença dos menus principais (Arquivo, Editar, Ferramentas, Ajuda).
4. Verificar a presença da área principal para exibição de arquivos.
5. Verificar a presença dos botões de ação principais (Escanear, Gerenciar Duplicatas, Backup).

**Resultado Esperado:**  
- A aplicação deve iniciar sem erros.
- A janela principal deve ser exibida com todos os elementos da interface mencionados.
- Todos os menus e botões devem estar habilitados e responsivos ao passar o mouse.

**Critério de Passagem Geral:** A aplicação inicia corretamente e apresenta todos os elementos da interface conforme especificado no design.

---

### ID do Cenário: UAT_FOTIX_002
**Título do Cenário:** Escaneamento de Diretório para Detecção de Duplicatas  
**Objetivo do Teste:** Validar que a aplicação consegue escanear um diretório e identificar arquivos de imagem duplicados.  
**Módulos/Funcionalidades Principais Envolvidas:** UI (main_window, progress_dialog), Application (scan_service), Core (duplicate_finder), Infrastructure (file_system, concurrency)  
**Pré-condições:** Aplicação Fotix iniciada.  
**Dados de Teste Sugeridos:** Diretório contendo pelo menos 5 imagens, com 2 ou 3 duplicatas (mesmas imagens com nomes diferentes ou em subdiretórios diferentes).  
**Passos para Execução:**  
1. Clicar no botão "Escanear" ou selecionar a opção no menu.
2. Na caixa de diálogo, selecionar o diretório de teste preparado.
3. Selecionar as opções de escaneamento (por exemplo, incluir subdiretórios, método de comparação).
4. Iniciar o escaneamento.
5. Observar o progresso do escaneamento na barra de progresso.
6. Aguardar a conclusão do escaneamento.

**Resultado Esperado:**  
- A caixa de diálogo de seleção de diretório deve ser exibida corretamente.
- O progresso do escaneamento deve ser exibido na barra de progresso.
- Após a conclusão, a lista de duplicatas deve ser exibida na interface.
- As duplicatas identificadas devem corresponder às imagens duplicadas no diretório de teste.

**Critério de Passagem Geral:** A aplicação identifica corretamente todas as duplicatas no diretório de teste e as exibe na interface.

---

### ID do Cenário: UAT_FOTIX_003
**Título do Cenário:** Gerenciamento de Arquivos Duplicados  
**Objetivo do Teste:** Validar que a aplicação permite selecionar e gerenciar arquivos duplicados identificados.  
**Módulos/Funcionalidades Principais Envolvidas:** UI (duplicate_list_widget, file_info_widget), Application (duplicate_management_service), Core (selection_strategy)  
**Pré-condições:** Aplicação Fotix iniciada e escaneamento de diretório concluído com duplicatas identificadas.  
**Dados de Teste Sugeridos:** Resultado do escaneamento do cenário UAT_FOTIX_002.  
**Passos para Execução:**  
1. Na lista de duplicatas, selecionar um grupo de arquivos duplicados.
2. Verificar a visualização prévia das imagens selecionadas.
3. Selecionar a estratégia de seleção automática (por exemplo, manter o mais recente, manter o de melhor qualidade).
4. Aplicar a estratégia de seleção.
5. Verificar quais arquivos foram marcados para exclusão.
6. Modificar manualmente a seleção (desmarcar um arquivo marcado e marcar outro).
7. Clicar no botão "Aplicar" ou "Executar" para processar as duplicatas.
8. Confirmar a ação na caixa de diálogo de confirmação.

**Resultado Esperado:**  
- A visualização prévia das imagens deve ser exibida corretamente.
- A estratégia de seleção automática deve marcar os arquivos conforme o critério selecionado.
- Deve ser possível modificar manualmente a seleção.
- Após confirmar, os arquivos marcados devem ser processados (movidos para lixeira ou pasta específica).
- A lista de duplicatas deve ser atualizada após o processamento.

**Critério de Passagem Geral:** A aplicação permite gerenciar corretamente os arquivos duplicados, aplicando estratégias de seleção e processando os arquivos conforme as escolhas do usuário.

---

### ID do Cenário: UAT_FOTIX_004
**Título do Cenário:** Criação de Backup de Arquivos  
**Objetivo do Teste:** Validar que a aplicação permite criar um backup dos arquivos selecionados.  
**Módulos/Funcionalidades Principais Envolvidas:** UI (main_window, progress_dialog), Application (backup_restore_service), Infrastructure (backup, zip_handler, file_system)  
**Pré-condições:** Aplicação Fotix iniciada.  
**Dados de Teste Sugeridos:** Diretório contendo pelo menos 10 imagens de diferentes tamanhos.  
**Passos para Execução:**  
1. Clicar no botão "Backup" ou selecionar a opção no menu.
2. Na caixa de diálogo, selecionar o diretório de origem (contendo as imagens).
3. Selecionar o diretório de destino para o backup.
4. Configurar opções de backup (por exemplo, compressão, exclusão de duplicatas).
5. Iniciar o processo de backup.
6. Observar o progresso do backup na barra de progresso.
7. Aguardar a conclusão do backup.

**Resultado Esperado:**  
- A caixa de diálogo de configuração de backup deve ser exibida corretamente.
- O progresso do backup deve ser exibido na barra de progresso.
- Após a conclusão, um arquivo de backup deve ser criado no diretório de destino.
- O arquivo de backup deve conter todas as imagens do diretório de origem.
- Um relatório de backup deve ser exibido ou disponibilizado.

**Critério de Passagem Geral:** A aplicação cria com sucesso um backup dos arquivos selecionados e o arquivo de backup contém todos os arquivos esperados.

---

### ID do Cenário: UAT_FOTIX_005
**Título do Cenário:** Restauração de Backup  
**Objetivo do Teste:** Validar que a aplicação permite restaurar arquivos a partir de um backup.  
**Módulos/Funcionalidades Principais Envolvidas:** UI (main_window, progress_dialog), Application (backup_restore_service), Infrastructure (backup, zip_handler, file_system)  
**Pré-condições:** Aplicação Fotix iniciada e um backup criado previamente (do cenário UAT_FOTIX_004).  
**Dados de Teste Sugeridos:** Arquivo de backup criado no cenário UAT_FOTIX_004.  
**Passos para Execução:**  
1. Clicar no botão "Restaurar" ou selecionar a opção no menu.
2. Na caixa de diálogo, selecionar o arquivo de backup.
3. Selecionar o diretório de destino para a restauração (diferente do original).
4. Configurar opções de restauração (por exemplo, sobrescrever arquivos existentes).
5. Iniciar o processo de restauração.
6. Observar o progresso da restauração na barra de progresso.
7. Aguardar a conclusão da restauração.

**Resultado Esperado:**  
- A caixa de diálogo de configuração de restauração deve ser exibida corretamente.
- O progresso da restauração deve ser exibido na barra de progresso.
- Após a conclusão, todos os arquivos do backup devem ser restaurados no diretório de destino.
- Um relatório de restauração deve ser exibido ou disponibilizado.

**Critério de Passagem Geral:** A aplicação restaura com sucesso todos os arquivos do backup para o diretório de destino.

---

### ID do Cenário: UAT_FOTIX_006
**Título do Cenário:** Configuração de Preferências da Aplicação  
**Objetivo do Teste:** Validar que a aplicação permite configurar e salvar preferências do usuário.  
**Módulos/Funcionalidades Principais Envolvidas:** UI (settings_dialog), Application (serviços), Infrastructure (file_system)  
**Pré-condições:** Aplicação Fotix iniciada.  
**Dados de Teste Sugeridos:** N/A  
**Passos para Execução:**  
1. Acessar o menu "Ferramentas" ou "Configurações".
2. Selecionar a opção "Preferências" ou "Configurações".
3. Na caixa de diálogo de configurações, modificar as seguintes preferências:
   - Diretório padrão para escaneamento
   - Método de comparação de imagens
   - Opções de backup (nível de compressão)
   - Comportamento para arquivos duplicados
4. Salvar as configurações.
5. Fechar e reabrir a aplicação.
6. Acessar novamente a caixa de diálogo de configurações.

**Resultado Esperado:**  
- A caixa de diálogo de configurações deve exibir todas as opções configuráveis.
- As alterações devem ser salvas corretamente.
- Após reabrir a aplicação, as configurações modificadas devem ser mantidas.

**Critério de Passagem Geral:** A aplicação salva e carrega corretamente as preferências do usuário entre sessões.

---

### ID do Cenário: UAT_FOTIX_007
**Título do Cenário:** Tratamento de Erros em Operações de Arquivo  
**Objetivo do Teste:** Validar que a aplicação trata adequadamente erros durante operações de arquivo.  
**Módulos/Funcionalidades Principais Envolvidas:** UI (error_dialog), Application (serviços), Infrastructure (file_system, error_handling)  
**Pré-condições:** Aplicação Fotix iniciada.  
**Dados de Teste Sugeridos:** Diretório com permissões restritas ou arquivo em uso por outro processo.  
**Passos para Execução:**  
1. Tentar escanear um diretório sem permissões de leitura.
2. Observar o comportamento da aplicação.
3. Tentar criar um backup em um diretório sem permissões de escrita.
4. Observar o comportamento da aplicação.
5. Durante um escaneamento em andamento, tentar acessar um arquivo que está sendo usado por outro processo.
6. Observar o comportamento da aplicação.

**Resultado Esperado:**  
- A aplicação deve exibir mensagens de erro claras e informativas.
- A aplicação não deve travar ou fechar inesperadamente.
- Após um erro, a aplicação deve permitir que o usuário tente novamente ou cancele a operação.
- O log de erros deve registrar os detalhes do problema.

**Critério de Passagem Geral:** A aplicação trata adequadamente situações de erro, fornecendo feedback claro ao usuário e mantendo a estabilidade.

---

### ID do Cenário: UAT_FOTIX_008
**Título do Cenário:** Visualização e Comparação de Imagens  
**Objetivo do Teste:** Validar que a aplicação permite visualizar e comparar imagens identificadas como duplicatas.  
**Módulos/Funcionalidades Principais Envolvidas:** UI (file_info_widget), Utils (image_utils)  
**Pré-condições:** Aplicação Fotix iniciada e escaneamento de diretório concluído com duplicatas identificadas.  
**Dados de Teste Sugeridos:** Resultado do escaneamento do cenário UAT_FOTIX_002.  
**Passos para Execução:**  
1. Na lista de duplicatas, selecionar um grupo de arquivos duplicados.
2. Clicar no botão "Visualizar" ou "Comparar".
3. Na interface de visualização, alternar entre as imagens duplicadas.
4. Utilizar as ferramentas de zoom para examinar detalhes das imagens.
5. Verificar as informações de metadados exibidas para cada imagem.
6. Comparar lado a lado duas imagens duplicadas.

**Resultado Esperado:**  
- A interface de visualização deve exibir corretamente as imagens.
- Deve ser possível alternar entre as imagens duplicadas.
- As ferramentas de zoom devem funcionar corretamente.
- Os metadados das imagens devem ser exibidos corretamente.
- A comparação lado a lado deve permitir identificar diferenças sutis entre as imagens.

**Critério de Passagem Geral:** A aplicação permite visualizar e comparar efetivamente imagens duplicadas, auxiliando o usuário na decisão de quais arquivos manter.

---

### ID do Cenário: UAT_FOTIX_009
**Título do Cenário:** Operação com Grandes Volumes de Arquivos  
**Objetivo do Teste:** Validar que a aplicação mantém o desempenho e a estabilidade ao lidar com grandes volumes de arquivos.  
**Módulos/Funcionalidades Principais Envolvidas:** Application (scan_service, duplicate_management_service), Infrastructure (concurrency, file_system)  
**Pré-condições:** Aplicação Fotix iniciada.  
**Dados de Teste Sugeridos:** Diretório contendo pelo menos 1000 imagens, com algumas duplicatas.  
**Passos para Execução:**  
1. Iniciar o escaneamento do diretório com grande volume de arquivos.
2. Observar o uso de recursos do sistema durante o escaneamento.
3. Verificar a responsividade da interface durante o processamento.
4. Após a conclusão, verificar a exibição dos resultados.
5. Tentar gerenciar as duplicatas identificadas.

**Resultado Esperado:**  
- A aplicação deve utilizar eficientemente os recursos do sistema.
- A interface deve permanecer responsiva durante o processamento.
- O progresso deve ser exibido corretamente.
- Os resultados devem ser exibidos de forma organizada, mesmo com grande volume de dados.
- As operações de gerenciamento de duplicatas devem funcionar corretamente com grandes conjuntos de dados.

**Critério de Passagem Geral:** A aplicação mantém o desempenho e a estabilidade ao lidar com grandes volumes de arquivos, sem travamentos ou uso excessivo de recursos.

---

### ID do Cenário: UAT_FOTIX_010
**Título do Cenário:** Cancelamento de Operações em Andamento  
**Objetivo do Teste:** Validar que a aplicação permite cancelar operações em andamento de forma segura.  
**Módulos/Funcionalidades Principais Envolvidas:** UI (progress_dialog), Application (serviços), Infrastructure (concurrency)  
**Pré-condições:** Aplicação Fotix iniciada.  
**Dados de Teste Sugeridos:** Diretório contendo pelo menos 100 imagens para garantir que o processamento leve tempo suficiente.  
**Passos para Execução:**  
1. Iniciar o escaneamento do diretório.
2. Durante o escaneamento, clicar no botão "Cancelar".
3. Verificar se a operação é interrompida.
4. Iniciar um processo de backup.
5. Durante o backup, clicar no botão "Cancelar".
6. Verificar se a operação é interrompida.

**Resultado Esperado:**  
- O botão "Cancelar" deve estar disponível durante operações de longa duração.
- Ao clicar em "Cancelar", a operação deve ser interrompida de forma segura.
- A aplicação deve exibir uma mensagem informando que a operação foi cancelada.
- O sistema deve voltar a um estado consistente após o cancelamento.
- Nenhum arquivo deve ficar em estado inconsistente após o cancelamento.

**Critério de Passagem Geral:** A aplicação permite cancelar operações em andamento de forma segura, mantendo a integridade do sistema e dos arquivos.
