from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.viacep import consultar_cep


class CepConsultaView(APIView):
    """
    GET ?cep=01001000
    Retorna endereço (logradouro, bairro, cidade, estado) do ViaCEP.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cep = request.query_params.get("cep", "").strip()
        if not cep:
            return Response(
                {"detail": "Informe o parâmetro cep."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            resultado = consultar_cep(cep)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if resultado is None:
            return Response(
                {"detail": "CEP não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(resultado, status=status.HTTP_200_OK)
