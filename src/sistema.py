"""Citizen Assist AI: consulta local, interface gráfica e modo terminal.

Uso: python src/sistema.py [--terminal] [--base caminho.json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

BASE_PADRAO = Path(__file__).resolve().parents[1] / "data" / "base.json"
CAMPOS_TEXTO = ("id", "tema", "subtema", "pergunta", "orientacao", "fonte", "referencia", "data_verificacao")
IGNORAR = {"a", "as", "o", "os", "de", "da", "do", "das", "dos", "e", "em", "na", "no", "para", "por", "um", "uma", "que", "como", "qual", "quais", "posso", "me", "eu", "minha", "meu", "quero", "preciso", "fazer", "tirar", "obter", "pedir", "onde"}


class ErroBase(ValueError):
    """Base ausente ou inconsistente, com mensagem compreensível ao usuário."""


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto.casefold())
    texto = "".join(letra for letra in texto if not unicodedata.combining(letra))
    return " ".join(re.findall(r"[a-z0-9]+", texto))


def termos(texto: str) -> set[str]:
    return set(normalizar(texto).split()) - IGNORAR


def carregar_base(caminho: str | Path = BASE_PADRAO) -> dict:
    arquivo = Path(caminho)
    try:
        conteudo = arquivo.read_text(encoding="utf-8-sig")
    except FileNotFoundError as erro:
        raise ErroBase(f"Base não encontrada: {arquivo}") from erro
    except (OSError, UnicodeError) as erro:
        raise ErroBase(f"Não foi possível ler a base: {erro}") from erro
    if not conteudo.strip():
        raise ErroBase("A base de conhecimento está vazia.")
    try:
        base = json.loads(conteudo)
    except json.JSONDecodeError as erro:
        raise ErroBase(f"JSON inválido na base (linha {erro.lineno}).") from erro
    if not isinstance(base, dict):
        raise ErroBase("A raiz da base deve ser um objeto JSON.")
    temas, registros = base.get("temas"), base.get("registros")
    if not isinstance(temas, dict) or not temas:
        raise ErroBase("A base precisa conter um objeto 'temas' não vazio.")
    if not isinstance(registros, list) or not registros:
        raise ErroBase("A base precisa conter uma lista 'registros' não vazia.")
    for chave, info in temas.items():
        if not isinstance(info, dict) or not isinstance(info.get("nome"), str):
            raise ErroBase(f"Tema inconsistente: {chave}.")
        subtemas = info.get("subtemas")
        if not isinstance(subtemas, dict) or not all(isinstance(nome, str) for nome in subtemas.values()):
            raise ErroBase(f"Confira os subtemas de {chave}.")
    if not isinstance(base.get("aviso_geral", ""), str):
        raise ErroBase("O aviso geral precisa ser um texto.")
    ids = set()
    for numero, registro in enumerate(registros, 1):
        if not isinstance(registro, dict):
            raise ErroBase(f"Registro {numero} deve ser um objeto JSON.")
        if not isinstance(registro.get("observacao", ""), str):
            raise ErroBase(f"Registro {numero}: observação inválida.")
        for campo in CAMPOS_TEXTO:
            if not isinstance(registro.get(campo), str) or not registro[campo].strip():
                raise ErroBase(f"Registro {numero}: campo '{campo}' ausente ou vazio.")
        rid = registro["id"]
        if rid in ids:
            raise ErroBase(f"ID duplicado: {rid}.")
        ids.add(rid)
        tema = registro["tema"]
        if tema not in temas or registro["subtema"] not in temas[tema]["subtemas"]:
            raise ErroBase(f"{rid}: tema ou subtema não existe na hierarquia.")
        for campo in ("palavras_chave", "relacionados"):
            lista = registro.get(campo)
            if not isinstance(lista, list) or not all(isinstance(item, str) and item.strip() for item in lista):
                raise ErroBase(f"{rid}: confira a lista de {campo}.")
        if not registro["palavras_chave"]:
            raise ErroBase(f"{rid}: faltam palavras-chave.")
        if not isinstance(registro.get("requer_confirmacao"), bool):
            raise ErroBase(f"{rid}: requer_confirmacao deve ser verdadeiro ou falso.")
        if not registro["referencia"].startswith(("https://", "http://")):
            raise ErroBase(f"{rid}: referência deve ser um link HTTP(S).")
        try:
            date.fromisoformat(registro["data_verificacao"])
        except ValueError as erro:
            raise ErroBase(f"{rid}: data_verificacao inválida.") from erro
    for registro in registros:
        for relacionado in registro["relacionados"]:
            if relacionado not in ids or relacionado == registro["id"]:
                raise ErroBase(f"{registro['id']}: relação inválida com {relacionado}.")
    return base


@dataclass(frozen=True)
class Resultado:
    status: str  # encontrado, ambiguo, sem_resposta, vazia
    ids: tuple[str, ...] = ()


class Sistema:
    def __init__(self, base: dict):
        self.base = base
        self.registros = base["registros"]
        self.por_id = {r["id"]: r for r in self.registros}
        self.por_tema = defaultdict(list)
        self.por_subtema = defaultdict(list)
        self.por_palavra = defaultdict(set)
        for registro in self.registros:
            rid = registro["id"]
            self.por_tema[registro["tema"]].append(rid)
            self.por_subtema[(registro["tema"], registro["subtema"])].append(rid)
            for palavra in registro["palavras_chave"]:
                for termo in termos(palavra):
                    self.por_palavra[termo].add(rid)

    def buscar(self, pergunta: str) -> Resultado:
        consulta = normalizar(pergunta)
        tokens = termos(pergunta)
        if not pergunta.strip():
            return Resultado("vazia")
        if not tokens:
            return Resultado("sem_resposta")

        apelidos = {"documento": "documentacao", "documentos": "documentacao",
                    "direito": "direitos", "servico": "servicos"}
        for chave, tema in self.base["temas"].items():
            if consulta in (normalizar(chave), normalizar(tema["nome"])) or apelidos.get(consulta) == chave:
                return Resultado("ambiguo", tuple(self.por_tema[chave]))

        candidatos = set()
        for termo in tokens:
            candidatos.update(self.por_palavra.get(termo, []))

        pontuacoes = []
        for rid in candidatos:
            registro = self.por_id[rid]
            chaves = set()
            bonus = 0
            for palavra in registro["palavras_chave"]:
                chaves.update(termos(palavra))
                if f" {normalizar(palavra)} " in f" {consulta} ":
                    bonus = max(bonus, 2 + len(termos(palavra)))

            titulo = termos(registro["pergunta"])
            acoes = tokens & {"cancelar", "bloquear", "desbloquear", "renovar", "alterar", "corrigir"}
            if acoes - (chaves | titulo):
                continue
            conhecidos = tokens & (chaves | titulo)
            # Uma sigla sozinha no meio de outra pergunta pode levar à resposta errada.
            if len(conhecidos) * 2 < len(tokens):
                continue
            pontos = len(tokens & chaves) + len(tokens & titulo) + bonus
            pontuacoes.append((pontos, rid))
        if not pontuacoes:
            return Resultado("sem_resposta")
        pontuacoes.sort(key=lambda item: (-item[0], item[1]))
        primeiro = pontuacoes[0][0]
        # Exige evidência mínima; um termo genérico isolado costuma ser ambíguo.
        selecionados = [rid for score, rid in pontuacoes if score >= max(2, primeiro - 1)]
        if not selecionados:
            return Resultado("sem_resposta")
        if len(selecionados) > 1:
            return Resultado("ambiguo", tuple(selecionados[:5]))
        return Resultado("encontrado", (selecionados[0],))

    def trechos(self, rid, modelo):
        registro = self.por_id[rid]
        texto = registro["orientacao"]
        if modelo.upper() == "A":
            return [texto]
        # A letra maiúscula depois do ponto evita cortar domínios como gov.br.
        partes = re.split(r"(?<=[.!?]) +(?=[A-ZÀ-Ý])", texto)
        if registro.get("observacao"):
            partes.append("Observação: " + registro["observacao"])
        return partes

    def resposta(self, rid: str, modelo: str = "B") -> str:
        r = self.por_id[rid]
        linhas = [r["pergunta"], "", "\n\n".join(self.trechos(rid, modelo))]
        linhas.extend(["", f"Fonte: {r['fonte']}", f"Referência: {r['referencia']}", f"Verificada em: {r['data_verificacao']}"])
        if r["requer_confirmacao"]:
            linhas.extend(["", "Confirme as regras atuais na fonte indicada antes de agir."])
        linhas.extend(["", self.base.get("aviso_geral", "Conteúdo informativo; não é canal oficial.")])
        return "\n".join(linhas)


def executar_terminal(sistema: Sistema) -> None:
    modelo = "B"
    while True:
        print("\nCITIZEN ASSIST AI | 1 Temas | 2 Perguntar | 3 Modelo A/B | 0 Sair")
        opcao = input("Escolha: ").strip()
        if opcao == "0":
            return
        if opcao == "3":
            modelo = "A" if modelo == "B" else "B"
            print(f"Modelo {modelo} selecionado.")
            continue
        if opcao == "1":
            for i, (chave, info) in enumerate(sistema.base["temas"].items(), 1):
                print(f"{i}. {info['nome']}")
            escolha = input("Número do tema: ").strip()
            chaves = list(sistema.base["temas"])
            if escolha not in [str(i) for i in range(1, len(chaves) + 1)]:
                print("Opção inválida.")
                continue
            ids = sistema.por_tema[chaves[int(escolha) - 1]]
        elif opcao == "2":
            resultado = sistema.buscar(input("Pergunta: "))
            if resultado.status == "vazia":
                print("Digite uma pergunta para consultar.")
                continue
            if resultado.status == "sem_resposta":
                print("Não há informação suficiente na base. Escolha um tema no menu ou consulte a fonte oficial.")
                continue
            ids = list(resultado.ids)
        else:
            print("Opção inválida.")
            continue
        while ids:
            for i, rid in enumerate(ids, 1):
                print(f"{i}. {sistema.por_id[rid]['pergunta']}")
            escolha = input("Número do assunto (Enter para voltar): ").strip()
            if not escolha:
                break
            if escolha not in [str(i) for i in range(1, len(ids) + 1)]:
                print("Opção inválida.")
                continue
            rid = ids[int(escolha) - 1]
            print("\n" + sistema.resposta(rid, modelo))
            ids = [r for r in sistema.por_id[rid]["relacionados"] if r in sistema.por_id]
            if ids:
                print("\nAssuntos relacionados:")


def main() -> int:
    parser = argparse.ArgumentParser(description="Citizen Assist AI")
    parser.add_argument("--terminal", action="store_true", help="Usar interface textual")
    parser.add_argument("--base", type=Path, default=BASE_PADRAO, help="Caminho do JSON da base")
    args = parser.parse_args()
    try:
        sistema = Sistema(carregar_base(args.base))
    except ErroBase as erro:
        print(f"Erro na base: {erro}", file=sys.stderr)
        return 1
    if args.terminal:
        executar_terminal(sistema)
    else:
        from interface import executar_interface
        executar_interface(sistema)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
