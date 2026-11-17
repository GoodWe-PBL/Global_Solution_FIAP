# Roteiro do vídeo — Citizen Assist AI

**Duração alvo:** 6 a 7 minutos (confirmar o limite no enunciado da FIAP ON).
**Formato:** gravação de tela do terminal e da documentação, com narração. Cada integrante apresenta a parte que fez.
**Publicação:** YouTube como **"Não Listado"**.

> Os trechos entre [colchetes] devem ser preenchidos com os resultados reais dos testes antes da gravação.

---

## Cena 1 — Abertura e problema (0:00 – 0:40)
**Quem fala:** Pessoa 1
**Tela:** título do projeto (README no GitHub) com nome da equipe e RMs.

> "Olá, somos a equipe [nome], e este é o Citizen Assist AI. Quando alguém precisa tirar um documento, pedir um benefício ou entender um direito, as informações costumam estar espalhadas, com termos difíceis e instruções incompletas. Nosso assistente organiza orientações verificadas, responde perguntas simples do dia a dia e sempre mostra a fonte oficial. Ele também avisa quando não sabe a resposta."

## Cena 2 — Base de conhecimento (0:40 – 1:40)
**Quem fala:** Pessoa 1
**Tela:** `data/base.json` aberto, depois o diagrama do grafo em `docs/base_conhecimento.md`.

> "A base tem 15 orientações divididas em 3 temas: Documentação, Serviços públicos e Direitos. Cada registro tem identificador, tema, subtema, pergunta, palavras-chave, orientação resumida, fonte, link de referência e data de verificação. Todas as informações foram conferidas em fontes oficiais, como gov.br, TSE, INSS e o texto das leis no site do Planalto."

> "Os temas formam uma hierarquia, que é usada no menu. Além disso, cada registro aponta para assuntos relacionados, formando um grafo. Por exemplo: seguro-desemprego leva à Carteira de Trabalho Digital, que leva à conta gov.br, que leva ao Meu INSS."

**Mostrar rapidamente:** rodar `python scripts/validar_base.py` e mostrar a saída "OK: 15 registros válidos".

## Cena 3 — Demonstração do sistema (1:40 – 4:00)
**Quem fala:** Pessoa 3
**Tela:** terminal com `python src/sistema.py`.

1. **Menu de temas**: escolher *Documentação → Identificação → CIN*. Mostrar a resposta, a fonte, o link e o aviso de confirmação.
   > "Toda resposta vem com a fonte, a data em que foi verificada e, quando a regra pode mudar, um aviso para confirmar no canal oficial."
2. **Pergunta direta**: digitar *"como tirar o título de eleitor?"*.
3. **Pergunta reformulada**: digitar *"fui mandado embora, o que eu faço?"*, que deve encontrar o seguro-desemprego.
   > "Mesmo sem usar as palavras exatas, a busca encontra a orientação pelas palavras-chave."
4. **Navegação**: a partir do seguro-desemprego, escolher um assunto relacionado e seguir por pelo menos 3 assuntos.
5. **Várias correspondências**: digitar *"documento"*. O sistema mostra as opções mais próximas e pede para escolher.
6. **Fora do tema**: digitar *"qual a previsão do tempo amanhã?"*. O sistema avisa que não tem base suficiente e sugere temas.
7. **Entrada vazia e opção inválida**: apertar Enter sem digitar nada e depois escolher a opção "99" no menu.
   > "O assistente nunca inventa uma resposta e não se apresenta como canal oficial. Ele também não pede nenhum dado pessoal."

## Cena 4 — Modelos de resposta (4:00 – 4:40)
**Quem fala:** Pessoa 3
**Tela:** os dois modelos lado a lado, ou `docs/prompts.md`.

> "Criamos dois modelos de resposta. O modelo A é simples e mostra só a orientação e a fonte. O modelo B é estruturado: define o papel do assistente, separa a resposta em partes e obriga a citação da fonte e do aviso. Nos testes, o modelo [A/B] foi mais claro e consistente porque [motivo]."

## Cena 5 — Testes e indicadores (4:40 – 5:50)
**Quem fala:** Pessoa 2
**Tela:** saída do `tests/avaliar.py` e tabela em `docs/testes.md`.

> "Rodamos [12] perguntas de teste: diretas, reformuladas, fora do tema e 3 situações-limite (entrada vazia, pergunta ambígua e pergunta sem resposta confiável). A taxa de acerto foi de [X]%, com tempo médio de consulta de [Y] milissegundos."

> "No teste de usabilidade, [N] pessoa(s) seguiram um roteiro de tarefas. As principais dificuldades foram [dificuldades]."

> "Com base nisso, propomos duas melhorias: [melhoria 1] e [melhoria 2]. A avaliação tem limitações: poucas perguntas de teste, poucos usuários e uma base de apenas 15 orientações."

## Cena 6 — Responsabilidade e encerramento (5:50 – 6:40)
**Quem fala:** Pessoa 1
**Tela:** seção de cuidados do README, depois o repositório no GitHub.

> "Tivemos cuidado com linguagem clara, privacidade e transparência: o sistema não coleta dados pessoais, não promete integração com órgãos públicos e sempre indica onde confirmar a informação. O uso de IA no desenvolvimento está registrado em `docs/uso_ia.md`. Como próximos passos, queremos ampliar a base e melhorar a busca. Obrigado!"

---

## Checklist antes de gravar
- [ ] Resultados reais dos testes preenchidos nos [colchetes].
- [ ] `python src/sistema.py` rodando sem erros, com as perguntas da Cena 3 já testadas.
- [ ] Fonte do terminal aumentada (fácil de ler no vídeo).
- [ ] Nenhum dado pessoal, senha ou aba privada aparecendo na tela.
- [ ] Áudio testado e o tempo total dentro do limite.
- [ ] Vídeo publicado como "Não Listado" e link testado em uma aba anônima.
