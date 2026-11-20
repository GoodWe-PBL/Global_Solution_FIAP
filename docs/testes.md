# Plano de testes, indicadores e resultados

## 1. O que foi avaliado

| Avaliação | Como | Onde está |
|---|---|---|
| Acerto das respostas | 17 perguntas de teste com resposta esperada, executadas nos dois modelos | `tests/perguntas_piloto.json`, `tests/resultados_perguntas_piloto.csv` |
| Tempo de consulta | Cronômetro (`time.perf_counter`) da busca até a resposta montada | Mesmo CSV, coluna `tempo_ms` |
| Funcionamento técnico | 6 testes automáticos (perguntas, limites, fonte, navegação, base inválida, sugestões) | `tests/test_sistema.py` |
| Integridade da base | Campos, ids, temas, links e relações | `scripts/validar_base.py` |
| Facilidade de uso | Roteiro de tarefas com participante de fora do grupo | Seção 5 deste documento |

Para reproduzir:

```bash
python scripts/validar_base.py
python -m unittest discover -s tests
python tests/avaliar.py
```

## 2. Perguntas de teste

As 17 perguntas cobrem os tipos pedidos no enunciado:

| Tipo | Qtd. | Exemplos |
|---|---|---|
| Diretas | 5 | "Como tirar o RG?", "Como acessar o Meu INSS?" |
| Reformuladas (linguagem do dia a dia) | 6 | "Fui mandado embora, o que eu faço?", "Não tenho dinheiro para advogado" |
| Fora dos temas | 2 | "Vai chover amanhã?", "Onde renovar meu passaporte?" |
| Situações-limite | 4 | entrada vazia, "documento" (ambígua), endereço de agência (sem resposta confiável), "Como cancelar meu CPF?" |

Uma resposta conta como **acerto** quando o sistema retorna exatamente o resultado esperado: a orientação certa, as opções certas (para consultas ambíguas) ou o aviso de limite (para perguntas sem base).

## 3. Resultados

| ID | Tipo | Pergunta | Esperado | Obtido | Acerto |
|---|---|---|---|---|---|
| T01 | direta | Como tirar o RG? | DOC01 | DOC01 | ✅ |
| T02 | direta | Onde consultar o CPF? | DOC02 | DOC02 | ✅ |
| T03 | direta | Como tirar o título de eleitor? | DOC04 | DOC04 | ✅ |
| T04 | direta | Como acessar o Meu INSS? | SERV02 | SERV02 | ✅ |
| T05 | direta | Como pedir seguro-desemprego? | SERV04 | SERV04 | ✅ |
| T06 | reformulada | Fui mandado embora, o que eu faço? | SERV04 | SERV04 | ✅ |
| T07 | reformulada | Não tenho dinheiro para advogado | DIR03 | DIR03 | ✅ |
| T08 | reformulada | Quero reclamar de uma empresa | DIR02 | DIR02 | ✅ |
| T09 | reformulada | Perdi a certidão, o que faço? | DOC03 | DOC03 | ✅ |
| T10 | reformulada | Preciso da minha carteira digital para trabalhar | DOC05 | DOC05 | ✅ |
| T11 | fora do tema | Vai chover amanhã? | sem resposta | sem resposta | ✅ |
| T12 | fora do tema | Onde renovar meu passaporte? | sem resposta | sem resposta | ✅ |
| T13 | limite | (entrada vazia) | pedir pergunta | pedir pergunta | ✅ |
| T14 | limite | documento | 5 opções de Documentação | 5 opções de Documentação | ✅ |
| T15 | limite | Endereço da agência do INSS perto da minha casa | sem resposta | sem resposta | ✅ |
| T16 | reformulada | Quero saber se meu patrão assinou minha carteira | DOC05 | sem resposta | ❌ |
| T17 | limite | Como cancelar meu CPF? | sem resposta | sem resposta | ✅ |

### Indicadores

| Indicador | Modelo A | Modelo B |
|---|---|---|
| Taxa de acerto | 16/17 = **94,1%** | 16/17 = **94,1%** |
| Tempo médio de consulta | ~0,08 ms | ~0,08 ms |
| Respostas com fonte, link e data | 100% | 100% |
| Respostas inventadas para perguntas fora da base | 0 | 0 |

Os tempos variam um pouco a cada execução (de 0,06 a 0,09 ms nas rodadas feitas) e dependem da máquina. O cronômetro começa depois da leitura do arquivo e termina antes de a tela ser desenhada.

## 4. Interpretação

