# Citizen Assist AI — Global Solution FIAP 2026.2

Assistente digital de orientação cidadã, desenvolvido para o desafio **CitizenTech** da Global Solution 2026.2. Ele responde dúvidas do dia a dia sobre documentos, serviços públicos e direitos usando uma base de orientações verificadas. Toda resposta mostra a fonte oficial, e o assistente avisa quando não tem informação suficiente.

> ⚠️ Projeto acadêmico. O Citizen Assist AI **não é canal oficial** de nenhum órgão público. Confirme sempre as regras atuais na fonte indicada.

## Equipe

**Nome da equipe:** _[preencher]_

| Integrante | RM | Responsabilidade |
|---|---|---|
| Guilherme Alves Nunes | rm572754 | Base de conhecimento, fontes, documentação da base e roteiro do vídeo |
| Pedro Henrique de Souza Elias |rm570487 | Perguntas de teste, métricas, usabilidade e documentação |
| Gabriel Leão Rocha | rm571330 | Sistema, interface, avaliador, integração e vídeo |

**Vídeo de apresentação (YouTube, não listado):** https://youtu.be/qtDNt3mKRD0

---

## 1. Problema, público e temas

**Problema.** Quem precisa tirar um documento, pedir um benefício ou entender um direito costuma encontrar informações espalhadas em vários sites, com termos técnicos e instruções incompletas. Isso gera perda de tempo, erros e golpes (pessoas pagando por serviços gratuitos, por exemplo).

**Público beneficiado.** Cidadãos com pouca familiaridade com serviços digitais do governo: jovens tirando os primeiros documentos, trabalhadores recém-demitidos, famílias de baixa renda em busca de programas sociais e consumidores com problemas em compras.

**Temas abordados (15 orientações):**

| Documentação | Serviços públicos | Direitos e orientação comunitária |
|---|---|---|
| Carteira de Identidade Nacional (CIN) | Conta gov.br (níveis) | Direito de arrependimento (7 dias) |
| CPF | Meu INSS | Reclamação contra empresa |
| Segunda via de certidão | Cadastro Único | Defensoria Pública |
| Título de eleitor | Seguro-desemprego | Juizado Especial Cível |
| Carteira de Trabalho Digital | Cartão do SUS | Disque 100 / Ligue 180 |

## 2. Como executar

Requisitos: **Python 3.10 ou superior**. Não há pacotes externos. A interface gráfica usa Tkinter, que já vem com o Python no Windows.

Na raiz do repositório:

```bash
python src/sistema.py              # interface gráfica (padrão)
python src/sistema.py --terminal   # interface de texto
```

Outros comandos:

```bash
python scripts/validar_base.py           # confere a base de conhecimento
python -m unittest discover -s tests     # testes automáticos
python tests/avaliar.py                  # roda as perguntas de teste e gera o CSV de resultados
```

## 3. Organização do repositório

```
├── README.md
├── PLANO_EXECUCAO.md                # planejamento e decisões da equipe
├── data/
│   └── base.json                 # base de conhecimento (15 orientações)
├── src/
│   ├── sistema.py                # carga, validação, busca, respostas e modo terminal
│   └── interface.py              # interface gráfica (Tkinter)
├── scripts/
│   └── validar_base.py           # validador da base
├── tests/
│   ├── test_sistema.py           # testes automáticos
│   ├── avaliar.py                # avaliador das perguntas de teste
│   ├── perguntas_piloto.json     # 17 perguntas com resposta esperada
│   └── resultados_perguntas_piloto.csv
└── docs/
    ├── base_conhecimento.md      # campos, hierarquia, grafo e fontes
    ├── prompts.md                # modelos de resposta A e B e comparação
    ├── testes.md                 # plano de testes, indicadores e usabilidade
    ├── uso_ia.md                 # registro do uso de IA
    ├── roteiro_video.md          # roteiro da apresentação
    └── revisao_entrega.md        # revisão técnica da equipe
```

## 4. Base de conhecimento, estruturas e estratégia de busca

### Base
`data/base.json` tem três partes: metadados com o aviso de conteúdo não oficial, a **hierarquia de temas** (3 temas e 12 subtemas) e a **lista de 15 registros**. Cada registro tem: `id`, `tema`, `subtema`, `pergunta`, `palavras_chave`, `orientacao`, `fonte`, `referencia` (link), `data_verificacao`, `requer_confirmacao`, `observacao` e `relacionados`. Todas as orientações foram resumidas a partir de fontes oficiais (gov.br, TSE, INSS e leis no site do Planalto). Detalhes em [`docs/base_conhecimento.md`](docs/base_conhecimento.md).

A base fica **separada do código**. Para acrescentar ou corrigir uma orientação, basta editar o JSON e rodar o validador, sem mexer no programa.

**Tratamento de erros na leitura:** arquivo ausente, vazio, JSON inválido, campo obrigatório faltando, id duplicado, tema inexistente, link inválido, data fora do formato ou relação para um id inexistente geram uma mensagem clara (`ErroBase`), e o programa não trava.

