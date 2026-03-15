"""
Serviço de consulta de livro por ISBN usando a API Open Library.
Documentação: https://openlibrary.org/dev/docs/api/books
"""

import json
import re
import urllib.error
import urllib.request

OPENLIBRARY_URL = "https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
OPENLIBRARY_BASE = "https://openlibrary.org"

# Mapa de códigos de idioma (Open Library) para nome em português
IDIOMA_CODIGO_PARA_NOME = {
    "por": "Português",
    "pt": "Português",
    "pt-br": "Português (Brasil)",
    "eng": "Inglês",
    "en": "Inglês",
    "spa": "Espanhol",
    "es": "Espanhol",
    "fra": "Francês",
    "fr": "Francês",
    "deu": "Alemão",
    "de": "Alemão",
    "ita": "Italiano",
    "it": "Italiano",
    "jpn": "Japonês",
    "ja": "Japonês",
    "rus": "Russo",
    "ru": "Russo",
    "chi": "Chinês",
    "zh": "Chinês",
    "ara": "Árabe",
    "ar": "Árabe",
}


def _normalizar_isbn(isbn: str) -> str:
    """Remove caracteres não numéricos e retorna string com no máximo 13 dígitos."""
    if isbn is None:
        return ""
    digits = re.sub(r"\D", "", str(isbn).strip())
    return digits[:13] if digits else ""


def _idioma_key_para_nome(key: str) -> str | None:
    """Converte chave /languages/por em nome em português."""
    if not key or not isinstance(key, str):
        return None
    key = key.strip().lower()
    if key.startswith("/languages/"):
        cod = key.replace("/languages/", "").strip()
    else:
        cod = key
    return IDIOMA_CODIGO_PARA_NOME.get(cod) or IDIOMA_CODIGO_PARA_NOME.get(cod[:3]) or cod.upper()


def _extrair_descricao(desc):
    """Extrai texto de description (pode ser string ou dict com 'value')."""
    if desc is None:
        return None
    if isinstance(desc, str):
        return desc.strip() or None
    if isinstance(desc, dict):
        v = desc.get("value")
        if isinstance(v, str):
            return v.strip() or None
    return None


def _buscar_edicao(edition_key: str) -> dict | None:
    """Busca JSON da edição para obter descrição e idiomas."""
    if not edition_key or not edition_key.startswith("/"):
        return None
    url = OPENLIBRARY_BASE + edition_key.rstrip("/") + ".json"
    req = urllib.request.Request(url, headers={"User-Agent": "BibliotecaQuintal/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
        return None


def consultar_isbn(isbn: str) -> dict | None:
    """
    Consulta dados de um livro na Open Library pelo ISBN.
    Inclui descrição, idioma e categorias (subjects) quando disponíveis.
    """
    isbn_limpo = _normalizar_isbn(isbn)
    if not isbn_limpo:
        raise ValueError("Informe um ISBN válido.")
    if len(isbn_limpo) < 10:
        raise ValueError("ISBN deve conter pelo menos 10 dígitos.")

    url = OPENLIBRARY_URL.format(isbn=isbn_limpo)
    req = urllib.request.Request(url, headers={"User-Agent": "BibliotecaQuintal/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError:
        raise ValueError("Não foi possível consultar o ISBN. Tente novamente.")

    key = f"ISBN:{isbn_limpo}"
    livro = data.get(key)
    if not livro:
        return None

    titulo = (livro.get("title") or "").strip()
    numero_paginas = livro.get("number_of_pages")
    publish_date = (livro.get("publish_date") or "").strip()

    ano_publicacao = None
    if publish_date:
        match = re.search(r"(19|20)\d{2}", publish_date)
        if match:
            ano_publicacao = int(match.group(0))

    autores_nomes = []
    for autor in livro.get("authors") or []:
        nome = (autor.get("name") or "").strip()
        if nome:
            autores_nomes.append(nome)

    editora_nome = None
    publishers = livro.get("publishers") or []
    if publishers:
        first = publishers[0]
        if isinstance(first, dict):
            editora_nome = (first.get("name") or "").strip()
        else:
            editora_nome = str(first).strip()

    # Capa: large → medium → small
    cover = livro.get("cover") or {}
    imagem_url = (
        (cover.get("large") or "").strip()
        or (cover.get("medium") or "").strip()
        or (cover.get("small") or "").strip()
    ) or None

    # Categorias (subjects) da resposta principal — nomes como estão na API
    categorias_nomes = []
    for s in livro.get("subjects") or []:
        if isinstance(s, dict):
            nome = (s.get("name") or "").strip()
        else:
            nome = (str(s) or "").strip()
        if nome:
            categorias_nomes.append(nome)

    # Descrição e idioma: buscar edição quando houver key
    descricao = None
    idioma_nome = None
    edition_key = livro.get("key")
    if edition_key:
        ed = _buscar_edicao(edition_key)
        if ed:
            descricao = _extrair_descricao(ed.get("description"))
            if not descricao and ed.get("works"):
                work_key = (ed["works"][0].get("key") or "").strip()
                if work_key:
                    work_url = OPENLIBRARY_BASE + work_key.rstrip("/") + ".json"
                    try:
                        req_w = urllib.request.Request(
                            work_url, headers={"User-Agent": "BibliotecaQuintal/1.0"}
                        )
                        with urllib.request.urlopen(req_w, timeout=8) as rw:
                            work = json.loads(rw.read().decode("utf-8"))
                            descricao = _extrair_descricao(work.get("description"))
                    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
                        pass
            langs = ed.get("languages") or []
            if langs and isinstance(langs[0], dict):
                lang_key = (langs[0].get("key") or "").strip()
                idioma_nome = _idioma_key_para_nome(lang_key)
            elif langs:
                idioma_nome = _idioma_key_para_nome(str(langs[0]))

    return {
        "isbn": isbn_limpo,
        "titulo": titulo or None,
        "numero_paginas": numero_paginas,
        "ano_publicacao": ano_publicacao,
        "autores": autores_nomes,
        "editora": editora_nome,
        "imagem_url": imagem_url,
        "descricao": descricao,
        "idioma": idioma_nome,
        "categorias": categorias_nomes,
    }

