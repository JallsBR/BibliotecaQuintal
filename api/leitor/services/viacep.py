"""
Serviço de consulta de CEP via ViaCEP (https://viacep.com.br/).
Retorna endereço no formato usado pelo formulário de leitor.
"""
import re
import json
import urllib.request
import urllib.error

VIACEP_URL = "https://viacep.com.br/ws/{cep}/json/"


def _normalizar_cep(cep):
    """Remove caracteres não numéricos e retorna string com no máximo 8 dígitos."""
    if cep is None:
        return ""
    digits = re.sub(r"\D", "", str(cep).strip())
    return digits[:8] if digits else ""


def consultar_cep(cep):
    """
    Consulta o endereço pelo CEP no ViaCEP.

    :param cep: CEP (pode conter pontuação, ex: 01.001-000)
    :return: dict com chaves endereco, bairro, cidade, estado, cep_formatado
             ou None se CEP inválido/inexistente.
    :raises ValueError: se o formato do CEP for inválido (não 8 dígitos).
    """
    cep_limpo = _normalizar_cep(cep)
    if len(cep_limpo) != 8:
        raise ValueError("CEP deve conter exatamente 8 dígitos.")

    url = VIACEP_URL.format(cep=cep_limpo)
    req = urllib.request.Request(url, headers={"User-Agent": "BibliotecaQuintal/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 400:
            raise ValueError("Formato de CEP inválido.")
        raise
    except urllib.error.URLError:
        raise ValueError("Não foi possível consultar o CEP. Tente novamente.")

    if data.get("erro") is True:
        return None

    return {
        "endereco": (data.get("logradouro") or "").strip(),
        "complemento": (data.get("complemento") or "").strip(),
        "bairro": (data.get("bairro") or "").strip(),
        "cidade": (data.get("localidade") or "").strip(),
        "estado": (data.get("uf") or "").strip(),
        "cep_formatado": (data.get("cep") or cep_limpo).strip(),
    }
