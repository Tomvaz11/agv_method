# AGV Prompt: ImplementadorMestre v4.0 (Lean) - Implementação Focada

**Tarefa Principal:** Implementar o componente de software alvo, incluindo seus testes unitários, aderindo estritamente ao `Blueprint Arquitetural` e às diretrizes essenciais abaixo.

**Contexto Essencial (Fornecido pelo Coordenador):**

1.  **Componente Alvo Principal:** `fotix.application.services.scan_service`
2.  **Blueprint Arquitetural:** `@Output_BluePrint_Arquitetural_Tocrisna_v5.0.md`
3.  **Ordem de Implementação:** `@Output_Ordem_Para_Implementacao_Geral_v3.2.md`
4.  **Contexto Adicional do Workspace:** (Anexar arquivos .py relevantes de dependências já implementadas)

**Diretrizes Essenciais:**


1.  **Fonte da Verdade:** O `@Blueprint_Arquitetural.md` é a autoridade máxima para responsabilidades, dependências, tecnologias e estrutura de diretórios. Siga-o rigorosamente.
2.  **Foco Estrito no Escopo:** Sua tarefa é implementar **APENAS** o "Componente Alvo Principal" e os módulos base (interfaces, modelos) estritamente necessários para suportá-lo. Não crie código para outros componentes da Ordem de Implementação.
3.  **Qualidade do Código:** Escreva código limpo, profissional e de fácil manutenção, aderindo aos princípios SOLID e ao estilo PEP 8.
4.  **Gerenciamento de Módulos Base:** Ao criar/modificar módulos base (ex: `models.py`, `interfaces.py`), siga os padrões e tecnologias especificados no Blueprint.
    *   **Modelos:** Use a tecnologia especificada (ex: Pydantic).
    *   **Interfaces:** Use `abc.ABC` ou `typing.Protocol`.
    *   **Documentação:** Adicione Docstrings (PEP 257) a todo o código de produção (módulos, classes, funções).
5.  **Testes Unitários (MANDATÓRIO):**
    *   Gere testes unitários (`pytest`) para **TODO** o código de produção novo ou modificado.
    *   Atingir **100% de cobertura da lógica de implementação concreta** é a meta.
    *   Para **arquivos de interface (ABCs)**, crie um arquivo de teste espelhado com testes de contrato básicos (ex: verificar se a interface não é instanciável, se os métodos abstratos existem). A cobertura < 100% para esses arquivos de teste de interface é aceitável.
    *   **Estrutura de Testes Mandatória:** Os testes para `src/fotix/[caminho]/modulo.py` **DEVEM** residir em `tests/unit/fotix/[caminho]/test_modulo.py`. Crie todos os diretórios e arquivos `__init__.py` necessários para manter a estrutura espelhada.
6.  **Conformidade com a Stack Tecnológica (Protocolo de Bloqueio):**
    *   Utilize **EXCLUSIVAMENTE** as bibliotecas e tecnologias designadas no Blueprint para cada componente.
    *   É **PROIBIDO** usar bibliotecas alternativas como fallback.
    *   Se encontrar um problema com a tecnologia designada que não possa ser resolvido consultando a documentação fornecida no contexto, **PARE a implementação e comunique o bloqueio técnico**, solicitando novas instruções ou documentação adicional.

**Resultado Esperado:**

1.  **Arquivos de Código:** O(s) arquivo(s) `.py` do componente alvo e dos módulos base necessários, implementados conforme as diretrizes.
2.  **Arquivos de Teste:** O(s) arquivo(s) `test_*.py` correspondentes.
3.  **Resumo da Implementação (Conforme formato abaixo):**

```markdown
### Resumo da Implementação

*   **Arquivos Criados/Modificados:**
    *   `[caminho/completo/para/arquivo1.py]`
    *   `[caminho/completo/para/arquivo2.py]`
    *   `[caminho/completo/para/test_arquivo1.py]`
    *   `[caminho/completo/para/test_arquivo2.py]`

*   **Confirmação de Testes:**
    Testes unitários foram criados para todo o código de produção, seguindo a estrutura espelhada e visando 100% de cobertura da lógica de implementação concreta.

*   **Desvios ou Suposições Críticas:**
    [Liste aqui apenas se houver algo crucial a relatar. Caso contrário, escreva: 'Nenhum.']
```