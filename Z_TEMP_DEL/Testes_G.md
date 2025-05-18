# Cenários de Teste de Aceitação do Usuário (UAT) - Fotix

## Visão Geral

Este documento contém cenários de teste de aceitação do usuário (UAT) para o aplicativo Fotix, uma ferramenta desktop para identificação e gerenciamento de arquivos de imagem duplicados. Os cenários foram desenvolvidos com base no Blueprint Arquitetural e na Ordem de Implementação do projeto.

## Cenários de Teste

### UAT_FOTIX_001: Configuração Inicial e Varredura Básica de Diretório

**Título do Cenário:** Configuração inicial e primeira varredura de diretório para identificação de duplicatas

**Objetivo do Teste:** Validar que o usuário pode iniciar o aplicativo, configurar preferências básicas e realizar uma varredura simples de um diretório para identificar arquivos duplicados.

**Módulos/Funcionalidades Principais Envolvidas:**
- fotix.ui.main_window
- fotix.application.services.scan_service
- fotix.core.duplicate_finder
- fotix.infrastructure.file_system

**Pré-condições:**
- Aplicativo Fotix instalado e funcional
- Existência de um diretório com alguns arquivos de imagem, incluindo pelo menos um par de duplicatas

**Dados de Teste Sugeridos:**
- Diretório de teste: criar uma pasta com 10-15 imagens, onde 2-3 pares são duplicatas exatas (mesmo conteúdo, mas possivelmente nomes diferentes)

**Passos para Execução:**
1. Iniciar o aplicativo Fotix
2. Na tela inicial, localizar e clicar no botão para selecionar diretório
3. No diálogo de seleção de diretório, navegar e selecionar o diretório de teste preparado
4. Verificar se as opções de varredura estão configuradas para "Apenas este diretório" (sem incluir subdiretórios ou arquivos ZIP)
5. Iniciar a varredura clicando no botão "Iniciar Varredura" ou equivalente
6. Aguardar a conclusão do processo de varredura
7. Examinar a lista de duplicatas exibida na interface

**Resultado Esperado:**
- Após o passo 1: O aplicativo deve iniciar sem erros, exibindo a interface principal
- Após o passo 3: O caminho do diretório selecionado deve aparecer na interface
- Após o passo 5: Deve ser exibido um indicador de progresso mostrando que a varredura está em andamento
- Após o passo 6: A varredura deve ser concluída em tempo razoável
- Após o passo 7: A interface deve exibir corretamente os conjuntos de arquivos duplicados encontrados, mostrando informações como nome, caminho, tamanho e possivelmente miniaturas das imagens

**Critério de Passagem Geral:** O aplicativo deve iniciar corretamente, permitir a seleção de um diretório, realizar a varredura e exibir com precisão os conjuntos de arquivos duplicados encontrados no diretório de teste.

### UAT_FOTIX_002: Varredura Avançada com Subdiretórios e Arquivos ZIP

**Título do Cenário:** Varredura de diretório com subdiretórios e arquivos ZIP

**Objetivo do Teste:** Validar que o aplicativo pode identificar duplicatas em uma estrutura de diretórios complexa, incluindo subdiretórios e arquivos dentro de ZIPs.

**Módulos/Funcionalidades Principais Envolvidas:**
- fotix.application.services.scan_service
- fotix.core.duplicate_finder
- fotix.infrastructure.file_system
- fotix.infrastructure.zip_handler
- fotix.infrastructure.concurrency

**Pré-condições:**
- Aplicativo Fotix instalado e funcional
- Existência de uma estrutura de diretórios com subdiretórios e pelo menos um arquivo ZIP contendo imagens
- Algumas imagens duplicadas distribuídas entre diretórios regulares e arquivos ZIP

**Dados de Teste Sugeridos:**
- Diretório principal com 5-10 imagens
- 2-3 subdiretórios com 3-5 imagens cada
- Um arquivo ZIP contendo 5-10 imagens
- Pelo menos 3 conjuntos de duplicatas distribuídos entre estas localizações (incluindo pelo menos uma duplicata entre um arquivo regular e um arquivo dentro do ZIP)

**Passos para Execução:**
1. Iniciar o aplicativo Fotix
2. Selecionar o diretório principal de teste
3. Ativar a opção "Incluir subdiretórios" nas configurações de varredura
4. Ativar a opção "Incluir arquivos em ZIPs" nas configurações de varredura
5. Iniciar a varredura
6. Aguardar a conclusão do processo
7. Examinar a lista de duplicatas exibida

