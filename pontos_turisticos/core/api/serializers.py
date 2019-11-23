from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from atracoes.models import Atracao
from core.models import PontoTuristico
from atracoes.api.serializers import AtracaoSerializer
from enderecos.api.serializers import EnderecoSerializer


class PontoTuristicoSerializer(ModelSerializer):
    atracaoes = AtracaoSerializer(many=True)
    endereco = EnderecoSerializer(read_only=True)
    descricao_completa = SerializerMethodField()

    class Meta:
        model = PontoTuristico
        fields = ('id', 'nome', 'descricao', 'aprovado', 'foto',
                  'atracaoes', 'comentarios', 'avaliacoes', 'endereco', 'descricao_completa', 'descricao_completa2')

        read_only_fields = ('comentarios', 'avaliacoes')

    def cria_atracaoes(self, atracaoes, ponto):
        for atracao in atracaoes:
            at = Atracao.objects.create(**atracao)
            ponto.atracaoes.add(at)

    def create(self, validated_data):
        atracaoes = validated_data['atracaoes']
        del validated_data['atracaoes']
        ponto = PontoTuristico.objects.create(**validated_data)
        self.cria_atracaoes(atracaoes, ponto)
        return ponto

    def get_descricao_completa(self, obj):
        return '%s - %s' % (obj.nome, obj.descricao)
