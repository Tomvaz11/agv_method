# AGV Prompt: ImplementadorMestre v7.6 (Bimodal) - Implementação e Setup

**Tarefa Principal:** Implementar o componente de software alvo, aderindo estritamente ao `Blueprint Arquitetural` e às diretrizes abaixo.

**Contexto Essencial:**

1. **Componente Alvo Principal:** Alvo 0
2. **Blueprint Arquitetural:** @Output_BluePrint_Arquitetural_Tocrisna_v1.0.md
3. **Ordem de Implementação:** @Output_Ordem_Para_Implementacao_Geral_v1.0.md
4. **Contexto Adicional do Workspace:** (Anexar todos os arquivos .py relevantes de dependências já implementadas, tanto interfaces quanto implementações).

---

## **Diretrizes Essenciais:**

**Analise o "Componente Alvo Principal". Aja de acordo com uma das duas modalidades abaixo:**

### **MODALIDADE A: Se o Alvo for "Alvo 0: Setup do Projeto Profissional"**

Sua única responsabilidade é criar o andaime ("scaffolding") completo do projeto.

**Diretriz Específica para Testes no Alvo 0:**

- A criação da **estrutura de diretórios** para testes (ex: tests/, tests/unit/) **FAZ PARTE** do scaffolding do Alvo 0.
- A criação de **arquivos de teste com código** (ex: test_models.py, etc.) é **ESTRITAMENTE PROIBIDA** nesta fase.

**Restrição de Conteúdo:** Ao criar os arquivos, você está **PROIBIDO** de implementar qualquer código que represente a lógica de negócio ou do domínio do aplicativo. O objetivo é criar a estrutura de arquivos e pastas, não a implementação.

- **O que EXCLUIR:** Qualquer linha de código de implementação dentro de arquivos como `models.py` (não crie classes Pydantic/Django), `services.py` (não crie funções de caso de uso), `views.py` (não crie endpoints), `components.tsx` (não crie a lógica do componente React), etc. Para cumprir o propósito de scaffolding, cada um desses arquivos de código DEVE ser criado contendo **apenas** um docstring de módulo que explique seu propósito na arquitetura (ex: """Este módulo conterá os modelos de domínio (SSOT)..."""). Nenhum outro código (classes, funções, imports) deve ser adicionado nesta fase.

---

#### **MODALIDADE B: Se o Alvo for Qualquer Outro Módulo Funcional**

Sua responsabilidade é implementar a funcionalidade do módulo. Siga estas diretrizes:

1. **Fonte da Verdade:** O `@Blueprint_Arquitetural.md` é a autoridade máxima para responsabilidades, dependências, tecnologias e esrutura de diretórios. Siga-o rigorosamente.
2. **Foco Estrito no Escopo:** Sua tarefa é implementar **APENAS** o "Componente Alvo Principal" e os módulos base (interfaces, modelos) estritamente necessários para suportá-lo.
3. **Qualidade do Código:** Escreva código limpo, profissional e de fácil manutenção, aderindo aos princípios SOLID e ao estilo PEP 8.
4. **Gerenciamento de Módulos Base:** Ao criar/modificar módulos base (ex: `models.py`), siga os padrões e tecnologias especificados no Blueprint. Adicione Docstrings (PEP 257) a todo o código de produção.

5. **Testes Unitários (MANDATÓRIO):**

   - Gere testes unitários (`pytest`) para **TODO** o código de produção novo ou modificado.
   - Atingir **100% de cobertura da lógica de implementação concreta** é a meta.
   - Para **arquivos de interface (ABCs)**, crie testes de contrato básicos.
   - **Estrutura de Testes Mandatória:** Os testes para `src/fotix/[caminho]/modulo.py` **DEVEM** residir em `tests/unit/fotix/[caminho]/test_modulo.py`.

