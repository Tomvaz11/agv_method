# Cenários de Teste de Aceitação do Usuário (UAT) - Fotix

## Visão Geral

Este documento contém cenários de teste manuais para validar as funcionalidades principais do Fotix, uma aplicação desktop para identificação e gerenciamento de arquivos de imagem duplicados. Os testes cobrem os fluxos de trabalho essenciais de ponta a ponta (End-to-End) da perspectiva do usuário final.

## Cenários de Teste

### UAT_FOTIX_001

**Título do Cenário:** Configuração Inicial e Verificação da Interface

**Objetivo do Teste:** Validar que a aplicação inicia corretamente e apresenta todos os elementos de interface necessários para operação.

**Módulos/Funcionalidades Principais Envolvidas:** 
- `fotix.ui.main_window`
- `fotix.config`

**Pré-condições:**
- Aplicação Fotix instalada no sistema
- Primeira execução ou configurações resetadas

**Dados de Teste Sugeridos:**
- N/A

**Passos para Execução:**
1. Iniciar a aplicação Fotix
2. Observar a janela principal da aplicação
3. Verificar a presença de todos os elementos de interface principais (área de seleção de diretórios, botões de ação, área de exibição de resultados)
4. Verificar se o menu principal contém as opções esperadas (Arquivo, Configurações, Ajuda, etc.)
5. Acessar a seção de configurações (se disponível)
6. Verificar se as configurações padrão estão presentes e com valores razoáveis

**Resultado Esperado:**
- A aplicação deve iniciar sem erros
- Todos os elementos de interface devem estar presentes e visualmente corretos
- As configurações padrão devem estar definidas com valores razoáveis
- A interface deve ser responsiva e sem elementos visuais quebrados

**Critério de Passagem Geral:** A aplicação inicia corretamente, apresentando uma interface completa e funcional com todas as opções necessárias para operação.

### UAT_FOTIX_002

**Título do Cenário:** Escaneamento Básico de Diretório para Duplicatas

**Objetivo do Teste:** Verificar se a aplicação consegue escanear um diretório e identificar corretamente arquivos de imagem duplicados.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.scan_service`
- `fotix.core.duplicate_finder`
- `fotix.infrastructure.file_system`

**Pré-condições:**
- Aplicação Fotix iniciada
- Diretório de teste com algumas imagens duplicadas preparado

**Dados de Teste Sugeridos:**
- Criar um diretório de teste contendo:
  - 2-3 pares de imagens idênticas com nomes diferentes
  - Algumas imagens únicas
  - Subdiretórios com mais algumas imagens (incluindo duplicatas)

**Passos para Execução:**
1. Na interface principal, localizar e clicar no botão/opção para selecionar diretório
2. Navegar até o diretório de teste preparado e selecioná-lo
3. Iniciar o processo de escaneamento (clicar em "Escanear" ou botão equivalente)
4. Observar o indicador de progresso durante o escaneamento
5. Aguardar a conclusão do escaneamento
6. Verificar os resultados exibidos na interface

**Resultado Esperado:**
- Para o passo 2: O diretório selecionado deve ser exibido na interface
- Para o passo 3-4: Um indicador de progresso deve ser exibido durante o escaneamento
- Para o passo 5-6: Após a conclusão, a interface deve exibir os conjuntos de arquivos duplicados encontrados
- Cada conjunto de duplicatas deve mostrar claramente quais arquivos são considerados duplicados
- As duplicatas identificadas devem corresponder às duplicatas reais no diretório de teste

**Critério de Passagem Geral:** A aplicação consegue escanear o diretório de teste e identificar corretamente todos os conjuntos de imagens duplicadas, exibindo-os de forma clara na interface.

### UAT_FOTIX_003

**Título do Cenário:** Escaneamento de Arquivos ZIP com Identificação de Duplicatas

**Objetivo do Teste:** Verificar se a aplicação consegue escanear arquivos ZIP e identificar imagens duplicadas entre arquivos normais e dentro de ZIPs.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.scan_service`
- `fotix.core.duplicate_finder`
- `fotix.infrastructure.file_system`
- `fotix.infrastructure.zip_handler`

**Pré-condições:**
- Aplicação Fotix iniciada
- Diretório de teste contendo:
  - Algumas imagens soltas
  - Um ou mais arquivos ZIP contendo imagens (algumas duplicadas das imagens soltas)

**Dados de Teste Sugeridos:**
- Criar um diretório de teste com:
  - 2-3 imagens soltas
  - Um arquivo ZIP contendo cópias das mesmas imagens (com nomes iguais ou diferentes)
  - Um segundo arquivo ZIP com pelo menos uma imagem duplicada