**Resultado Esperado:**
- Após o passo 5: Deve ser exibido um indicador de progresso mostrando que a varredura está em andamento
- Após o passo 6: A varredura deve ser concluída em tempo razoável, mesmo com a complexidade adicional
- Após o passo 7: A interface deve exibir corretamente todos os conjuntos de arquivos duplicados, incluindo aqueles em subdiretórios e dentro de arquivos ZIP. A exibição deve indicar claramente quais arquivos estão em ZIPs.

**Critério de Passagem Geral:** O aplicativo deve identificar corretamente todas as duplicatas na estrutura complexa, incluindo aquelas dentro de arquivos ZIP, e exibi-las de forma organizada e compreensível.

### UAT_FOTIX_003: Seleção Automática de Arquivos a Manter por Critério de Data

**Título do Cenário:** Seleção automática de arquivos a manter usando o critério de data de modificação

**Objetivo do Teste:** Validar que o aplicativo pode aplicar corretamente a estratégia de seleção baseada em data de modificação para escolher automaticamente quais arquivos manter de cada conjunto de duplicatas.

**Módulos/Funcionalidades Principais Envolvidas:**
- fotix.ui.main_window
- fotix.application.services.duplicate_management_service
- fotix.core.selection_strategy

**Pré-condições:**
- Aplicativo Fotix instalado e funcional
- Varredura já realizada com alguns conjuntos de duplicatas identificados
- Os arquivos duplicados possuem datas de modificação diferentes

**Dados de Teste Sugeridos:**
- Pelo menos 3 conjuntos de duplicatas, cada um com 2-3 arquivos com datas de modificação diferentes

**Passos para Execução:**
1. Com a lista de duplicatas já exibida após uma varredura, localizar a opção de seleção automática
2. Selecionar o critério "Manter o arquivo mais recente" (baseado na data de modificação)
3. Aplicar a seleção automática clicando em "Aplicar Seleção" ou botão equivalente
4. Verificar quais arquivos foram selecionados para manter em cada conjunto de duplicatas
5. Verificar se é possível ajustar manualmente a seleção após a aplicação automática

**Resultado Esperado:**
- Após o passo 3: O aplicativo deve processar a seleção rapidamente
- Após o passo 4: Em cada conjunto de duplicatas, o arquivo com a data de modificação mais recente deve estar marcado para ser mantido, e os outros marcados para remoção
- Após o passo 5: Deve ser possível alterar manualmente a seleção de arquivos a manter/remover

**Critério de Passagem Geral:** O aplicativo deve aplicar corretamente a estratégia de seleção baseada em data, marcando para manutenção os arquivos mais recentes em cada conjunto de duplicatas, e permitir ajustes manuais após a seleção automática.

### UAT_FOTIX_004: Seleção Automática de Arquivos a Manter por Critério de Resolução

**Título do Cenário:** Seleção automática de arquivos a manter usando o critério de resolução de imagem

**Objetivo do Teste:** Validar que o aplicativo pode aplicar corretamente a estratégia de seleção baseada na resolução da imagem para escolher automaticamente quais arquivos manter de cada conjunto de duplicatas.

**Módulos/Funcionalidades Principais Envolvidas:**
- fotix.ui.main_window
- fotix.application.services.duplicate_management_service
- fotix.core.selection_strategy

**Pré-condições:**
- Aplicativo Fotix instalado e funcional
- Varredura já realizada com alguns conjuntos de duplicatas identificados
- Os arquivos duplicados incluem imagens com resoluções diferentes

**Dados de Teste Sugeridos:**
- Pelo menos 3 conjuntos de duplicatas, cada um com 2-3 arquivos de imagem com resoluções diferentes (ex: uma versão em alta resolução e uma versão redimensionada da mesma imagem)

**Passos para Execução:**
1. Com a lista de duplicatas já exibida após uma varredura, localizar a opção de seleção automática
2. Selecionar o critério "Manter a imagem de maior resolução"
3. Aplicar a seleção automática clicando em "Aplicar Seleção" ou botão equivalente
4. Verificar quais arquivos foram selecionados para manter em cada conjunto de duplicatas
5. Verificar se é possível ajustar manualmente a seleção após a aplicação automática