6. **Documentação e Clareza (Docstrings - MANDATÓRIO):**

   - **Docstring de Módulo:** Todo arquivo de produção `.py` criado ou modificado DEVE começar com um docstring de módulo (usando `"""..."""`) que explique sucintamente o propósito do módulo e seu papel na arquitetura.
   - **Docstrings de Funções/Classes/Métodos:** Todas as classes e funções/métodos públicos devem ter docstrings claras explicando o que fazem, seus parâmetros e o que retornam (estilo PEP 257).

7. **Conformidade com a Stack Tecnológica (Protocolo de Bloqueio):**

   - Utilize **EXCLUSIVAMENTE** as bibliotecas e tecnologias designadas no Blueprint. É **PROIBIDO** usar alternativas.
   - Se encontrar um problema que não possa ser resolvido, **PARE a implementação e comunique o bloqueio técnico**, solicitando novas instruções.

8. **Diretriz de Foco no Contrato (Interface-First para Dependências) - [CRUCIAL]**

   - **Análise de Dependências:** Ao analisar o Blueprint, identifique as dependências diretas do "Componente Alvo Principal".
   - **Priorize Interfaces:** Para cada dependência que possuir uma **interface** definida no workspace (ex: `IFileSystemService` para `FileSystemService`), você **DEVE** priorizar o uso do arquivo da **interface** (ex: `src/fotix/infrastructure/interfaces/file_system.py`) como sua fonte de conhecimento primária sobre como interagir com essa dependência. O arquivo de interface é mais leve e contém o "contrato" que você precisa cumprir.
   - **Uso Condicional da Implementação:** Você só deve consultar o arquivo da **implementação** concreta (ex: `.../implementations/file_system_service.py`) se a informação na interface for insuficiente para a sua tarefa (o que deve ser raro).
   - **Racionalização para Mocks:** Ao criar testes unitários, esta abordagem "Interface-First" é o seu guia. Seus mocks (`unittest.mock.patch` ou `pytest` fixtures) devem mirar e replicar a **interface**, não os detalhes internos da implementação concreta. Isso resulta em testes mais robustos e desacoplados.

9. **Gerenciamento do Ambiente (Lifecycle-Aware):** Se a implementação do seu alvo exigir uma **nova biblioteca/dependência externa** que não está listada no `pyproject.toml`, você **DEVE**:
   - Adicionar a nova dependência na seção apropriada do `pyproject.toml` (`[project.dependencies]` para produção ou `[project.optional-dependencies.dev]` para desenvolvimento).
   - Se a nova biblioteca gerar arquivos que devam ser ignorados, adicione as entradas correspondentes ao arquivo `.gitignore`.
   - Mencione explicitamente essas atualizações no seu relatório final.

---

### **Resultado Esperado (Formato do Relatório Final)**

O formato do seu resumo final dependerá da modalidade executada:

#### **Se executou a MODALIDADE A (Setup do Projeto):**

```markdown
### Resumo da Implementação - Alvo 0: Setup do Projeto Profissional

- **Arquivos e Estrutura Criados:**

- **Instruções de Setup para o Coordenador:**

  1.  Execute `pip install -e .[dev]` para instalar o projeto em modo editável e as dependências de desenvolvimento.
  2.  Execute `pre-commit install` para ativar os ganchos de pré-commit no repositório.

- **Desvios, Adições ou Suposições Críticas:**
  [Liste aqui apenas se houver algo crucial a relatar. Caso contrário, escreva: 'Nenhum.']
```

---

#### **Se executou a MODALIDADE B (Implementação de Módulo):**

```markdown
### Resumo da Implementação

- **Arquivos Criados/Modificados:**

  - `[caminho/completo/para/arquivo1.py]`
  - `[caminho/completo/para/test_arquivo1.py]`

- **Confirmação de Testes:**
  Testes unitários foram criados para todo o código de produção, seguindo a estrutura espelhada e visando 100% de cobertura da lógica de implementação concreta.

- **Confirmação de Documentação:**
  Todo o código de produção foi documentado com docstrings de módulo e de função/classe, conforme as diretrizes.

- **Desvios, Adições ou Suposições Críticas:**
  [Liste aqui apenas se houver algo crucial a relatar. Caso contrário, escreva: 'Nenhum.']
```
