# Modelos de instrução de resposta

O Citizen Assist AI não usa um modelo de linguagem para gerar respostas. Toda orientação vem da base verificada (`data/base.json`). Os "prompts" do projeto são **modelos de instrução de resposta**: regras fixas, escritas no código, que definem o papel do assistente, o formato da resposta e o que precisa aparecer sempre. Assim o assistente não inventa conteúdo, e a mesma pergunta recebe sempre a mesma resposta.

Os dois modelos usam a mesma busca. Muda só a forma de apresentar a orientação encontrada. O código está em `Sistema.trechos()` e `Sistema.resposta()` (`src/sistema.py`).

## Regras comuns aos dois modelos

Estas instruções valem para qualquer resposta:

1. **Papel:** o assistente é um orientador informativo. Não é canal oficial, não faz atendimento e não promete integração com órgãos públicos.
2. **Só responde com base no arquivo:** o texto exibido vem do campo `orientacao` de um registro. Nada é gerado ou completado.
3. **Sempre cita a fonte:** toda resposta mostra o nome da fonte, o link de referência e a data de verificação.
4. **Avisa quando a regra pode mudar:** se o registro tem `requer_confirmacao: true`, aparece "Confirme as regras atuais na fonte indicada antes de agir".
5. **Reconhece o limite:** sem correspondência segura, a resposta é "Não há informação suficiente na base", seguida de assuntos próximos ou da lista de temas. Nunca há uma resposta improvisada.
6. **Não pede dados pessoais:** a interface orienta a escrever só a dúvida.

## Modelo A — Resposta direta

**Instrução:**

> Você é um orientador informativo de serviços ao cidadão. Responda com a orientação cadastrada em um único parágrafo, na ordem original. Em seguida, mostre a fonte, o link, a data de verificação, o aviso de confirmação (quando houver) e o aviso de que o conteúdo não é oficial. Não acrescente nada que não esteja no registro.

**Formato:**

```
<pergunta do registro>

<orientação em texto corrido>

Fonte: <fonte>
Referência: <link>
Verificada em: <data>

[Confirme as regras atuais na fonte indicada antes de agir.]

<aviso geral: conteúdo informativo, não é canal oficial>
```

## Modelo B — Resposta estruturada

**Instrução:**

> Você é um orientador informativo de serviços ao cidadão. Divida a orientação cadastrada em partes curtas, uma ideia por parágrafo, mantendo a ordem: o que é ou quem tem direito, como fazer, prazos e custos. Se houver observação cadastrada (alerta de golpe, variação por estado, outro canal), mostre-a destacada no fim. Depois apresente a fonte, o link, a data, o aviso de confirmação (quando houver) e o aviso de que o conteúdo não é oficial. Não acrescente nada que não esteja no registro.

**Formato:**

```
<pergunta do registro>

<parte 1>

<parte 2>

...

Observação: <observação do registro, se houver>

Fonte: <fonte>
Referência: <link>
Verificada em: <data>

[Confirme as regras atuais na fonte indicada antes de agir.]

<aviso geral>
```

### Exemplo com a mesma pergunta: "fui mandado embora, o que eu faço?" (SERV04)

**Modelo A:**

> O seguro-desemprego é para quem trabalhava com carteira assinada e foi dispensado sem justa causa. O trabalhador formal deve fazer o pedido entre o 7º e o 120º dia corrido após a demissão. A solicitação pode ser feita pelo aplicativo Carteira de Trabalho Digital, pelo portal gov.br (com o número do requerimento entregue pela empresa) ou presencialmente em uma unidade de atendimento. As parcelas são pagas pela Caixa.

**Modelo B:**

> O seguro-desemprego é para quem trabalhava com carteira assinada e foi dispensado sem justa causa.
>
> O trabalhador formal deve fazer o pedido entre o 7º e o 120º dia corrido após a demissão.
>
> A solicitação pode ser feita pelo aplicativo Carteira de Trabalho Digital, pelo portal gov.br (com o número do requerimento entregue pela empresa) ou presencialmente em uma unidade de atendimento.
>
> As parcelas são pagas pela Caixa.
>
> **Observação:** Empregados domésticos e outras categorias têm prazos e regras próprios.

Nos dois casos, a fonte, o link, a data e os avisos aparecem em seguida.

## Comparação nas perguntas de teste

As 17 perguntas de `tests/perguntas_piloto.json` foram executadas com os dois modelos (`python tests/avaliar.py`). A tabela completa, com o texto de cada resposta, está em `tests/resultados_perguntas_piloto.csv`.

| Critério | Modelo A | Modelo B |
|---|---|---|
| Acerto da orientação recuperada | 16/17 (94,1%) | 16/17 (94,1%) |
| Tempo médio de busca e montagem | ~0,08 ms | ~0,08 ms |
| Fonte, link e data em todas as respostas | Sim | Sim |
| Aviso de confirmação quando exigido | Sim | Sim |
| Mostra a observação do registro (alertas e variações) | **Não** (0 de 13 registros que têm observação) | **Sim** (13 de 13) |
| Estrutura do texto | 1 bloco de ~64 palavras, em média | ~4,8 partes curtas por resposta, em média |

**Como ler esses números:**

- **O acerto e o tempo são iguais** porque os dois modelos usam a mesma busca. O modelo de resposta não muda qual orientação é encontrada, só a forma de apresentá-la. Por isso, a escolha precisa se basear em clareza e consistência, e não na taxa de acerto.
- **O modelo B é mais completo.** O A omite a observação de 13 dos 15 registros, e é justamente ali que estão alertas importantes, como "desconfie de quem cobra pela inscrição no CPF", "o INSS não pede senha por WhatsApp" e "domésticos têm prazos próprios". Uma resposta que esconde esses alertas é menos segura para o cidadão.
- **O modelo B é mais fácil de ler.** Separar uma ideia por parágrafo ajuda quem lê no celular, quem tem pouca familiaridade com o assunto e quem usa leitor de tela, porque cada parte é lida como um bloco independente. Prazos e valores ("entre o 7º e o 120º dia") ficam mais visíveis.
- **O modelo B é mais consistente.** Todas as respostas seguem a mesma ordem (o que é, como fazer, observação, fonte), independentemente do registro.

**Decisão:** o **modelo B** é o padrão do sistema, tanto na interface gráfica quanto no terminal. O modelo A continua disponível pelo botão "Ler em texto corrido" e pela opção 3 do menu do terminal, para quem prefere ler tudo de uma vez.

**Limitação desta comparação:** os critérios de clareza acima foram avaliados pela equipe. O teste de usabilidade (`docs/testes.md`) inclui uma tarefa em que o participante compara os dois formatos, para confirmar ou rever essa escolha com alguém de fora do grupo.