**Resultado Esperado:**
- Após o passo 3: O aplicativo deve processar a seleção rapidamente
- Após o passo 4: Em cada conjunto de duplicatas, o arquivo com a maior resolução deve estar marcado para ser mantido, e os outros marcados para remoção
- Após o passo 5: Deve ser possível alterar manualmente a seleção de arquivos a manter/remover

**Critério de Passagem Geral:** O aplicativo deve aplicar corretamente a estratégia de seleção baseada em resolução, marcando para manutenção os arquivos de maior resolução em cada conjunto de duplicatas, e permitir ajustes manuais após a seleção automática.

### UAT_FOTIX_005: Remoção de Duplicatas com Backup Automático

**Título do Cenário:** Remoção de arquivos duplicados com criação automática de backup

**Objetivo do Teste:** Validar que o aplicativo pode remover com segurança os arquivos duplicados selecionados, criando um backup antes da remoção.

**Módulos/Funcionalidades Principais Envolvidas:**
- fotix.ui.main_window
- fotix.application.services.duplicate_management_service
- fotix.infrastructure.backup
- fotix.infrastructure.file_system

**Pré-condições:**
- Aplicativo Fotix instalado e funcional
- Varredura já realizada com alguns conjuntos de duplicatas identificados
- Seleção de arquivos a manter/remover já realizada (manual ou automaticamente)

**Dados de Teste Sugeridos:**
- Pelo menos 3 conjuntos de duplicatas com seleção já aplicada (alguns arquivos marcados para manter, outros para remover)

**Passos para Execução:**
1. Com a lista de duplicatas e seleções já definidas, localizar a opção para remover os arquivos duplicados
2. Verificar se a opção "Criar backup antes de remover" está ativada
3. Iniciar o processo de remoção clicando em "Remover Duplicatas" ou botão equivalente
4. Confirmar a ação no diálogo de confirmação que deve aparecer
5. Aguardar a conclusão do processo de backup e remoção
6. Verificar o status final exibido na interface
7. Verificar fisicamente se os arquivos marcados para remoção foram movidos para a lixeira
8. Navegar até a seção de backups do aplicativo para confirmar que um novo backup foi criado

**Resultado Esperado:**
- Após o passo 4: Deve aparecer um indicador de progresso mostrando o backup e a remoção em andamento
- Após o passo 5: O processo deve ser concluído sem erros
- Após o passo 6: A interface deve indicar que a operação foi concluída com sucesso
- Após o passo 7: Os arquivos marcados para remoção não devem mais estar em seus locais originais, mas devem estar na lixeira do sistema
- Após o passo 8: Deve ser possível ver um novo backup na lista de backups, contendo os arquivos que foram removidos

**Critério de Passagem Geral:** O aplicativo deve realizar com sucesso o backup dos arquivos selecionados para remoção e depois movê-los para a lixeira, mantendo os arquivos selecionados para preservação em seus locais originais.

### UAT_FOTIX_006: Restauração de Backup

**Título do Cenário:** Restauração de arquivos a partir de um backup

**Objetivo do Teste:** Validar que o aplicativo permite visualizar backups anteriores e restaurar arquivos selecionados para seus locais originais ou para um novo local.

**Módulos/Funcionalidades Principais Envolvidas:**
- fotix.ui.main_window
- fotix.application.services.backup_restore_service
- fotix.infrastructure.backup
- fotix.infrastructure.file_system

**Pré-condições:**
- Aplicativo Fotix instalado e funcional
- Pelo menos um backup criado anteriormente durante a remoção de duplicatas

**Dados de Teste Sugeridos:**
- Um backup existente contendo pelo menos 5 arquivos de imagem

**Passos para Execução:**
1. Iniciar o aplicativo Fotix
2. Navegar para a seção de "Gerenciamento de Backups" ou equivalente
3. Verificar a lista de backups disponíveis
4. Selecionar um backup específico para visualizar seu conteúdo
5. Examinar a lista de arquivos contidos no backup
6. Selecionar alguns arquivos específicos para restauração (ou todos)
7. Escolher a opção "Restaurar para local original"
8. Confirmar a ação no diálogo de confirmação
9. Aguardar a conclusão do processo de restauração
10. Verificar se os arquivos foram restaurados corretamente em seus locais originais
11. Repetir os passos 4-9, mas desta vez escolhendo "Restaurar para novo local" e selecionando um diretório diferente

