import argparse
import csv
import json
import sys
from pathlib import Path
from time import perf_counter

PASTA = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA.parent / "src"))
from sistema import Sistema, carregar_base


def avaliar(sistema, casos):
    linhas = []
    vistos = set()
    for caso in casos:
        teste = caso["id"]
        status = caso["status_esperado"]
        if teste in vistos or not isinstance(caso["pergunta"], str):
            raise ValueError(f"Confira o identificador e a pergunta de {teste}.")
        vistos.add(teste)
        if status == "encontrado":
            esperados = [caso["id_esperado"]]
        elif status == "ambiguo":
            esperados = caso["ids_esperados"]
            if len(set(esperados)) < 2:
                raise ValueError(f"{teste} precisa de duas opções esperadas.")
        elif status in ("sem_resposta", "vazia"):
            esperados = []
        else:
            raise ValueError(f"Resultado esperado desconhecido em {teste}.")
        if any(codigo not in sistema.por_id for codigo in esperados):
            raise ValueError(f"{teste} indica uma orientação inexistente.")
        for modelo in ("A", "B"):
            inicio = perf_counter()
            resultado = sistema.buscar(caso["pergunta"])
            resposta = ""
            if resultado.status == "encontrado":
                resposta = sistema.resposta(resultado.ids[0], modelo)
            tempo_ms = (perf_counter() - inicio) * 1000
            acerto = status == resultado.status and set(esperados) == set(resultado.ids)
            linhas.append(dict(teste=teste, modelo=modelo, pergunta=caso["pergunta"],
                               esperado=" ".join([status, *esperados]).strip(),
                               obtido=" ".join([resultado.status, *resultado.ids]).strip(),
                               acerto=acerto, tempo_ms=round(tempo_ms, 4), orientacao=resposta))
    return linhas


def main():
    parser = argparse.ArgumentParser(description="Avalia as perguntas usando a busca do assistente.")
    oficial = PASTA / "perguntas_teste.json"
    padrao = oficial if oficial.exists() else PASTA / "perguntas_piloto.json"
    parser.add_argument("perguntas", nargs="?", type=Path, default=padrao)
    parser.add_argument("--saida", type=Path)
    args = parser.parse_args()
    saida = args.saida or args.perguntas.with_name("resultados_" + args.perguntas.stem + ".csv")
    if saida.suffix.lower() != ".csv":
        parser.error("Use um arquivo CSV para os resultados.")
    try:
        casos = json.loads(args.perguntas.read_text(encoding="utf-8-sig"))
        if not isinstance(casos, list) or not casos:
            raise ValueError("Inclua pelo menos uma pergunta.")
        linhas = avaliar(Sistema(carregar_base()), casos)
        with saida.open("w", encoding="utf-8-sig", newline="") as arquivo:
            tabela = csv.DictWriter(arquivo, fieldnames=linhas[0].keys())
            tabela.writeheader()
            tabela.writerows(linhas)
    except (OSError, ValueError, KeyError, TypeError) as erro:
        parser.exit(1, f"Não foi possível avaliar as perguntas: {erro}\n")
    print("Perguntas:", args.perguntas.name)
    for modelo in ("A", "B"):
        grupo = [linha for linha in linhas if linha["modelo"] == modelo]
        acertos = sum(linha["acerto"] for linha in grupo)
        media = sum(linha["tempo_ms"] for linha in grupo) / len(grupo)
        print(f"{modelo}: {acertos}/{len(grupo)} ({acertos/len(grupo):.1%}), média de {media:.3f} ms")
    print("Tabela:", saida)


if __name__ == "__main__":
    main()