### Estruturas de dados
- **Lista** `registros`: todas as orientações, na ordem do arquivo.
- **Dicionário** `por_id`: acesso direto a um registro pelo identificador.
- **Dicionários** `por_tema` e `por_subtema`: listas de ids usadas no menu.
- **Dicionário invertido** `por_palavra`: cada palavra-chave aponta para o conjunto de registros que a contêm.
- **Árvore** tema → subtema → registro, para a navegação pelo menu.
- **Grafo dirigido** pelo campo `relacionados` (36 ligações), que permite seguir de um assunto para outro. Exemplo: Seguro-desemprego → Carteira de Trabalho Digital → Conta gov.br → Meu INSS.

### Estratégia de busca
1. **Normalização:** a pergunta vai para minúsculas, sem acentos e sem pontuação, e palavras comuns ("como", "de", "o", "quero") são descartadas.
2. **Pedido de tema inteiro:** se a pessoa digita só o nome de um tema ("documento"), o sistema lista as orientações daquele tema.
3. **Candidatos:** o índice `por_palavra` reúne os registros que têm pelo menos uma palavra da pergunta.
4. **Pontuação:** palavras em comum com as palavras-chave valem 1 ponto, palavras em comum com a pergunta do registro valem mais 1, e uma **expressão inteira** encontrada ("seguro desemprego", "mandado embora") vale um bônus maior.
5. **Filtros de segurança:**
   - se a pergunta pede uma ação que o registro não cobre ("cancelar", "bloquear", "renovar"), ele é descartado;
   - se menos da metade das palavras da pergunta é conhecida pelo registro, ele também é descartado. Isso evita responder errado só porque uma sigla apareceu.
6. **Decisão:**
   - um vencedor claro → mostra a orientação;
   - **várias correspondências** com pontuação próxima (diferença de até 1 ponto) → mostra até 5 opções em ordem de pontuação para a pessoa escolher;
   - nenhum candidato com pontuação mínima → informa o limite e sugere assuntos próximos.

## 5. Regras de resposta, modelos de prompt e limitações

O assistente não usa um modelo de linguagem: as respostas seguem **modelos de instrução** fixos, aplicados sobre o texto verificado. Em todas as respostas o assistente:

- se apresenta como orientador informativo, nunca como canal oficial;
- usa **só** o texto da base, sem inventar instruções;
- mostra **fonte, link e data de verificação**;
- exibe "Confirme as regras atuais na fonte indicada" quando a orientação depende de prazos, valores ou regras locais (`requer_confirmacao`).

**Dois modelos de resposta** ([`docs/prompts.md`](docs/prompts.md)):

- **Modelo A — Resposta direta:** a orientação em um único parágrafo.
- **Modelo B — Resposta estruturada:** uma ideia por parágrafo e a observação destacada (alertas de golpe, variações por estado).

Os dois acertaram 16 de 17 perguntas, porque usam a mesma busca. O **modelo B foi escolhido como padrão** porque mostra as observações que o A omite (13 de 15 registros têm uma) e é mais fácil de ler em partes. O modelo A continua disponível ("Ler em texto corrido" ou opção 3 no terminal).

**Tratamento das limitações:**

| Situação | Comportamento |
|---|---|
| Entrada vazia | "Digite uma pergunta para consultar." |
| Opção inexistente no menu | "Opção inválida." e o menu reaparece |
| Pergunta ambígua | Lista as orientações possíveis para a pessoa escolher |
| Pergunta sem correspondência | "Não há informação suficiente na base para responder com segurança.", mais assuntos próximos ou a lista de temas |
| Ação não coberta ("cancelar CPF") | Recusa, em vez de responder sobre inscrição no CPF |

## 6. Exemplos de uso

**Pergunta reformulada:** `fui mandado embora, o que eu faço?`

```
Como pedir o seguro-desemprego?

O seguro-desemprego é para quem trabalhava com carteira assinada e foi dispensado sem justa causa.

O trabalhador formal deve fazer o pedido entre o 7º e o 120º dia corrido após a demissão.

A solicitação pode ser feita pelo aplicativo Carteira de Trabalho Digital, pelo portal gov.br (...) ou presencialmente em uma unidade de atendimento.

As parcelas são pagas pela Caixa.

Observação: Empregados domésticos e outras categorias têm prazos e regras próprios.

Fonte: Ministério do Trabalho e Emprego - gov.br
Referência: https://www.gov.br/pt-br/servicos/solicitar-o-seguro-desemprego
Verificada em: 2026-11-17

Confirme as regras atuais na fonte indicada antes de agir.

Assuntos relacionados:
1. Como obter a Carteira de Trabalho Digital?
2. O que são os níveis bronze, prata e ouro da conta gov.br?
3. Como funciona o Juizado Especial Cível (pequenas causas)?
```

**Pergunta ambígua:** `documento`