**Resultado Esperado:**
- Após o passo 3: A interface deve exibir uma lista de backups disponíveis com informações como data, número de arquivos, etc.
- Após o passo 5: A interface deve mostrar detalhes dos arquivos no backup, como nome original, caminho, tamanho, etc.
- Após o passo 9: O processo de restauração deve ser concluído sem erros
- Após o passo 10: Os arquivos selecionados devem estar presentes em seus locais originais
- Após a repetição com novo local: Os arquivos selecionados devem estar presentes no novo diretório escolhido

**Critério de Passagem Geral:** O aplicativo deve permitir a visualização de backups anteriores e a restauração seletiva de arquivos, tanto para seus locais originais quanto para um novo local especificado pelo usuário.

### UAT_FOTIX_007: Tratamento de Erros durante a Varredura

**Título do Cenário:** Tratamento de erros durante a varredura de diretórios

**Objetivo do Teste:** Validar que o aplicativo lida adequadamente com erros durante o processo de varredura, como arquivos inacessíveis ou corrompidos.

**Módulos/Funcionalidades Principais Envolvidas:**
- fotix.ui.main_window
- fotix.application.services.scan_service
- fotix.infrastructure.file_system
- fotix.infrastructure.logging_config

**Pré-condições:**
- Aplicativo Fotix instalado e funcional
- Diretório de teste contendo alguns arquivos normais e pelo menos um arquivo com problemas (ex: sem permissão de leitura, corrompido)

**Dados de Teste Sugeridos:**
- Diretório com 10 imagens normais
- Um arquivo de imagem com permissões modificadas para bloquear acesso de leitura
- Um arquivo ZIP corrompido ou protegido por senha

**Passos para Execução:**
1. Iniciar o aplicativo Fotix
2. Selecionar o diretório de teste contendo os arquivos problemáticos
3. Iniciar a varredura
4. Observar como o aplicativo lida com os arquivos problemáticos durante a varredura
5. Aguardar a conclusão do processo
6. Verificar se há mensagens de erro ou avisos na interface
7. Verificar se os arquivos acessíveis foram processados corretamente, apesar dos erros

**Resultado Esperado:**
- Durante o passo 4: O aplicativo não deve travar ou falhar completamente ao encontrar arquivos problemáticos
- Após o passo 5: A varredura deve ser concluída, mesmo que com avisos
- Após o passo 6: A interface deve exibir mensagens informativas sobre os arquivos que não puderam ser processados
- Após o passo 7: Os arquivos acessíveis devem ter sido processados normalmente, e quaisquer duplicatas entre eles devem ser identificadas

**Critério de Passagem Geral:** O aplicativo deve demonstrar resiliência ao lidar com arquivos problemáticos, continuando a varredura para os arquivos acessíveis e fornecendo feedback adequado ao usuário sobre os problemas encontrados.

### UAT_FOTIX_008: Cancelamento de Operações em Andamento

**Título do Cenário:** Cancelamento de operações de longa duração

**Objetivo do Teste:** Validar que o usuário pode cancelar operações de longa duração, como varredura ou remoção de duplicatas, e que o aplicativo responde adequadamente ao cancelamento.

**Módulos/Funcionalidades Principais Envolvidas:**
- fotix.ui.main_window
- fotix.application.services.scan_service
- fotix.application.services.duplicate_management_service
- fotix.infrastructure.concurrency

**Pré-condições:**
- Aplicativo Fotix instalado e funcional
- Diretório grande com muitos arquivos para garantir que a varredura leve tempo suficiente para ser cancelada

**Dados de Teste Sugeridos:**
- Diretório com pelo menos 1000 imagens ou um diretório com subdiretórios profundos

**Passos para Execução:**
1. Iniciar o aplicativo Fotix
2. Selecionar o diretório grande de teste
3. Iniciar a varredura
4. Aguardar alguns segundos até que a operação esteja claramente em andamento
5. Localizar e clicar no botão "Cancelar" ou equivalente
6. Observar como o aplicativo responde ao cancelamento
7. Verificar se a interface volta ao estado anterior à operação
8. Repetir os passos 2-7, mas desta vez cancelando durante uma operação de remoção de duplicatas (após identificar duplicatas e selecionar arquivos para remover)

