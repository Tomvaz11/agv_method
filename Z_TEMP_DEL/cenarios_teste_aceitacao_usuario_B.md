# Cenários de Teste de Aceitação do Usuário (UAT) para Fotix

## Visão Geral

Este documento contém cenários de teste manuais para validar as funcionalidades principais do Fotix, uma aplicação desktop para identificação e gerenciamento de arquivos de imagem duplicados. Os testes cobrem os fluxos de trabalho essenciais de ponta a ponta (End-to-End) da perspectiva do usuário final.

## Cenários de Teste

### UAT_FOTIX_001

**Título do Cenário:** Configuração Inicial e Verificação da Interface do Usuário

**Objetivo do Teste:** Validar que a aplicação inicia corretamente e apresenta todos os elementos de interface necessários para operação.

**Módulos/Funcionalidades Principais Envolvidas:** 
- `fotix.ui.main_window`
- `fotix.config`

**Pré-condições:**
- Fotix está instalado no sistema
- Primeira execução da aplicação ou configurações resetadas

**Dados de Teste Sugeridos:**
- N/A

**Passos para Execução:**
1. Iniciar a aplicação Fotix
2. Observar a janela principal da aplicação
3. Verificar a presença dos elementos de interface: campo para seleção de diretórios, botão para iniciar varredura, área para exibição de resultados
4. Verificar a presença de menus e opções de configuração

**Resultado Esperado:**
- A aplicação inicia sem erros
- A interface principal é exibida com todos os elementos necessários
- Os menus e opções de configuração estão acessíveis

**Critério de Passagem Geral:**
A aplicação inicia corretamente e apresenta uma interface completa e funcional com todos os elementos necessários para operação.

### UAT_FOTIX_002

**Título do Cenário:** Varredura de Diretório para Identificação de Duplicatas

**Objetivo do Teste:** Validar que a aplicação consegue escanear um diretório e identificar corretamente arquivos de imagem duplicados.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.scan_service`
- `fotix.core.duplicate_finder`
- `fotix.infrastructure.file_system`

**Pré-condições:**
- Fotix está em execução
- Existe um diretório de teste com algumas imagens duplicadas

**Dados de Teste Sugeridos:**
- Diretório contendo pelo menos 3 imagens, onde 2 são duplicatas exatas (mesmo conteúdo, mesmo hash)

**Passos para Execução:**
1. Na interface principal, selecionar a opção para escolher diretório
2. Navegar e selecionar o diretório de teste preparado
3. Iniciar a varredura clicando no botão correspondente
4. Aguardar a conclusão do processo de varredura
5. Observar os resultados exibidos na interface

**Resultado Esperado:**
- A aplicação exibe indicador de progresso durante a varredura
- Após a conclusão, as duplicatas são exibidas agrupadas
- As informações de cada arquivo (nome, caminho, tamanho) são exibidas corretamente
- Os arquivos duplicados são corretamente identificados e agrupados

**Critério de Passagem Geral:**
A aplicação identifica corretamente todos os arquivos duplicados no diretório de teste e os apresenta de forma organizada na interface.

### UAT_FOTIX_003

**Título do Cenário:** Varredura de Arquivos ZIP para Identificação de Duplicatas

**Objetivo do Teste:** Validar que a aplicação consegue escanear arquivos ZIP e identificar imagens duplicadas entre arquivos normais e dentro de ZIPs.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.scan_service`
- `fotix.core.duplicate_finder`
- `fotix.infrastructure.file_system`
- `fotix.infrastructure.zip_handler`

**Pré-condições:**
- Fotix está em execução
- Existe um diretório de teste com algumas imagens e um arquivo ZIP contendo imagens, onde pelo menos uma imagem dentro do ZIP é duplicata de uma imagem no diretório

**Dados de Teste Sugeridos:**
- Diretório contendo 2-3 imagens normais
- Arquivo ZIP contendo 2-3 imagens, onde pelo menos uma é duplicata de uma imagem no diretório

