"""Valida a base de conhecimento (data/base.json) do Citizen Assist AI.

Uso: python scripts/validar_base.py [caminho_da_base]

Confere:
- se o arquivo existe, não está vazio e é um JSON válido;
- se todo registro tem os campos obrigatórios preenchidos;
- se ids são únicos e se tema/subtema existem na hierarquia;
- se a referência é um link (http/https) e a data está no formato AAAA-MM-DD;
- se os ids em "relacionados" existem (grafo sem links quebrados);
- os mínimos do enunciado: 15 registros e 3 temas.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

CAMPOS_OBRIGATORIOS = [
    "id", "tema", "subtema", "pergunta", "palavras_chave",
    "orientacao", "fonte", "referencia", "data_verificacao",
    "requer_confirmacao", "relacionados",
]


def validar(caminho):
    erros, avisos = [], []
    arquivo = Path(caminho)

    if not arquivo.exists():
        return [f"Arquivo não encontrado: {caminho}"], avisos
    if arquivo.stat().st_size == 0:
        return ["Arquivo vazio."], avisos
    try:
        base = json.loads(arquivo.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"JSON inválido: {e}"], avisos

    temas = base.get("temas", {})
    registros = base.get("registros", [])
    if not isinstance(registros, list) or not registros:
        return ["A chave 'registros' está ausente ou vazia."], avisos

    ids = [r.get("id") for r in registros]
    ids_existentes = set(ids)

    for r in registros:
        rid = r.get("id", "<sem id>")
        for campo in CAMPOS_OBRIGATORIOS:
            if campo not in r:
                erros.append(f"{rid}: campo obrigatório ausente '{campo}'")
            elif campo not in ("requer_confirmacao", "relacionados") and r[campo] in ("", [], None):
                erros.append(f"{rid}: campo '{campo}' vazio")

        tema = r.get("tema")
        if tema not in temas:
            erros.append(f"{rid}: tema '{tema}' não existe em 'temas'")
        elif r.get("subtema") not in temas[tema].get("subtemas", {}):
            erros.append(f"{rid}: subtema '{r.get('subtema')}' não existe no tema '{tema}'")

        if not str(r.get("referencia", "")).startswith(("http://", "https://")):
            erros.append(f"{rid}: referência deve ser um link http(s)")

        try:
            datetime.strptime(str(r.get("data_verificacao")), "%Y-%m-%d")
        except ValueError:
            erros.append(f"{rid}: data_verificacao fora do formato AAAA-MM-DD")

        if not isinstance(r.get("requer_confirmacao"), bool):
            erros.append(f"{rid}: requer_confirmacao deve ser true ou false")

        for rel in r.get("relacionados", []):
            if rel not in ids_existentes:
                erros.append(f"{rid}: relacionado '{rel}' não existe na base")
            if rel == rid:
                erros.append(f"{rid}: registro relacionado a si mesmo")

        if len(r.get("palavras_chave", [])) < 3:
            avisos.append(f"{rid}: poucas palavras-chave (recomendado 3 ou mais)")

    duplicados = {i for i in ids if ids.count(i) > 1}
    for d in duplicados:
        erros.append(f"id duplicado: {d}")

    if len(registros) < 15:
        erros.append(f"Mínimo de 15 registros não atingido ({len(registros)})")
    temas_usados = {r.get("tema") for r in registros}
    if len(temas_usados) < 3:
        erros.append(f"Mínimo de 3 temas não atingido ({len(temas_usados)})")

    return erros, avisos


def main():
    caminho = sys.argv[1] if len(sys.argv) > 1 else "data/base.json"
    erros, avisos = validar(caminho)

    if not erros:
        base = json.loads(Path(caminho).read_text(encoding="utf-8"))
        regs = base["registros"]
        print(f"OK: {len(regs)} registros válidos.")
        for tema, info in base["temas"].items():
            qtd = sum(1 for r in regs if r["tema"] == tema)
            print(f"  - {info['nome']}: {qtd} registros")
        ligacoes = sum(len(r["relacionados"]) for r in regs)
        print(f"  - Ligações entre assuntos (arestas do grafo): {ligacoes}")
    for a in avisos:
        print(f"AVISO: {a}")
    for e in erros:
        print(f"ERRO: {e}")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
