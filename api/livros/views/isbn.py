from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.isbn import consultar_isbn
from ..models import Autor, Editora


class IsbnConsultaView(APIView):
    """
    GET ?isbn=9780140328721
    Consulta dados do livro na Open Library e garante que autores/editoras existam.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        isbn = (request.query_params.get("isbn") or "").strip()
        if not isbn:
            return Response(
                {"detail": "Informe o parâmetro isbn."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            resultado = consultar_isbn(isbn)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if resultado is None:
            return Response(
                {"detail": "Livro não encontrado na Open Library."},
                status=status.HTTP_404_NOT_FOUND,
            )

        autores_ids = []
        for nome in resultado.get("autores") or []:
            autor, _ = Autor.objects.get_or_create(nome=nome.strip())
            autores_ids.append(autor.id)

        editora_id = None
        editora_nome = resultado.get("editora")
        if editora_nome:
            editora, _ = Editora.objects.get_or_create(nome=editora_nome.strip())
            editora_id = editora.id

        payload = {
            "isbn": resultado["isbn"],
            "titulo": resultado.get("titulo"),
            "qtd_paginas": resultado.get("numero_paginas"),
            "ano_publicacao": resultado.get("ano_publicacao"),
            "autores_ids": autores_ids,
            "editora_id": editora_id,
            "autores_nomes": resultado.get("autores") or [],
            "editora_nome": editora_nome,
            "imagem_url": resultado.get("imagem_url"),
            "descricao": resultado.get("descricao"),
            "idioma": resultado.get("idioma"),
        }

        return Response(payload, status=status.HTTP_200_OK)