**Passos para Execução:**
1. Na interface principal, selecionar a opção para escolher diretório
2. Navegar e selecionar o diretório de teste preparado
3. Certificar-se que a opção "Incluir arquivos ZIP" está ativada
4. Iniciar a varredura clicando no botão correspondente
5. Aguardar a conclusão do processo de varredura
6. Observar os resultados exibidos na interface

**Resultado Esperado:**
- A aplicação processa tanto os arquivos normais quanto o conteúdo do ZIP
- As duplicatas entre arquivos normais e arquivos dentro do ZIP são identificadas corretamente
- A interface exibe claramente quais arquivos estão dentro de ZIPs

**Critério de Passagem Geral:**
A aplicação identifica corretamente duplicatas entre arquivos normais e arquivos dentro de ZIPs, exibindo-os de forma organizada e clara na interface.

### UAT_FOTIX_004

**Título do Cenário:** Seleção Automática e Remoção de Duplicatas

**Objetivo do Teste:** Validar que a aplicação consegue selecionar automaticamente quais arquivos manter e remover duplicatas conforme a estratégia escolhida.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.duplicate_management_service`
- `fotix.core.selection_strategy`
- `fotix.infrastructure.file_system`
- `fotix.infrastructure.backup`

**Pré-condições:**
- Fotix está em execução
- Uma varredura foi realizada e duplicatas foram identificadas
- Os resultados estão sendo exibidos na interface

**Dados de Teste Sugeridos:**
- Conjunto de duplicatas identificado no cenário UAT_FOTIX_002

**Passos para Execução:**
1. Nos resultados da varredura, selecionar um conjunto de duplicatas
2. Selecionar a estratégia de seleção automática (ex: "Manter o arquivo mais recente")
3. Aplicar a estratégia de seleção
4. Verificar quais arquivos foram marcados para remoção
5. Confirmar a remoção dos arquivos marcados
6. Verificar se a opção de backup está ativada
7. Confirmar a operação final

**Resultado Esperado:**
- A estratégia de seleção marca corretamente os arquivos conforme o critério escolhido
- A interface exibe claramente quais arquivos serão mantidos e quais serão removidos
- Após confirmação, os arquivos marcados são movidos para a lixeira
- Se a opção de backup estiver ativada, os arquivos são copiados para o diretório de backup antes da remoção
- A interface é atualizada para refletir as alterações

**Critério de Passagem Geral:**
A aplicação seleciona corretamente os arquivos conforme a estratégia escolhida, realiza backup se solicitado, e remove os arquivos duplicados, mantendo a interface atualizada durante todo o processo.

### UAT_FOTIX_005

**Título do Cenário:** Seleção Manual e Remoção de Duplicatas

**Objetivo do Teste:** Validar que a aplicação permite ao usuário selecionar manualmente quais arquivos manter e quais remover.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.duplicate_management_service`
- `fotix.infrastructure.file_system`
- `fotix.infrastructure.backup`

**Pré-condições:**
- Fotix está em execução
- Uma varredura foi realizada e duplicatas foram identificadas
- Os resultados estão sendo exibidos na interface

**Dados de Teste Sugeridos:**
- Conjunto de duplicatas identificado no cenário UAT_FOTIX_002 ou UAT_FOTIX_003

**Passos para Execução:**
1. Nos resultados da varredura, selecionar um conjunto de duplicatas
2. Selecionar manualmente qual arquivo deseja manter (clicando ou marcando o arquivo)
3. Verificar se os demais arquivos do conjunto são marcados automaticamente para remoção
4. Confirmar a remoção dos arquivos marcados
5. Verificar se a opção de backup está ativada
6. Confirmar a operação final

**Resultado Esperado:**
- A interface permite selecionar claramente qual arquivo manter
- Os demais arquivos do conjunto são marcados automaticamente para remoção
- Após confirmação, os arquivos marcados são movidos para a lixeira
- Se a opção de backup estiver ativada, os arquivos são copiados para o diretório de backup antes da remoção
- A interface é atualizada para refletir as alterações

