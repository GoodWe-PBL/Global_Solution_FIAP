# Plano de execução — Citizen Assist AI

Planejamento da Pessoa 3, preparado em 19/11/2026 a partir do enunciado fornecido, da divisão do grupo e do repositório existente.

## Objetivo e responsabilidades

Construir um assistente de orientação cidadã em Python, com interface gráfica como entrada principal e modo terminal alternativo, que consulte uma base local verificada, apresente referências, permita navegar entre assuntos e reconheça seus limites. O projeto deve demonstrar leitura de arquivos, listas, dicionários, busca, regras de resposta e avaliação objetiva.

- Pessoa 1: conteúdo, fontes, documentação da base e roteiro do vídeo.
- Pessoa 2: perguntas de avaliação, comparação dos modelos, métricas e interpretação, usabilidade, README e registro do uso de IA.
- Pessoa 3 (nossa parte): sistema, avaliador automático, organização e integração do repositório, verificação técnica, gravação/edição/publicação do vídeo e preparação do TXT final.

Entrega institucional: arquivo TXT com apenas dois links, um para o repositório público e outro para o vídeo no YouTube como Não Listado. Datas oficiais da FIAP ON prevalecem.

## Estado verificado

- Repositório clonado em `C:\Development\FIAP\Global Solution`.
- Origem: https://github.com/GoodWe-PBL/Global_Solution_FIAP
- Referência inicial: branch `main`, commit `5f4f98e`.
- Arquivos recebidos originalmente na raiz: `base.json`, `base_conhecimento.md`, `roteiro_video.md` e `validar_base.py`; já organizados em `data/`, `docs/` e `scripts/` nesta branch.
- Executado `python validar_base.py base.json`: aprovado, com 15 registros, 5 por tema e 36 relações.
- A base contém metadados, um dicionário `temas` e uma lista `registros`. Esse será o formato usado pelo programa.
- Cada registro inclui os campos do combinado, além de `fonte` e `observacao`. Existem registros com 3 relacionados; preservar todas as relações válidas.
- O commit recebido não continha sistema, avaliador, perguntas de teste ou README. Nesta branch estão o sistema, a interface guiada, o avaliador, o piloto de 17 casos e o README inicial. O conjunto independente e o teste de usabilidade da Pessoa 2 seguem pendentes.
- Git e Python 3.13.12 estão disponíveis nesta máquina. A versão mínima suportada será documentada após implementação e teste.
- A validação executada é estrutural: não verifica o conteúdo remoto das fontes. A data de verificação registrada pela Pessoa 1 será preservada; alterações de conteúdo devem ser justificadas por fontes.

## Estrutura prevista

```text
Global Solution/
├── README.md                         # Pessoa 2; integração técnica pela Pessoa 3
├── PLANO_EXECUCAO.md
├── .gitignore
├── data/
│   └── base.json                     # Conteúdo recebido da Pessoa 1
├── docs/
│   ├── base_conhecimento.md          # Pessoa 1
│   ├── roteiro_video.md              # Pessoa 1; ajustes conforme sistema e testes
│   ├── prompts.md                    # Pessoa 2, apoiada pela implementação
│   ├── testes.md                     # Pessoa 2
│   └── uso_ia.md                     # Pessoa 2, com registro da nossa contribuição
├── scripts/
│   └── validar_base.py               # Validador recebido, integrado e reforçado
├── src/
│   ├── sistema.py                    # Busca, validação, respostas e modo terminal
│   └── interface.py                  # Interface gráfica Tkinter
├── tests/
│   ├── perguntas_teste.json          # Pessoa 2
│   ├── avaliar.py                    # Nosso avaliador
│   ├── test_sistema.py               # Verificações técnicas dos comportamentos críticos
│   └── resultados.csv               # Gerado por avaliação real
└── entrega.txt                       # Criado ao final, apenas com os dois links reais
```

Modelo oficial consultado: https://github.com/equipe1ccon/FIAP-PORTFOLIO-1CCON/tree/master

