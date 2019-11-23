from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from atracoes.models import Atracao
from core.models import PontoTuristico, DocIdentificacao
from atracoes.api.serializers import AtracaoSerializer
from enderecos.api.serializers import EnderecoSerializer
from enderecos.models import Endereco


class DocIdentificacaoSerializer(ModelSerializer):
    class Meta:
        model = DocIdentificacao
        fields = '__all__'


class PontoTuristicoSerializer(ModelSerializer):
    atracaoes = AtracaoSerializer(many=True)
    endereco = EnderecoSerializer()
    descricao_completa = SerializerMethodField()
    doc_identificacao = DocIdentificacaoSerializer()

    class Meta:
        model = PontoTuristico
        fields = ('id', 'nome', 'descricao', 'aprovado', 'foto',
                  'atracaoes', 'comentarios', 'avaliacoes', 'endereco',
                  'descricao_completa', 'descricao_completa2', 'doc_identificacao')

        read_only_fields = ('comentarios', 'avaliacoes')

    def cria_atracaoes(self, atracaoes, ponto):
        for atracao in atracaoes:
            at = Atracao.objects.create(**atracao)
            ponto.atracaoes.add(at)

    def create(self, validated_data):
        atracaoes = validated_data['atracaoes']
        del validated_data['atracaoes']

        endereco = validated_data['endereco']
        del validated_data['endereco']

        doc = validated_data['doc_identificacao']
        del validated_data['doc_identificacao']


        ponto = PontoTuristico.objects.create(**validated_data)
        self.cria_atracaoes(atracaoes, ponto)

        end = Endereco.objects.create(**endereco)
        ponto.endereco = end

        doc1 = DocIdentificacao.objects.create(**doc)
        ponto.doc_identificacao = doc1

        ponto.save()
        return ponto

    def get_descricao_completa(self, obj):
        return '%s - %s' % (obj.nome, obj.descricao)