**Resultado Esperado:**
- Após o passo 5: O aplicativo deve reconhecer imediatamente o pedido de cancelamento
- Após o passo 6: A operação deve ser interrompida de forma limpa, sem travamentos
- Após o passo 7: A interface deve voltar a um estado utilizável, possivelmente exibindo uma mensagem indicando que a operação foi cancelada
- Após a repetição com remoção: O aplicativo deve cancelar a operação de remoção sem deixar o sistema em estado inconsistente (nenhum arquivo parcialmente removido)

**Critério de Passagem Geral:** O aplicativo deve permitir o cancelamento seguro de operações de longa duração, respondendo prontamente ao comando do usuário e retornando a um estado consistente e utilizável.

### UAT_FOTIX_009: Processamento de Grande Volume de Arquivos

**Título do Cenário:** Processamento eficiente de grande volume de arquivos

**Objetivo do Teste:** Validar que o aplicativo pode lidar eficientemente com um grande volume de arquivos, utilizando paralelismo para otimizar o desempenho.

**Módulos/Funcionalidades Principais Envolvidas:**
- fotix.application.services.scan_service
- fotix.core.duplicate_finder
- fotix.infrastructure.concurrency
- fotix.infrastructure.file_system

**Pré-condições:**
- Aplicativo Fotix instalado e funcional
- Diretório muito grande com milhares de arquivos ou múltiplos diretórios com muitos arquivos

**Dados de Teste Sugeridos:**
- Estrutura de diretórios contendo pelo menos 5.000 imagens (podem ser geradas por script)
- Incluir alguns conjuntos de duplicatas espalhados pela estrutura

**Passos para Execução:**
1. Iniciar o aplicativo Fotix
2. Selecionar o diretório raiz da estrutura de teste
3. Ativar a opção "Incluir subdiretórios"
4. Iniciar a varredura
5. Observar o indicador de progresso e o uso de recursos do sistema durante a varredura
6. Aguardar a conclusão do processo
7. Verificar o tempo total necessário para a varredura
8. Examinar os resultados para confirmar que todas as duplicatas foram identificadas

**Resultado Esperado:**
- Durante o passo 5: O aplicativo deve mostrar progresso constante e utilizar múltiplos núcleos do processador (indicando paralelismo)
- Após o passo 6: A varredura deve ser concluída em tempo razoável, considerando o volume de dados
- Após o passo 7: O tempo total deve ser significativamente menor do que seria esperado para processamento sequencial
- Após o passo 8: Todas as duplicatas conhecidas na estrutura de teste devem ter sido identificadas corretamente

**Critério de Passagem Geral:** O aplicativo deve demonstrar capacidade de processar eficientemente grandes volumes de dados, utilizando paralelismo para otimizar o desempenho, sem comprometer a precisão dos resultados.

### UAT_FOTIX_010: Persistência de Configurações do Usuário

**Título do Cenário:** Persistência de configurações e preferências do usuário entre sessões

**Objetivo do Teste:** Validar que o aplicativo salva e restaura corretamente as configurações e preferências do usuário entre diferentes sessões.

**Módulos/Funcionalidades Principais Envolvidas:**
- fotix.ui.main_window
- fotix.config

**Pré-condições:**
- Aplicativo Fotix instalado e funcional
- Primeira execução ou configurações resetadas para valores padrão

**Dados de Teste Sugeridos:**
- Não aplicável

**Passos para Execução:**
1. Iniciar o aplicativo Fotix
2. Observar as configurações padrão
3. Modificar várias configurações:
   - Alterar o diretório padrão de backup
   - Modificar a estratégia de seleção padrão (ex: de "mais recente" para "maior resolução")
   - Ativar/desativar a opção "Incluir subdiretórios" por padrão
   - Ativar/desativar a opção "Incluir arquivos em ZIPs" por padrão
4. Realizar uma varredura em um diretório específico
5. Fechar completamente o aplicativo
6. Reiniciar o aplicativo Fotix
7. Verificar se todas as configurações modificadas foram mantidas
8. Verificar se o último diretório escaneado é lembrado ou sugerido

**Resultado Esperado:**
- Após o passo 6: O aplicativo deve iniciar normalmente
- Após o passo 7: Todas as configurações modificadas no passo 3 devem estar exatamente como foram definidas
- Após o passo 8: O aplicativo deve mostrar ou sugerir facilmente o último diretório escaneado

**Critério de Passagem Geral:** O aplicativo deve salvar corretamente todas as configurações e preferências do usuário e restaurá-las nas sessões subsequentes, proporcionando uma experiência consistente.