**Critério de Passagem Geral:**
A aplicação permite ao usuário selecionar manualmente qual arquivo manter, realiza backup se solicitado, e remove os arquivos duplicados, mantendo a interface atualizada durante todo o processo.

### UAT_FOTIX_006

**Título do Cenário:** Visualização e Restauração de Backups

**Objetivo do Teste:** Validar que a aplicação permite visualizar e restaurar arquivos de backups anteriores.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.backup_restore_service`
- `fotix.infrastructure.backup`
- `fotix.infrastructure.file_system`

**Pré-condições:**
- Fotix está em execução
- Pelo menos uma operação de remoção com backup foi realizada anteriormente

**Dados de Teste Sugeridos:**
- Backup criado durante o cenário UAT_FOTIX_004 ou UAT_FOTIX_005

**Passos para Execução:**
1. Na interface principal, acessar a seção ou menu de backups
2. Verificar a lista de backups disponíveis
3. Selecionar um backup específico para visualizar seu conteúdo
4. Verificar as informações exibidas sobre os arquivos no backup
5. Selecionar um ou mais arquivos para restauração
6. Escolher o destino da restauração (local original ou novo local)
7. Confirmar a operação de restauração
8. Verificar se os arquivos foram restaurados corretamente

**Resultado Esperado:**
- A interface exibe a lista de backups disponíveis com informações como data e número de arquivos
- Ao selecionar um backup, seu conteúdo é exibido detalhadamente
- É possível selecionar arquivos específicos para restauração
- A operação de restauração é realizada corretamente para o destino escolhido
- A interface fornece feedback sobre o sucesso da operação

**Critério de Passagem Geral:**
A aplicação permite visualizar backups anteriores, selecionar arquivos específicos e restaurá-los corretamente para o destino escolhido, fornecendo feedback adequado durante todo o processo.

### UAT_FOTIX_007

**Título do Cenário:** Processamento de Grande Volume de Arquivos

**Objetivo do Teste:** Validar que a aplicação consegue processar eficientemente um grande volume de arquivos e manter a responsividade da interface.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.scan_service`
- `fotix.core.duplicate_finder`
- `fotix.infrastructure.concurrency`
- `fotix.infrastructure.file_system`

**Pré-condições:**
- Fotix está em execução
- Existe um diretório com grande volume de arquivos (100+ imagens)

**Dados de Teste Sugeridos:**
- Diretório contendo pelo menos 100 imagens, com algumas duplicatas

**Passos para Execução:**
1. Na interface principal, selecionar a opção para escolher diretório
2. Navegar e selecionar o diretório com grande volume de arquivos
3. Iniciar a varredura clicando no botão correspondente
4. Observar o indicador de progresso durante a varredura
5. Tentar interagir com a interface durante o processamento
6. Aguardar a conclusão do processo de varredura
7. Verificar os resultados exibidos

**Resultado Esperado:**
- A aplicação exibe um indicador de progresso claro durante a varredura
- A interface permanece responsiva durante o processamento
- O processamento é concluído em tempo razoável, utilizando paralelismo
- Os resultados são exibidos corretamente após a conclusão
- Não ocorrem travamentos ou erros durante o processamento

**Critério de Passagem Geral:**
A aplicação processa eficientemente um grande volume de arquivos, mantendo a interface responsiva e exibindo corretamente os resultados após a conclusão.

### UAT_FOTIX_008

**Título do Cenário:** Tratamento de Erros de Acesso a Arquivos

