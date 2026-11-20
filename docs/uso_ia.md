# Uso de Inteligência Artificial no projeto

Este registro atende ao item "Uso de Inteligência Artificial" do enunciado. O protótipo **não usa IA para responder**. Todas as orientações vêm da base verificada em `data/base.json`, e o assistente não gera texto novo. A IA foi usada só como apoio durante o **desenvolvimento**, e tudo o que ela produziu foi revisado e testado pela equipe.

## Ferramentas e onde foram usadas

| Parte do trabalho | Ferramenta | Como a IA ajudou | Como validamos |
|---|---|---|---|
| Interpretação do enunciado e divisão de tarefas | Claude (Anthropic) | Resumo dos requisitos e proposta de divisão em 3 frentes | A equipe ajustou a divisão ao número real de integrantes |
| Base de conhecimento (`data/base.json`) | Claude | Pesquisa de fontes oficiais e redação dos resumos das 15 orientações | Cada orientação tem fonte e link identificáveis. Os links devem ser reabertos pela equipe antes da entrega (ver abaixo) |
| Documentação da base e roteiro do vídeo | Claude | Rascunho de `docs/base_conhecimento.md` e `docs/roteiro_video.md` | Revisão do texto e conferência do grafo: as 36 ligações do diagrama batem com o JSON |
| Validador da base | Claude | Primeira versão de `scripts/validar_base.py` | Executado com a base real e com arquivos ausente, vazio e inválido |
| Sistema, interface e avaliador | Codex (OpenAI) | Planejamento e implementação em Python/Tkinter, revisão da busca, casos de teste e execução do piloto | Testes automáticos, execução dos fluxos da janela e do terminal, e piloto de 17 perguntas |
| Revisão final da entrega | Claude | Conferência do repositório contra o enunciado; README completo, `docs/prompts.md`, `docs/testes.md`, sugestões na tela "sem resposta" | Testes automáticos (6, todos passando), validador e avaliador executados de novo após as mudanças |

## Validação crítica: o que a IA errou ou o que corrigimos

- **Busca por palavras-chave:** o teste "Como cancelar meu CPF?" mostrou que a busca respondia sobre inscrição no CPF, o que seria uma orientação errada. A regra foi ajustada para recusar ações (cancelar, bloquear, renovar etc.) que não aparecem no registro, e o caso entrou no conjunto de testes.
- **Pergunta não reconhecida:** "Quero saber se meu patrão assinou minha carteira" continua sem resposta direta. Mantivemos o erro registrado na tabela de testes, em vez de "forçar" a palavra na base só para acertar o teste.
- **Grafo da documentação:** o primeiro diagrama da base tinha 35 ligações, contra 36 no JSON (faltava DIR03 → SERV02). A diferença foi encontrada na conferência e corrigida.
- **Fontes:** a pesquisa da IA usou resultados de busca. Alguns links da base apontam para a página geral do órgão, e não para o passo a passo do serviço (DOC02 CPF e SERV01 conta gov.br). Por isso, a equipe precisa abrir os 15 links e confirmar o conteúdo antes da entrega.
- **Sem dados inventados:** o teste de usabilidade não foi simulado por IA. A seção correspondente em `docs/testes.md` só deve ser preenchida com uma sessão real.

## Conferência das fontes pela equipe

Marque após abrir cada link de `data/base.json` e confirmar que o resumo bate com a fonte:

- [ ] DOC01 · [ ] DOC02 · [ ] DOC03 · [ ] DOC04 · [ ] DOC05
- [ ] SERV01 · [ ] SERV02 · [ ] SERV03 · [ ] SERV04 · [ ] SERV05
- [ ] DIR01 · [ ] DIR02 · [ ] DIR03 · [ ] DIR04 · [ ] DIR05

Se algo mudou, corrija o registro, atualize `data_verificacao` e rode `python scripts/validar_base.py`.

## Compromissos da equipe

- Antes da entrega, cada integrante executa o projeto e deve saber explicar o funcionamento da busca, dos modelos de resposta e dos testes.
- O conteúdo da base é de responsabilidade da equipe, não da ferramenta de IA.
- O assistente informa sempre que não é canal oficial e indica onde confirmar a informação.