- **A busca acerta quase tudo dentro do escopo e recusa corretamente o que está fora dele.** Nenhuma das 6 perguntas fora do tema ou de limite recebeu uma orientação indevida. Para um assistente cidadão, isso importa mais do que responder tudo: errar com confiança é pior do que dizer "não sei".
- **O único erro (T16) mostra o ponto fraco da busca por palavras-chave.** "Meu patrão assinou minha carteira" fala de Carteira de Trabalho com palavras que não estão cadastradas ("patrão", "assinou"). Como menos da metade das palavras da pergunta coincidia com o registro, o sistema preferiu não responder. Depois desta avaliação, a tela de "sem resposta" passou a sugerir assuntos próximos, e nesse caso a Carteira de Trabalho Digital aparece como sugestão. O erro continua contado, porque a resposta direta não foi dada.
- **O tempo não é um problema.** Com 15 registros, a busca leva menos de um milésimo de segundo. O número serve para mostrar o método de medição, não para prever o desempenho com milhares de registros.
- **Os dois modelos empatam no acerto** porque usam a mesma busca. A comparação de clareza está em `docs/prompts.md`.

## 5. Teste de facilidade de uso

**Como foi aplicado:** um participante usou a interface gráfica (`python src/sistema.py`) seguindo um roteiro de 5 tarefas, sem ajuda durante a execução. Não foram registrados dados pessoais do participante.

| # | Tarefa para o participante | Resultado | Tempo aprox. | Observações |
|---|---|---|---|---|
| 1 | Encontrar, pelo menu, como tirar a nova carteira de identidade | Concluída sem ajuda | Menos de 1 min | Nenhuma dificuldade relatada |
| 2 | Encontrar uma orientação escrevendo uma pergunta | Concluída sem ajuda | Menos de 1 min | O participante digitou "Como tirar o título de eleitor?" e o sistema retornou a orientação correspondente (DOC04) |
| 3 | Abrir a fonte oficial da orientação encontrada | Concluída sem ajuda | Menos de 1 min | Encontrou o botão "Consultar a fonte" |
| 4 | Comparar "Ler em texto corrido" (modelo A) e "Ler por partes" (modelo B) | Concluída sem ajuda | Menos de 1 min | Preferiu o texto por partes (modelo B): "achei mais simples de usar" |
| 5 | Fazer uma pergunta fora do tema e seguir para outro assunto | Concluída sem ajuda | Menos de 1 min | Entendeu a mensagem de limite e conseguiu continuar a navegação |

**Resumo:** 5 de 5 tarefas concluídas sem ajuda, todas em menos de 1 minuto. Na avaliação geral, o participante disse que o assistente foi "bem fácil de entender".

**Formato preferido na tarefa 4:** modelo B (texto por partes), por ser mais simples de usar. Isso confirma a escolha do modelo B como padrão, descrita em `docs/prompts.md`.

**Observação sobre o roteiro:** na tarefa 2, o participante escolheu sua própria pergunta (título de eleitor) em vez do cenário de demissão sugerido. O objetivo da tarefa, que era encontrar uma orientação digitando uma pergunta, foi mantido.

**Limitações deste teste:** foi feito com um único participante e os tempos foram estimados, não cronometrados. O resultado indica que a navegação é compreensível para alguém de fora, mas não substitui um teste com mais pessoas e perfis diferentes (por exemplo, quem tem pouca familiaridade com computador).

## 6. Melhorias propostas

1. **Ampliar o vocabulário com frases reais.** Coletar como as pessoas de fato perguntam (por exemplo, "carteira assinada", "patrão", "registro") e acrescentá-las às `palavras_chave`. Reservar perguntas novas, que não foram usadas para ajustar a base, para medir o efeito da mudança.
2. **Tratar sinônimos e variações de palavras.** Reduzir palavras ao radical ("assinou" → "assin") ou usar uma pequena tabela de sinônimos, para reconhecer flexões sem precisar cadastrar cada forma.
3. **Confirmar a sugestão quando não há resposta.** Hoje o sistema sugere assuntos próximos. Uma evolução é perguntar "Você quis dizer: Como obter a Carteira de Trabalho Digital?" e medir quantas pessoas aceitam a sugestão.

## 7. Limitações da avaliação

- **As perguntas foram escritas pela equipe**, que conhece a base. Isso tende a inflar a taxa de acerto. Perguntas escritas por pessoas de fora dariam uma medida mais realista.
- **A amostra é pequena:** 17 perguntas e poucos participantes no teste de uso. Os números indicam tendências, não conclusões estatísticas.
- **O acerto mede se a orientação certa foi encontrada,** não se a pessoa entendeu e conseguiu agir. Isso só o teste de uso mostra.
- **A validação da base é estrutural.** O script confere campos e ligações, mas não se o conteúdo das fontes mudou. A conferência das fontes é manual e tem data registrada em cada orientação.