```
Encontramos mais de uma orientação possível. Escolha a que melhor descreve sua dúvida:
1. Como tirar a nova Carteira de Identidade Nacional (CIN)?
2. Como fazer o CPF ou consultar minha situação cadastral?
3. Como pedir a segunda via da certidão de nascimento?
4. Como tirar o título de eleitor pela primeira vez?
5. Como obter a Carteira de Trabalho Digital?
```

**Pergunta fora dos temas:** `vai chover amanhã?`

```
Não há informação suficiente na base para responder com segurança.
Não vamos inventar uma orientação. Consulte o canal oficial do órgão responsável.
Temas disponíveis (opção 1 do menu): Documentação, Serviços públicos, Direitos e orientação comunitária.
```

**Pergunta sem resposta direta, com sugestão:** `quero saber se meu patrão assinou minha carteira`

```
Não há informação suficiente na base para responder com segurança.
Não vamos inventar uma orientação. Consulte o canal oficial do órgão responsável.

Talvez algum destes assuntos ajude:
1. Como tirar a nova Carteira de Identidade Nacional (CIN)?
2. Como obter a Carteira de Trabalho Digital?
```

**Entrada vazia:** `Digite uma pergunta para consultar.` · **Opção inexistente (ex.: 9):** `Opção inválida.`

## 7. Plano de testes, indicadores e resultados

Plano completo e tabela pergunta a pergunta em [`docs/testes.md`](docs/testes.md).

- **17 perguntas de teste:**
  - 5 diretas;
  - 6 reformuladas;
  - 2 fora do tema;
  - 4 situações-limite: vazia, ambígua, sem resposta confiável e ação não coberta.
- **Taxa de acerto:** 16/17 = **94,1%** nos dois modelos.
- **Tempo médio de consulta:** cerca de **0,08 ms** (varia por máquina e execução).
- **Respostas inventadas:** **0**. Todas as perguntas fora da base receberam o aviso de limite.
- **Testes automáticos:** 6/6 passando.
- **Teste de usabilidade:** roteiro de 5 tarefas em `docs/testes.md`, seção 5. _[1 participante concluiu as 5 tarefas do roteiro sem ajuda, cada uma em menos de 1 minuto, preferiu o modelo B (texto por partes) e avaliou o assistente como "bem fácil de entender". Detalhes em `docs/testes.md`, seção 5.]_

**Interpretação.** A busca acerta as perguntas dentro do escopo e recusa corretamente as que estão fora dele, o que é essencial para não orientar errado. O único erro ("meu patrão assinou minha carteira") mostra o limite da busca por palavras-chave quando a pessoa usa vocabulário que não está cadastrado. Nesse caso, o sistema agora sugere a Carteira de Trabalho Digital como assunto próximo. O tempo é irrelevante para uma base deste tamanho.

## 8. Clareza, acessibilidade, privacidade e informação não oficial

- **Linguagem clara:** orientações curtas, sem juridiquês, com a pergunta escrita como o cidadão perguntaria.
- **Acessibilidade:**
  - uma decisão por tela;
  - botão Voltar e tecla Esc;
  - texto dividido em partes (modelo B);
  - contraste alto na interface;
  - modo terminal como alternativa para leitores de tela.
- **Privacidade:** o assistente **não pede nenhum dado pessoal** (nome, CPF, endereço). A tela de pergunta orienta a escrever só a dúvida, as consultas ficam apenas na memória durante o uso e nada é salvo em arquivo.
- **Informação não oficial:** toda resposta traz o aviso de que o conteúdo é informativo, a fonte oficial e a data de verificação. O sistema não promete integração com órgãos públicos.
- **Segurança do cidadão:** as observações alertam para golpes, como cobranças pelo CPF ou pedidos de senha do INSS por WhatsApp.

## 9. Conclusões, limitações e melhorias

**Conclusões.** O protótipo cumpre o fluxo completo pedido: recebe a pergunta, consulta uma base organizada, apresenta a orientação com fonte e trata o que não sabe sem inventar. Fundamentos simples (arquivos, listas, dicionários, condicionais e um grafo de relações) bastam para um assistente útil e transparente, desde que a base seja bem cuidada.

**Limitações.**

- A base tem só 15 orientações e informações gerais, que variam por estado ou município em alguns casos.
- A busca por palavras-chave não entende sinônimos nem flexões que não estejam cadastrados.
- As perguntas de teste foram escritas pela própria equipe.
- As fontes precisam ser reconferidas periodicamente, porque regras e prazos mudam.

**Melhorias possíveis.**

1. Ampliar as palavras-chave com frases reais coletadas de usuários.
2. Tratar sinônimos e radicais das palavras.
3. Perguntar "Você quis dizer...?" antes de mostrar uma sugestão.
4. Ampliar a base para outros temas (habitação, educação, transporte).
5. Criar um alerta automático para orientações com data de verificação antiga.

## 10. Uso de IA

Ferramentas de IA apoiaram a pesquisa das fontes, a redação, a implementação e a revisão. O protótipo **não usa IA para responder**. Registro completo e validação crítica em [`docs/uso_ia.md`](docs/uso_ia.md).
