# Revisão da entrega · 19/11/2026

O protótipo já demonstra o ciclo pedido pela FIAP. Uma pergunta entra, a busca consulta registros de um arquivo e a pessoa recebe uma orientação com fonte ou um caminho para continuar. A avaliação com alguém de fora é a principal evidência que falta para saber se isso funciona no cotidiano.

| Parte do enunciado | O que conseguimos demonstrar | O que merece atenção |
|---|---|---|
| Arquivos e organização | O mesmo leitor atende à aplicação e ao validador. A base passou com 15 registros, cinco por tema e 36 ligações. | A verificação automática confere a estrutura e as ligações entre registros. A Pessoa 1 deve reconferir a cobertura de cada fonte. Em DIR05, por exemplo, dois serviços aparecem na mesma orientação, com a referência do segundo na observação. |
| Estruturas de dados | Um dicionário recupera o registro pelo ID. Outro associa cada palavra aos possíveis registros. Uma lista de IDs permite seguir de seguro-desemprego para Carteira de Trabalho, conta gov.br e Meu INSS. | No vídeo, vale percorrer esse caminho e mostrar a lista `relacionados` de um dos registros. Assim fica visível de onde as opções vieram. |
| Busca e lógica | O programa ignora acentos e termos comuns, conta as coincidências e dá mais pontos a expressões inteiras. Candidatos com pontuações próximas aparecem para escolha. Um tema amplo, como “documento”, abre suas opções. | A regra de cobertura e a checagem de algumas ações reduzem respostas indevidas. Flexões e sinônimos ainda podem escapar. Uma resposta recuperada continua dependendo de leitura crítica. |
| Estratégias de resposta | A apresenta o texto corrido. B divide a mesma orientação em partes e inclui a observação cadastrada. Ambos exibem a fonte, a data e o aviso de confirmação aplicável. | Comparar os formatos com a mesma pergunta. Em DOC01, pedir à pessoa que localize onde confirmar os requisitos e a variação por estado. Registrar qual formato ajudou e por quê. |
| Uso, clareza e privacidade | A primeira tela oferece duas escolhas. O botão Voltar recupera a etapa anterior. A consulta normal fica só em memória. Somente as perguntas fictícias do avaliador vão para o CSV. | Verificar com uma pessoa se “Escolher um tema” e “Consultar a fonte” são compreendidos sem explicação do grupo. |
| Avaliação objetiva | O piloto tem 17 casos, com diretas, reformulações, perguntas fora do escopo e situações-limite. A tabela guarda esperado, obtido, acerto, tempo e texto de cada modelo. | Os autores conhecem a base. A Pessoa 2 deve trazer perguntas independentes e registrar o teste de usabilidade. |
| Entrega institucional | O roteiro, as instruções de execução e o repositório público da equipe existem. A interface revisada está na cópia local. | Integrar a versão final no GitHub, preencher equipe e RMs, comparar a estrutura com a Tabela 2 original na FIAP ON, gravar o vídeo não listado e entregar o TXT com os dois links. |

## O que o piloto mostra

Os modelos acertaram 16 de 17 casos cada (94,1%). Nesta execução, a média de busca e montagem foi de 0,067 ms para A e 0,068 ms para B. O cronômetro começa depois da leitura da base e termina antes de desenhar a tela. A diferença de tempo é pequena demais para orientar a escolha de formato.

A pergunta “Quero saber se meu patrão assinou minha carteira” deveria levar a DOC05. Ambos retornaram ausência de resposta. “Como cancelar meu CPF?” teve o comportamento esperado de indicar o limite. O primeiro caso mostra a dificuldade de reconhecer o vocabulário cotidiano. O segundo explica por que reconhecer uma sigla é insuficiente para orientar a pessoa.

Os dois modelos usam a mesma busca, o que explica o mesmo índice de acerto. A contagem avalia o ID, as opções ou a recusa esperada. Clareza da orientação e tempo gasto pela pessoa são outras medidas.

## Como relacionar às fases

Na demonstração, vale acompanhar “fui mandado embora” desde a leitura de `data/base.json` até SERV04. Isso torna observáveis leitura de arquivos, normalização, dicionários e condicionais. Ao abrir o próximo assunto, aparece uma aplicação de grafos. Ao mostrar o erro de DOC05 no CSV, aparece a avaliação de desempenho. Na memória de estudo da Fase 6, os capítulos 3 e 7 tratam de custo de algoritmos e avaliação. Com 15 registros, esses tempos ilustram o método de medição e dizem pouco sobre desempenho em escala.

## Duas melhorias para a próxima rodada

1. Reunir frases espontâneas antes de editar as palavras-chave. Para Carteira de Trabalho, verificar com os participantes expressões como “carteira assinada”. Reservar perguntas novas para medir o efeito depois da mudança.
2. Testar a recuperação após uma busca sem resposta. Observar se a pessoa prefere editar a pergunta ou procurar por tema. Se ela desistir, experimentar uma sugestão de assunto como pergunta de confirmação e repetir a tarefa.

## Teste de uso a realizar

Convidar alguém de fora do grupo, usar dados fictícios e evitar orientar durante as tarefas. Pedir que encontre a CIN pelo menu, consulte onde buscar orientação após uma demissão, abra a fonte e compare os dois formatos, e tente se recuperar de uma pergunta fora do tema. Para cada tarefa, registrar conclusão sem ajuda, conclusão com ajuda ou desistência, junto com o ponto de dificuldade. Guardar apenas observações anônimas em `docs/testes.md`. O piloto automático e o teste técnico da janela já foram feitos. A sessão com participante está pendente.
