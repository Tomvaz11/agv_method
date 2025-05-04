# AGV Prompt Template: PreenchedorGenerico v1.2 - Preenchimento Cirúrgico de Prompt AGV

**Tarefa Principal:**  
Preencher **exclusivamente** os campos marcados como placeholders (ex: `[PLACEHOLDER]`) no arquivo de template `[NOME_DO_ARQUIVO_TEMPLATE_ALVO.md]`, utilizando **somente** informações textualmente presentes nos documentos listados como fontes (`[LISTAR_ARQUIVOS_FONTE.md]`), de forma **literal, sem alterações, deduções ou criações**.

---

## REGRAS ABSOLUTAS (NÃO IGNORAR):

1. **NÃO** altere, resuma, reordene ou delete qualquer conteúdo do template original.
2. **NÃO** invente, reescreva, reformule ou "melhore" textos com base em interpretação ou conhecimento prévio.
3. **NÃO** preencha campos com “chute” ou suposições.
4. **NÃO** insira dados que não existam explicitamente nos documentos fonte.
5. **NÃO** preencha campos reservados a humanos, conforme indicação no próprio template.

---

## INSTRUÇÕES DETALHADAS:

1. **Leitura Atenta das Fontes:**  
   Leia com atenção **cada documento fonte** listado, buscando **somente dados factuais e literais** para preencher os campos do template.

2. **Identificação de Placeholders:**  
   Identifique todos os campos entre colchetes (`[EXEMPLO]`) no template alvo. Estes são os únicos locais permitidos para inserção de conteúdo.

3. **Preenchimento com Dados Literais:**
   - Substitua os placeholders **exatamente** pelos textos presentes nas fontes.
   - Caso a informação **não exista nas fontes**, insira exatamente:  
     ```[INFORMAÇÃO NÃO ENCONTRADA NAS FONTES]```
   - Se o conteúdo da fonte for grande, mas corresponder integralmente ao campo, **cole-o completo**, sem cortes.

4. **Preservação da Estrutura Markdown:**
   - Mantenha todos os `# Títulos`, `- Listas`, `1. Enumerações`, `> Blocos de citação` e `**negritos**` **exatamente como no template original**.
   - Não remova, altere ou adicione nenhum item fora dos locais explicitamente marcados para preenchimento.

---

## ARQUIVOS DE REFERÊNCIA:

### 1. Template Alvo (a ser preenchido):
```markdown
# --- Conteúdo de [NOME_DO_ARQUIVO_TEMPLATE_ALVO.md] ---
[COLE AQUI O CONTEÚDO DO TEMPLATE VAZIO, ex: Prompt_Severino_v1.1.md]
```

### 2. Documentos Fonte:
```markdown
# --- Conteúdo de [ARQUIVO_FONTE_1.md] ---
[COLE AQUI O CONTEÚDO DO PRIMEIRO DOCUMENTO FONTE]

# --- Conteúdo de [ARQUIVO_FONTE_2.md] ---
[COLE AQUI O CONTEÚDO DO SEGUNDO DOCUMENTO FONTE, SE HOUVER]

# --- [Adicionar mais fontes conforme necessário] ---
```

---

## RESULTADO FINAL ESPERADO:

1. **Prompt Final Preenchido:**  
   Arquivo `[NOME_DO_ARQUIVO_TEMPLATE_ALVO.md]` totalmente preenchido com dados extraídos fielmente dos arquivos fonte, pronto para uso, em Markdown puro.

2. **Relatório de Preenchimento:**  
   Adicione no final do arquivo, dentro de um bloco Markdown, um relatório com:
   - Quais seções foram preenchidas.
   - Quais documentos fonte foram usados para cada uma.
   - Quais campos **não puderam ser preenchidos**.
   - Exemplo:

     ```
     **Relatório de Preenchimento:**
     - Seção 'Interfaces': preenchida com base no `Blueprint_Tocrisna.md`.
     - Campo `[NOME_DO_PROJETO]`: encontrado em `Stack_Overview.md`.
     - Campo `[RESPONSAVEL_TECNICO]`: [INFORMAÇÃO NÃO ENCONTRADA NAS FONTES]
     ```
     
---

## VALIDAÇÃO FINAL OBRIGATÓRIA:

Antes de concluir:
- Faça uma comparação linha a linha com o template original.
- Certifique-se de que **nada além dos placeholders foi alterado.**
- Nenhum título, texto informativo, bloco de instruções ou formatação pode ter sido tocado.

---

### >>> RETORNE AO USUÁRIO UM ÚNICO ARQUIVO `.md` PRONTO PARA DOWNLOAD <<<