**Passos para Execução:**
1. Na interface principal, localizar e clicar no botão/opção para selecionar diretório
2. Navegar até o diretório de teste preparado e selecioná-lo
3. Marcar a opção "Incluir arquivos ZIP" (ou equivalente)
4. Iniciar o processo de escaneamento
5. Observar o indicador de progresso durante o escaneamento
6. Aguardar a conclusão do escaneamento
7. Verificar os resultados exibidos na interface

**Resultado Esperado:**
- Para o passo 3: A opção para incluir ZIPs deve estar disponível e funcional
- Para o passo 4-5: O indicador de progresso deve mostrar o processamento dos arquivos ZIP
- Para o passo 6-7: A interface deve exibir os conjuntos de duplicatas encontrados, incluindo arquivos dentro de ZIPs
- Os arquivos dentro de ZIPs devem ser claramente identificados como tal na interface
- As duplicatas entre arquivos normais e arquivos dentro de ZIPs devem ser corretamente identificadas

**Critério de Passagem Geral:** A aplicação consegue escanear o diretório e os arquivos ZIP, identificando corretamente as duplicatas entre arquivos normais e arquivos dentro de ZIPs.

### UAT_FOTIX_004

**Título do Cenário:** Seleção e Remoção de Duplicatas com Backup Automático

**Objetivo do Teste:** Verificar se a aplicação permite selecionar quais duplicatas manter/remover e se realiza o backup dos arquivos removidos.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.duplicate_management_service`
- `fotix.core.selection_strategy`
- `fotix.infrastructure.file_system`
- `fotix.infrastructure.backup`

**Pré-condições:**
- Aplicação Fotix iniciada
- Escaneamento de diretório já realizado com duplicatas identificadas e exibidas na interface

**Dados de Teste Sugeridos:**
- Utilizar os resultados do escaneamento do cenário UAT_FOTIX_002 ou UAT_FOTIX_003

**Passos para Execução:**
1. Na lista de duplicatas exibida, selecionar um conjunto específico
2. Verificar se a aplicação indica qual arquivo será mantido por padrão (baseado na estratégia de seleção)
3. Alterar a seleção para manter um arquivo diferente do sugerido automaticamente (se aplicável)
4. Confirmar a remoção das duplicatas (clicar em "Remover Duplicatas" ou botão equivalente)
5. Confirmar a ação na caixa de diálogo de confirmação (se apresentada)
6. Observar o progresso da operação (se indicado)
7. Verificar se a interface atualiza para refletir a remoção das duplicatas
8. Navegar até a seção de backups da aplicação
9. Verificar se um novo backup foi criado contendo os arquivos removidos

**Resultado Esperado:**
- Para o passo 2: A aplicação deve indicar claramente qual arquivo será mantido por padrão
- Para o passo 3: Deve ser possível alterar a seleção do arquivo a ser mantido
- Para o passo 4-5: Uma confirmação deve ser solicitada antes da remoção
- Para o passo 6-7: A interface deve mostrar o progresso e atualizar após a conclusão
- Para o passo 8-9: Um backup deve ter sido criado e listado na seção de backups
- Os arquivos duplicados selecionados para remoção não devem mais estar presentes no diretório original
- O arquivo selecionado para ser mantido deve permanecer no local original

**Critério de Passagem Geral:** A aplicação permite selecionar quais duplicatas manter/remover, realiza a remoção corretamente e cria um backup dos arquivos removidos que pode ser acessado posteriormente.

### UAT_FOTIX_005

**Título do Cenário:** Restauração de Arquivos a partir de Backup

**Objetivo do Teste:** Verificar se a aplicação permite restaurar arquivos previamente removidos a partir de um backup.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.backup_restore_service`
- `fotix.infrastructure.backup`
- `fotix.infrastructure.file_system`

**Pré-condições:**
- Aplicação Fotix iniciada
- Pelo menos um backup criado previamente (idealmente do cenário UAT_FOTIX_004)

**Dados de Teste Sugeridos:**
- Utilizar o backup criado no cenário UAT_FOTIX_004

**Passos para Execução:**
1. Navegar até a seção de backups da aplicação
2. Verificar a lista de backups disponíveis
3. Selecionar o backup criado anteriormente
4. Visualizar os detalhes/conteúdo do backup (se a interface permitir)
5. Iniciar o processo de restauração (clicar em "Restaurar" ou botão equivalente)
6. Escolher entre restaurar para o local original ou para um novo local (se a opção for oferecida)
7. Se solicitado, selecionar um diretório de destino para restauração
8. Confirmar a ação de restauração
9. Observar o progresso da restauração (se indicado)
10. Verificar se os arquivos foram restaurados no local esperado

