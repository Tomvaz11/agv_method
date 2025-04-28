## 1. 🔹 Propósito Principal

Este prompt modelo foi projetado para guiar uma LLM (você no caso) na tarefa de **definir e documentar uma proposta de arquitetura técnica de alto nível** para um novo projeto de software. 

O foco é estabelecer uma estrutura sólida, modular, manutenível e alinhada com boas práticas desde o início, com ênfase na definição clara dos **componentes principais** e, crucialmente, das **interfaces de comunicação (contratos)** entre eles.

---

## 2. 🔹 Agente AGV Associado

- **Tocrisna** (Arquiteta) - Nome ficticio dado a você, que fará o papel de arquiteta do projeto.

---

## 3. 🔹 Fase do Fluxo AGV

- Este é o prompt central da **Fase 2 (Arquitetura Técnica)** do fluxo AGV.
- Utilizado logo após a Fase 1 (Definição e Preparação), onde a visão do produto e a stack tecnológica são definidas.

---

## 4. 🔹 Inputs Chave Necessários (Placeholders já Preenchidos)

O usuário deve preencher a seção **"Contexto e Definições Iniciais do Projeto"** no arquivo `Prompt_Tocrisna_Architecture_v1.0.md` com as informações da Fase 1, conforme orientação abaixo:

### 🔹 Nome Oficial do Projeto

- `Fotix`

### 🔹 Visão do Produto

```markdown
- Aplicativo desktop desenvolvido em Python, com backend robusto e interface gráfica (GUI) completa, projetado para localizar e remover arquivos duplicados (idênticos) de imagens e vídeos em múltiplos diretórios e arquivos ZIP.
- O sistema analisa arquivos de mídia e, **somente ao identificar dois ou mais arquivos idênticos**, utiliza um algoritmo inteligente para decidir qual arquivo manter e qual remover, com base em critérios como maior resolução da imagem, data de criação mais antiga e estrutura do nome do arquivo (evitando cópias como "(1)", "cópia", etc.).
- A arquitetura é otimizada para grandes volumes de dados, utilizando processamento assíncrono, batching progressivo e execução paralela.
- O aplicativo também oferece sistema de backup e restauração para recuperação segura dos arquivos removidos.
```
	
### 🔹 Funcionalidades Chave em Alto Nível

```markdown
- Análise de arquivos de mídia (imagens e vídeos) em diretórios e arquivos ZIP.
- Identificação precisa de arquivos duplicados (idênticos) utilizando hashing.
- Seleção automática do arquivo a ser mantido entre duplicatas com base em critérios objetivos.
- Remoção segura de duplicatas com backup automático.
- Recuperação fácil de arquivos removidos através do sistema de restauração.
- Processamento otimizado para grandes volumes de dados com execução assíncrona, paralela e em lotes.
- Interface gráfica intuitiva para configuração e acompanhamento.
- Geração de logs detalhados e relatórios resumidos com estatísticas pós-processamento.
```

### 🔹 Público-Alvo e Ambiente

- `Usuários finais em desktop (Windows)`

### 🔹 Stack de Tecnologias

```markdown
- **GUI (Interface Gráfica):** PySide6 (Qt for Python) — framework moderno para criação de interfaces desktop nativas.
- **Motor de Escaneamento de Duplicatas:** BLAKE3 + pré-filtragem por tamanho com `os.path.getsize` para otimização inicial.
- **Manipulação de Arquivos e Sistema de Arquivos:** pathlib + shutil + send2trash (remoção segura) + concurrent.futures (execução paralela).
- **Descompactação Otimizada:** stream-unzip para leitura e extração progressiva de arquivos ZIP.
```

### 🔹 Requisitos Não Funcionais Iniciais

```markdown
- Capacidade de processar grandes volumes (100.000+ arquivos) sem travamentos.
- Identificação rápida de duplicatas com uso eficiente de CPU, RAM e disco.
- Backups automáticos para garantir segurança de dados.
- GUI responsiva mesmo sob alta carga de processamento.
- Compatibilidade garantida com Windows 10 ou superior.
- Descompactação eficiente de grandes arquivos ZIP com baixo uso de memória.
- Tratamento de erros em operações críticas de escrita e remoção.
```

### 🔹 Principais Restrições

```markdown
- Suporte exclusivo para Windows na primeira versão.
- Sem integração com bancos de dados externos.
- Análise limitada a arquivos idênticos (sem similaridade perceptual).
- Suporte apenas ao formato ZIP para arquivos compactados.
- Sem sistema de atualização automática previsto na primeira versão.
- Desempenho condicionado à capacidade de hardware local do usuário.
```

---

## 5. 🔹 Outputs Esperados da LLM (você)

A execução bem-sucedida deste prompt deve gerar um **Blueprint Arquitetural Detalhado**, preferencialmente em Markdown, contendo no mínimo:

1. **Visão Geral da Arquitetura:** Abordagem escolhida (ex: Camadas, Microserviços) e justificativa.
2. **Diagrama de Componentes (Simplificado):** Representação visual ou textual dos módulos principais e suas conexões.
3. **Descrição dos Componentes/Módulos:** Nome, responsabilidade e tecnologias chave para cada componente.
4. **Definição das Interfaces Principais:** Detalhamento crucial dos contratos entre componentes (assinaturas, estruturas de dados, propósito).
5. **Gerenciamento de Dados:** Como os dados serão tratados.
6. **Estrutura de Diretórios Proposta:** Sugestão inicial de organização de pastas.
7. **Considerações de Segurança:** Princípios aplicados no design.
8. **Justificativas e Trade-offs:** Explicação das decisões chave.

---

## 6. 🔹 Diretrizes e Princípios AGV Enfatizados

Este prompt instrui a LLM a priorizar:

- **Modularidade e SRP:** Divisão clara de responsabilidades.
- **Baixo Acoplamento e Alta Coesão:** Módulos independentes, mas internamente focados.
- **Interfaces Explícitas:** Definição clara dos contratos como diretriz crítica para Integração Incremental (ver `docs/principios_chave_agv.md`).
- **Clareza, Manutenibilidade e Testabilidade:** A arquitetura deve ser compreensível e facilitar o desenvolvimento e testes futuros.
- **Segurança Fundamental:** Considerações de segurança básicas incorporadas ao design.
- **Aderência à Stack e Padrões:** Uso da stack definida e aplicação de padrões de design com justificativa.






## 7. Notas de Uso e Otimização

*   Este é um dos prompts mais críticos do fluxo AGV. A qualidade do Blueprint Arquitetural gerado impactará todas as fases subsequentes.
*   **Validação Humana é Essencial:** Revise *cuidadosamente* a arquitetura proposta pela IA. Ela faz sentido para o seu projeto? As interfaces estão claras e completas? Os trade-offs são aceitáveis? Não hesite em iterar, ajustando o prompt ou pedindo clarificações/alternativas à IA até que a arquitetura seja aprovada.
*   Quanto mais claros e detalhados forem os inputs da Fase 1 (visão, funcionalidades, requisitos não funcionais), melhor será a arquitetura gerada.