O README de GLOBAL-SOLUTION-2 do modelo permite usar apenas as pastas pertinentes e acrescentar outras. Adaptar sua apresentação ao projeto, incluindo equipe, RMs, execução e resultados exigidos pelo enunciado; revisar também os campos administrativos do modelo, como a decisão de participação na competição, com a equipe.

## Sequência de execução

### 1. Organizar e preservar a contribuição existente

- Trabalhar em branch de implementação no repositório clonado.
- Reposicionar os quatro arquivos nos diretórios previstos, preservando IDs, conteúdo, metadados e relações da base.
- Ajustar caminhos de execução e importação. O programa deve localizar a base a partir da localização do projeto.
- Conferir com a equipe o acesso dos integrantes ao repositório já público; não há necessidade de criar outro.

Pronto quando: validador funciona na estrutura definitiva e nenhuma informação da base se perde.

### 2. Implementar carregamento e validação

- Reaproveitar a lógica do validador recebido e completar a validação de tipos e estruturas antes de usar `.get`, listas ou conjuntos.
- Tratar arquivo ausente, vazio, ilegível, codificação inválida, JSON malformado, estrutura incorreta, campos inválidos, IDs duplicados, temas/subtemas desconhecidos e referências inexistentes entre registros.
- Apresentar mensagens compreensíveis e impedir a consulta quando a base estiver inválida.
- Manter uma regra compartilhada de validação para evitar divergência entre script e sistema.

Pronto quando: a base válida carrega e os principais erros são tratados sem encerrar com traceback para o usuário.

### 3. Implementar busca e índices

- Criar listas e dicionários para recuperação por ID, tema, subtema e palavra-chave.
- Normalizar maiúsculas, acentos, espaços e pontuação tanto na consulta quanto nas palavras-chave.
- Comparar palavras e expressões completas; evitar correspondências acidentais dentro de outras palavras.
- Pontuar termos em comum, documentando como expressões específicas influenciam a ordenação.
- Separar resultado encontrado, ambíguo, sem resposta e entrada vazia. Nos casos ambíguos, exibir candidatos e pedir escolha; não escolher silenciosamente pelo primeiro ID.
- Para ausência de informação suficiente, apresentar limitação e temas disponíveis. Uma palavra conhecida não comprova que a base responde a qualquer pergunta sobre aquele assunto.
- Deixar a consulta disponível por função, independente de `input()` e `print()`, para o avaliador usar o mesmo mecanismo do terminal.

Pronto quando: perguntas diretas, reformuladas, ambíguas e fora do escopo produzem comportamentos coerentes.

### 4. Concluir interação e modelos de resposta

- Interface gráfica em Tkinter com paleta inspirada no magenta, preto e branco da FIAP; escolhas sucessivas de tema, subtema e orientação, busca por pergunta e abertura da referência no navegador.
- Manter o modo terminal para uso alternativo e demonstração dos fundamentos de lógica.
- Tratamento de entrada vazia, opção inválida e encerramento pelo usuário.
- Navegação pelo campo `relacionados`, inclusive entre temas, demonstrando uma sequência de pelo menos três assuntos.
- Modelo A: apresentação concisa da orientação.
- Modelo B: apresentação organizada em blocos de orientação, observações e confirmação.
- Ambos preservam a informação da base, o nome e link da fonte, a data de verificação e os avisos aplicáveis. O modelo B não pode inventar passos ausentes na orientação.
- Exibir o aviso geral de conteúdo informativo e não oficial. Não solicitar dados pessoais nem registrar consultas em uso normal.

Pronto quando: o fluxo completo funciona pelo comando `python src/sistema.py`, abrindo a interface gráfica, com os dois modelos selecionáveis. `python src/sistema.py --terminal` abre o modo textual.

### 5. Entregar o avaliador à Pessoa 2