### UAT_FOTIX_011: Visualização e Comparação de Imagens Duplicadas

**Título do Cenário:** Visualização e comparação visual de imagens duplicadas

**Objetivo do Teste:** Validar que o aplicativo permite ao usuário visualizar e comparar visualmente as imagens duplicadas para tomar decisões informadas sobre quais manter.

**Módulos/Funcionalidades Principais Envolvidas:**
- fotix.ui.main_window
- fotix.ui.widgets (componentes de visualização de imagem)

**Pré-condições:**
- Aplicativo Fotix instalado e funcional
- Varredura já realizada com alguns conjuntos de duplicatas identificados

**Dados de Teste Sugeridos:**
- Pelo menos 3 conjuntos de duplicatas, incluindo imagens com pequenas diferenças visuais (ex: uma versão original e uma levemente editada)

**Passos para Execução:**
1. Com a lista de duplicatas já exibida após uma varredura, selecionar um conjunto específico de duplicatas
2. Localizar e ativar a funcionalidade de visualização/comparação de imagens
3. Examinar as imagens duplicadas lado a lado ou em visualização detalhada
4. Verificar se é possível ampliar/reduzir as imagens para examinar detalhes
5. Verificar se informações adicionais são exibidas (resolução, data, tamanho)
6. Selecionar qual imagem manter diretamente da interface de visualização
7. Repetir para outro conjunto de duplicatas

**Resultado Esperado:**
- Após o passo 2: A interface deve exibir as imagens duplicadas de forma que permita comparação visual
- Após o passo 4: Deve ser possível ampliar as imagens para examinar detalhes específicos
- Após o passo 5: Informações relevantes sobre cada imagem devem ser exibidas junto com a visualização
- Após o passo 6: A seleção feita na interface de visualização deve ser refletida na lista principal de duplicatas

**Critério de Passagem Geral:** O aplicativo deve fornecer ferramentas eficazes para visualização e comparação de imagens duplicadas, permitindo ao usuário tomar decisões informadas sobre quais arquivos manter com base na inspeção visual.

### UAT_FOTIX_012: Gerenciamento de Múltiplos Backups

**Título do Cenário:** Gerenciamento de múltiplos backups ao longo do tempo

**Objetivo do Teste:** Validar que o aplicativo permite gerenciar eficientemente múltiplos backups criados ao longo do tempo, incluindo visualização, restauração seletiva e remoção.

**Módulos/Funcionalidades Principais Envolvidas:**
- fotix.ui.main_window
- fotix.application.services.backup_restore_service
- fotix.infrastructure.backup

**Pré-condições:**
- Aplicativo Fotix instalado e funcional
- Pelo menos três backups criados em momentos diferentes

**Dados de Teste Sugeridos:**
- Três backups distintos:
  - Um backup antigo (criado há alguns dias, se possível)
  - Um backup de tamanho médio (10-20 arquivos)
  - Um backup recente com poucos arquivos (2-3)

**Passos para Execução:**
1. Iniciar o aplicativo Fotix
2. Navegar para a seção de "Gerenciamento de Backups" ou equivalente
3. Verificar a lista de backups disponíveis, confirmando que todos os backups esperados estão presentes
4. Ordenar a lista de backups por diferentes critérios (data, tamanho, número de arquivos)
5. Selecionar um backup específico e examinar seus detalhes
6. Selecionar um arquivo específico deste backup e restaurá-lo para um novo local
7. Selecionar outro backup e excluí-lo completamente
8. Confirmar a ação de exclusão no diálogo de confirmação
9. Verificar se o backup foi removido da lista
10. Verificar se os arquivos de backup foram realmente removidos do sistema de arquivos

**Resultado Esperado:**
- Após o passo 3: A interface deve mostrar todos os backups esperados com informações como data, número de arquivos, tamanho total
- Após o passo 4: A lista deve ser reordenada de acordo com o critério selecionado
- Após o passo 6: O arquivo selecionado deve ser restaurado corretamente no local especificado
- Após o passo 9: O backup excluído não deve mais aparecer na lista
- Após o passo 10: Os arquivos físicos do backup excluído não devem mais existir no sistema

**Critério de Passagem Geral:** O aplicativo deve fornecer funcionalidades completas para gerenciar múltiplos backups, permitindo visualização, ordenação, restauração seletiva e remoção, mantendo a integridade do sistema de backup.
