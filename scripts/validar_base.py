import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from sistema import BASE_PADRAO, ErroBase, carregar_base


def conferir(base):
    erros, avisos = [], []
    registros = base["registros"]
    if len(registros) < 15:
        erros.append("O trabalho pede pelo menos 15 orientações.")
    if len({r["tema"] for r in registros}) < 3:
        erros.append("Distribua as orientações em pelo menos três temas.")
    for registro in registros:
        if len(registro["palavras_chave"]) < 3:
            avisos.append(f"{registro['id']} tem poucas palavras-chave.")
    return erros, avisos


def validar(caminho):
    try:
        return conferir(carregar_base(caminho))
    except ErroBase as erro:
        return [str(erro)], []


def main():
    caminho = sys.argv[1] if len(sys.argv) > 1 else BASE_PADRAO
    try:
        base = carregar_base(caminho)
    except ErroBase as erro:
        print("Erro:", erro)
        return 1
    erros, avisos = conferir(base)
    for mensagem in avisos + erros:
        print(mensagem)
    if erros:
        return 1
    registros = base["registros"]
    print(f"OK: {len(registros)} registros válidos.")
    for chave, tema in base["temas"].items():
        print(tema["nome"], sum(r["tema"] == chave for r in registros))
    print("Ligações entre assuntos:", sum(len(r["relacionados"]) for r in registros))
    return 0


if __name__ == "__main__":
    sys.exit(main())
