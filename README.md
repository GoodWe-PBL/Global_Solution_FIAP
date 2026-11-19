# Citizen Assist AI — Global Solution FIAP 2026.2

Protótipo acadêmico de orientação cidadã. Consulta uma base local com 15 orientações sobre documentação, serviços públicos e direitos, mostra a fonte e a data de verificação e oferece caminhos para assuntos relacionados. A interface gráfica usa uma paleta inspirada no magenta, preto e branco da FIAP.

## Como executar

Requer Python 3.10 ou superior com Tkinter instalado. No Windows, Tkinter costuma acompanhar a instalação padrão do Python. Não são necessários pacotes externos.

Na raiz do repositório:

```bash
python src/sistema.py
```

Na primeira tela, escolha **Escrever minha pergunta** ou **Escolher um tema**. A aplicação mostra uma decisão por vez. Use **Voltar** ou Esc para retornar. Na orientação, você pode consultar a fonte, ler o texto por partes e seguir para assuntos relacionados.

Para usar o modo terminal:

```bash
python src/sistema.py --terminal
```

Para verificar a estrutura da base:

```bash
python scripts/validar_base.py
```

## Base e busca

`data/base.json` reúne 15 registros divididos em 3 temas, com 36 ligações entre assuntos. `docs/base_conhecimento.md` explica os campos, a hierarquia e as fontes. O programa usa dicionários para encontrar orientações por ID, tema, subtema e palavras-chave. Normaliza acentos, maiúsculas e pontuação. Perguntas amplas ou com mais de uma correspondência apresentam opções; perguntas sem base suficiente recebem uma mensagem de limite.

Exemplos: “como tirar o título de eleitor?”, “fui mandado embora, o que eu faço?”, “documento” e “qual a previsão do tempo amanhã?”.

O conteúdo é informativo e não constitui atendimento oficial. A aplicação não solicita dados pessoais. Confirme regras que possam mudar na fonte indicada.

## Organização

- `src/sistema.py`: carregamento, validação, busca, respostas e modo terminal.
- `src/interface.py`: interface gráfica Tkinter.
- `data/base.json`: orientações recebidas da Pessoa 1.
- `scripts/validar_base.py`: validador estrutural da base.
- `docs/base_conhecimento.md`: descrição da base e fontes.
- `docs/roteiro_video.md`: roteiro da apresentação.
- `PLANO_EXECUCAO.md`: plano e responsabilidades.

## Avaliação

Execute `python tests/avaliar.py` para gerar o CSV na pasta `tests`. O avaliador lê `perguntas_teste.json` quando esse arquivo da Pessoa 2 estiver disponível. Até lá usa `perguntas_piloto.json`, que serve também de exemplo dos campos. É possível escolher outra coleção com `python tests/avaliar.py caminho/arquivo.json`. Para rodar os testes técnicos, use `python -m unittest discover -s tests`.

No piloto, cada modelo acertou 16 de 17 casos. A pergunta sobre o patrão ter assinado a carteira ficou sem resposta. A análise das métricas, o roteiro de usabilidade e as pendências de entrega estão na [revisão da entrega](docs/revisao_entrega.md). A contribuição de IA para esta parte está no [registro de uso](docs/uso_ia.md).