- Definir cedo o contrato de `tests/perguntas_teste.json`, para a Pessoa 2 preparar as perguntas enquanto o sistema é implementado.
- Proposta por caso: identificador do teste, categoria, pergunta, `status_esperado`, `id_esperado` e, para ambiguidades, `ids_esperados`.
- Uma resposta normal usa ID real. Entrada vazia e ausência de resposta usam ID nulo e status próprio. Ambiguidade usa a lista de candidatos esperados, sem inventar um registro de resposta.
- Executar a mesma coleção nos dois modelos, medindo consulta e formatação com `time.perf_counter`, sem incluir digitação ou carregamento inicial da base.
- Exportar tabela com modelo, teste, esperado, obtido, acerto/erro, resposta exibida e tempo em milissegundos; calcular taxa de acerto e tempo médio por modelo.
- Validar o arquivo de testes e sinalizar casos malformados, em vez de descartá-los silenciosamente.
- Planejar 12 perguntas mais 3 situações-limite separadas, totalizando pelo menos 15 casos, para cumprir também a divisão interna do grupo.
- Como os modelos compartilham a busca, a precisão de seleção tende a ser igual. A comparação de clareza e facilidade de uso cabe à análise da Pessoa 2; não transformar essa avaliação humana em uma métrica inventada.

Pronto quando: `python tests/avaliar.py` gera resultados reproduzíveis usando o sistema real, e a Pessoa 2 consegue atualizar as perguntas sem editar o código.

### 6. Integrar e verificar

- Testar os erros de base, normalização, resultado único, ambiguidade, ausência de resposta e navegação relacionados.
- Executar a interface gráfica de ponta a ponta, inclusive entrada vazia, filtros, seleção de resultados e alternância de modelo; testar também o modo terminal e opções inválidas.
- Conferir todas as cenas do roteiro, incluindo a reformulação sobre demissão e a consulta ampla `documento`; ajustar a cena ou a estratégia geral com justificativa se a ambiguidade prevista não ocorrer.
- Corrigir o roteiro para que o modelo A também mencione data e avisos obrigatórios.
- Integrar os resultados, os documentos e o teste de usabilidade real da Pessoa 2; não preencher resultados por suposição.
- Fornecer à Pessoa 2 os detalhes da busca, os comandos e o uso de IA no desenvolvimento para completar README, prompts e uso_ia.
- Verificar execução em uma cópia limpa do repositório, arquivos versionados necessários e links internos.

Pronto quando: funcionalidades demonstradas, avaliação e documentação descrevem o mesmo comportamento.

### 7. Preparar vídeo e entrega

- Preencher o roteiro com os resultados reais e ensaiar a demonstração.
- Gravar a interface gráfica, explicação das escolhas, dois modelos, casos-limite e métricas; editar e publicar no YouTube como Não Listado.
- Incluir o link no README e verificar acesso público ao repositório e acesso ao vídeo pelo link.
- Gerar `entrega.txt` com exatamente duas linhas: URL do repositório e URL do vídeo.
- Enviar o TXT na FIAP ON dentro do prazo oficial.

Pronto quando: os dois links funcionam e o envio institucional está concluído.

## Dependências e pontos a conferir antes da entrega

- O texto fornecido não contém o conteúdo visual das Tabelas 1 e 2; conferir a Tabela 2 na FIAP ON antes do fechamento.
- O prazo exato não consta no texto. O roteiro propõe 6–7 minutos, mas essa duração não é um limite oficial confirmado.
- Confirmar dados da equipe, RMs e acessos necessários para publicação e entrega.
- Receber da Pessoa 2 os testes e documentos finais, incluindo evidências reais de usabilidade com alguém de fora, conforme a divisão do grupo.
- A escolha é Python com biblioteca padrão, interface gráfica Tkinter e respostas montadas a partir da base. A atividade não exige API paga nem treinamento de modelo.

## Primeiro marco

A versão executável com interface gráfica, busca e navegação já existe nesta branch. O avaliador já aceita o formato de perguntas exemplificado no piloto. O próximo marco é integrar a avaliação independente da Pessoa 2. Vídeo e TXT dependem do sistema e dos resultados consolidados.