**Objetivo do Teste:** Validar que a aplicação lida adequadamente com erros de acesso a arquivos e fornece feedback apropriado ao usuário.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.scan_service`
- `fotix.infrastructure.file_system`
- `fotix.infrastructure.logging_config`

**Pré-condições:**
- Fotix está em execução
- Existe um diretório com pelo menos um arquivo sem permissão de leitura

**Dados de Teste Sugeridos:**
- Diretório contendo alguns arquivos normais e pelo menos um arquivo sem permissão de leitura

**Passos para Execução:**
1. Na interface principal, selecionar a opção para escolher diretório
2. Navegar e selecionar o diretório preparado com o arquivo sem permissão
3. Iniciar a varredura clicando no botão correspondente
4. Observar como a aplicação lida com o erro de acesso
5. Verificar se a varredura continua para os demais arquivos
6. Verificar se há algum log ou mensagem de erro na interface

**Resultado Esperado:**
- A aplicação identifica o erro de acesso ao arquivo
- Uma mensagem de erro apropriada é exibida na interface
- O erro é registrado nos logs da aplicação
- A varredura continua para os demais arquivos acessíveis
- O resultado final inclui apenas os arquivos que puderam ser processados

**Critério de Passagem Geral:**
A aplicação lida adequadamente com erros de acesso a arquivos, fornecendo feedback apropriado ao usuário e continuando o processamento para os arquivos acessíveis.

### UAT_FOTIX_009

**Título do Cenário:** Configuração e Personalização da Aplicação

**Objetivo do Teste:** Validar que a aplicação permite configurar e personalizar seu comportamento conforme as preferências do usuário.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.config`

**Pré-condições:**
- Fotix está em execução

**Dados de Teste Sugeridos:**
- Diferentes configurações para testar (ex: caminho de backup personalizado, nível de log, etc.)

**Passos para Execução:**
1. Na interface principal, acessar a seção ou menu de configurações
2. Verificar as opções de configuração disponíveis
3. Modificar algumas configurações (ex: caminho de backup, nível de log)
4. Salvar as configurações
5. Reiniciar a aplicação (se necessário)
6. Verificar se as configurações foram mantidas
7. Realizar uma operação que utilize as configurações modificadas (ex: backup)

**Resultado Esperado:**
- A interface exibe todas as opções de configuração disponíveis
- As configurações podem ser modificadas e salvas
- As configurações são mantidas após reiniciar a aplicação
- As operações utilizam corretamente as configurações modificadas

**Critério de Passagem Geral:**
A aplicação permite configurar e personalizar seu comportamento, mantém as configurações entre sessões e utiliza corretamente as configurações definidas pelo usuário.

### UAT_FOTIX_010

**Título do Cenário:** Fluxo Completo de Trabalho End-to-End

**Objetivo do Teste:** Validar o fluxo completo de trabalho da aplicação, desde a varredura até a remoção de duplicatas e restauração de backup.

**Módulos/Funcionalidades Principais Envolvidas:**
- Todos os módulos principais da aplicação

**Pré-condições:**
- Fotix está em execução
- Existe um diretório de teste com algumas imagens duplicadas

**Dados de Teste Sugeridos:**
- Diretório contendo pelo menos 5 imagens, onde algumas são duplicatas

**Passos para Execução:**
1. Na interface principal, selecionar a opção para escolher diretório
2. Navegar e selecionar o diretório de teste
3. Iniciar a varredura clicando no botão correspondente
4. Aguardar a conclusão do processo de varredura
5. Nos resultados, selecionar um conjunto de duplicatas
6. Aplicar uma estratégia de seleção automática
7. Confirmar a remoção com backup ativado
8. Verificar se os arquivos foram removidos corretamente
9. Acessar a seção de backups
10. Selecionar o backup recém-criado
11. Restaurar um arquivo do backup para um novo local
12. Verificar se o arquivo foi restaurado corretamente

**Resultado Esperado:**
- Cada etapa do fluxo é executada corretamente
- A interface fornece feedback adequado durante todo o processo
- Os arquivos duplicados são identificados, removidos e backups são criados
- Os arquivos podem ser restaurados a partir do backup
- Não ocorrem erros ou comportamentos inesperados durante todo o fluxo

**Critério de Passagem Geral:**
A aplicação executa corretamente o fluxo completo de trabalho, desde a varredura até a remoção de duplicatas e restauração de backup, mantendo a integridade dos dados e fornecendo feedback adequado ao usuário durante todo o processo.
