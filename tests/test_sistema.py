"""Verificações dos fluxos demonstrados na Global Solution."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sistema import ErroBase, Sistema, carregar_base


class SistemaTestes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sistema = Sistema(carregar_base())

    def test_perguntas_direta_e_reformulada(self):
        self.assertEqual(self.sistema.buscar("Como tirar o título de eleitor?").ids, ("DOC04",))
        self.assertEqual(self.sistema.buscar("fui mandado embora, o que eu faço?").ids, ("SERV04",))

    def test_limites(self):
        self.assertEqual(self.sistema.buscar(" ").status, "vazia")
        self.assertEqual(self.sistema.buscar("qual a previsão do tempo amanhã?").status, "sem_resposta")
        amplo = self.sistema.buscar("documento")
        self.assertEqual(amplo.status, "ambiguo")
        self.assertGreaterEqual(len(amplo.ids), 2)

    def test_sugestoes_quando_nao_ha_resposta(self):
        pergunta = "Quero saber se meu patrão assinou minha carteira"
        self.assertEqual(self.sistema.buscar(pergunta).status, "sem_resposta")
        self.assertIn("DOC05", self.sistema.sugestoes(pergunta))
        self.assertEqual(self.sistema.sugestoes("qual a previsão do tempo amanhã?"), [])

    def test_respostas_mantem_fonte_data_e_aviso(self):
        for modelo in ("A", "B"):
            texto = self.sistema.resposta("DOC01", modelo)
            self.assertIn("Fonte:", texto)
            self.assertIn("Referência: https://", texto)
            self.assertIn("Verificada em: 2026-11-17", texto)
            self.assertIn("Confirme as regras atuais", texto)

    def test_navegacao_por_tres_assuntos(self):
        caminho = ("SERV04", "DOC05", "SERV01", "SERV02")
        for origem, destino in zip(caminho, caminho[1:]):
            self.assertIn(destino, self.sistema.por_id[origem]["relacionados"])

    def test_base_invalida_nao_quebra_interface(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "base.json"
            with self.assertRaises(ErroBase):
                carregar_base(arquivo)
            arquivo.write_text("", encoding="utf-8")
            with self.assertRaises(ErroBase):
                carregar_base(arquivo)
            arquivo.write_text("{", encoding="utf-8")
            with self.assertRaises(ErroBase):
                carregar_base(arquivo)
            arquivo.write_text(json.dumps({"temas": [], "registros": [5]}), encoding="utf-8")
            with self.assertRaises(ErroBase):
                carregar_base(arquivo)


if __name__ == "__main__":
    unittest.main()