**Resultado Esperado:**
- Para o passo 2: A lista de backups deve mostrar o backup criado anteriormente
- Para o passo 3-4: Deve ser possível selecionar e visualizar detalhes do backup
- Para o passo 5-6: Opções de restauração devem ser apresentadas
- Para o passo 7-9: O processo de restauração deve ser iniciado e mostrar progresso
- Para o passo 10: Os arquivos devem ser restaurados corretamente no local escolhido
- Os arquivos restaurados devem ser idênticos aos originais que foram removidos

**Critério de Passagem Geral:** A aplicação permite visualizar backups disponíveis, selecionar um backup específico e restaurar os arquivos contidos nele para o local original ou um novo local.

### UAT_FOTIX_006

**Título do Cenário:** Aplicação de Diferentes Estratégias de Seleção

**Objetivo do Teste:** Verificar se a aplicação permite configurar e aplicar diferentes estratégias para selecionar automaticamente qual arquivo manter entre duplicatas.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.duplicate_management_service`
- `fotix.core.selection_strategy`
- `fotix.config`

**Pré-condições:**
- Aplicação Fotix iniciada
- Diretório de teste com duplicatas que possuem características diferentes (datas, resoluções, nomes)

**Dados de Teste Sugeridos:**
- Criar um diretório com pares de imagens duplicadas onde:
  - Um par tem datas de criação/modificação diferentes
  - Um par tem resoluções diferentes (se aplicável para o tipo de arquivo)
  - Um par tem nomes de arquivo significativamente diferentes

**Passos para Execução:**
1. Acessar as configurações da aplicação
2. Localizar as opções de estratégia de seleção
3. Alterar a estratégia para "Manter o mais recente" (ou equivalente)
4. Salvar as configurações
5. Realizar um escaneamento do diretório de teste
6. Verificar qual arquivo é selecionado por padrão para ser mantido no par com datas diferentes
7. Voltar às configurações e alterar a estratégia para "Manter maior resolução" (ou equivalente)
8. Realizar novo escaneamento e verificar a seleção padrão
9. Repetir com a estratégia "Manter por nome" (ou equivalente)

**Resultado Esperado:**
- Para o passo 2-3: As opções de estratégia de seleção devem estar disponíveis e ser alteráveis
- Para o passo 5-6: Com a estratégia "Manter o mais recente", o arquivo com data mais recente deve ser selecionado
- Para o passo 7-8: Com a estratégia "Manter maior resolução", o arquivo com maior resolução deve ser selecionado
- Para o passo 9: Com a estratégia "Manter por nome", a seleção deve seguir a lógica de nomes definida

**Critério de Passagem Geral:** A aplicação permite configurar diferentes estratégias de seleção e aplica corretamente cada estratégia ao selecionar automaticamente qual arquivo manter entre duplicatas.

### UAT_FOTIX_007

**Título do Cenário:** Gerenciamento de Múltiplos Conjuntos de Duplicatas em Lote

**Objetivo do Teste:** Verificar se a aplicação permite selecionar e gerenciar múltiplos conjuntos de duplicatas simultaneamente.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.duplicate_management_service`
- `fotix.infrastructure.backup`
- `fotix.infrastructure.file_system`

**Pré-condições:**
- Aplicação Fotix iniciada
- Escaneamento realizado com múltiplos conjuntos de duplicatas identificados

**Dados de Teste Sugeridos:**
- Diretório com pelo menos 3-4 conjuntos diferentes de arquivos duplicados

**Passos para Execução:**
1. Realizar um escaneamento do diretório de teste
2. Verificar que múltiplos conjuntos de duplicatas são exibidos
3. Selecionar vários conjuntos de duplicatas (usando Ctrl+clique, caixas de seleção ou método equivalente)
4. Verificar se a interface indica corretamente quais arquivos serão mantidos em cada conjunto
5. Iniciar a remoção em lote (clicar em "Remover Selecionados" ou botão equivalente)
6. Confirmar a ação na caixa de diálogo (se apresentada)
7. Observar o progresso da operação em lote
8. Verificar se a interface atualiza para refletir a remoção dos múltiplos conjuntos
9. Verificar se um backup foi criado contendo todos os arquivos removidos

**Resultado Esperado:**
- Para o passo 3: Deve ser possível selecionar múltiplos conjuntos de duplicatas
- Para o passo 4: A interface deve mostrar claramente quais arquivos serão mantidos/removidos
- Para o passo 5-7: A operação em lote deve ser iniciada e mostrar progresso
- Para o passo 8: A interface deve atualizar removendo os conjuntos processados
- Para o passo 9: Um único backup deve conter todos os arquivos removidos na operação em lote

**Critério de Passagem Geral:** A aplicação permite selecionar e processar múltiplos conjuntos de duplicatas em uma única operação, criando um backup consolidado dos arquivos removidos.

### UAT_FOTIX_008

**Título do Cenário:** Cancelamento de Operações de Longa Duração

**Objetivo do Teste:** Verificar se a aplicação permite cancelar operações de longa duração como escaneamento ou processamento de duplicatas.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.scan_service`
- `fotix.infrastructure.concurrency`

**Pré-condições:**
- Aplicação Fotix iniciada
- Diretório grande com muitos arquivos ou arquivos ZIP grandes disponível para teste

**Dados de Teste Sugeridos:**
- Diretório com muitas imagens (>100) ou arquivos ZIP grandes contendo muitas imagens

**Passos para Execução:**
1. Selecionar o diretório grande para escaneamento
2. Iniciar o processo de escaneamento
3. Enquanto o escaneamento está em progresso, localizar e clicar no botão "Cancelar" (ou equivalente)
4. Observar o comportamento da aplicação após o cancelamento
5. Iniciar um novo escaneamento do mesmo diretório
6. Aguardar até que alguns resultados comecem a aparecer
7. Cancelar novamente a operação
8. Verificar se os resultados parciais são mantidos ou descartados

**Resultado Esperado:**
- Para o passo 3: Um botão de cancelamento deve estar disponível durante operações longas
- Para o passo 4: A aplicação deve interromper o escaneamento de forma limpa, sem travamentos
- Para o passo 7-8: O cancelamento deve funcionar consistentemente, com comportamento claro sobre resultados parciais

**Critério de Passagem Geral:** A aplicação permite cancelar operações de longa duração de forma segura e consistente, retornando a um estado utilizável após o cancelamento.

### UAT_FOTIX_009

**Título do Cenário:** Tratamento de Erros e Recuperação

**Objetivo do Teste:** Verificar se a aplicação lida adequadamente com situações de erro e permite recuperação.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.application.services.scan_service`
- `fotix.infrastructure.file_system`
- `fotix.infrastructure.logging_config`

**Pré-condições:**
- Aplicação Fotix iniciada
- Diretório de teste com situações problemáticas preparado

**Dados de Teste Sugeridos:**
- Diretório contendo:
  - Um arquivo corrompido ou inacessível
  - Um subdiretório sem permissão de leitura
  - Um arquivo ZIP inválido ou corrompido

**Passos para Execução:**
1. Selecionar o diretório problemático para escaneamento
2. Iniciar o processo de escaneamento
3. Observar como a aplicação lida com os arquivos problemáticos
4. Verificar se mensagens de erro apropriadas são exibidas
5. Verificar se o escaneamento continua com os arquivos válidos
6. Após a conclusão, verificar se um relatório de erros está disponível
7. Se disponível, acessar os logs da aplicação e verificar se os erros foram registrados

**Resultado Esperado:**
- Para o passo 3-4: A aplicação deve exibir mensagens de erro claras para os problemas encontrados
- Para o passo 5: O escaneamento deve continuar com os arquivos válidos, sem travar
- Para o passo 6-7: Erros devem ser registrados em logs e possivelmente disponibilizados ao usuário

**Critério de Passagem Geral:** A aplicação lida graciosamente com situações de erro, exibindo mensagens apropriadas, continuando a operação quando possível e registrando os problemas para referência.

### UAT_FOTIX_010

**Título do Cenário:** Persistência de Configurações do Usuário

**Objetivo do Teste:** Verificar se as configurações do usuário são salvas e restauradas corretamente entre sessões.

**Módulos/Funcionalidades Principais Envolvidas:**
- `fotix.ui.main_window`
- `fotix.config`
- `fotix.infrastructure.file_system`

**Pré-condições:**
- Aplicação Fotix instalada
- Primeira execução ou configurações resetadas

**Dados de Teste Sugeridos:**
- N/A

**Passos para Execução:**
1. Iniciar a aplicação Fotix
2. Acessar as configurações da aplicação
3. Alterar várias configurações (estratégia de seleção, diretório de backup, etc.)
4. Salvar as configurações
5. Fechar a aplicação completamente
6. Reiniciar a aplicação
7. Acessar novamente as configurações
8. Verificar se todas as alterações foram mantidas

**Resultado Esperado:**
- Para o passo 3-4: Deve ser possível alterar e salvar diversas configurações
- Para o passo 7-8: Após reiniciar, todas as configurações alteradas devem ser mantidas

**Critério de Passagem Geral:** A aplicação salva corretamente as configurações do usuário e as restaura nas sessões subsequentes.
