from django.test import TestCase
from django.contrib.auth import get_user_model
from usuarios.models import Morador
from encomendas.models import Encomenda
from blocos.models import Bloco, Apartamento, Torre

User = get_user_model()

class EncomendaModelTest(TestCase):
    
    def setUp(self):
        """
        Configuração do cenário de testes.
        """
        # 1. Criar Porteiro
        self.porteiro = User.objects.create_user(
            username='porteiro_teste',
            password='123'
        )

        # 2. Criar Estrutura (Bloco -> Torre -> Apto)
        bloco = Bloco.objects.create(nome='A')
        torre = Torre.objects.create(nome='Torre 1', bloco=bloco)
        
        # Guardamos o apartamento numa variável para usar depois
        self.apto = Apartamento.objects.create(numero='101', torre=torre)

        # 3. Criar Morador (AQUI ESTAVA O ERRO)
        self.morador = Morador.objects.create(
            nome='João Teste',
            telefone='(11) 99999-9999',  # Se der erro aqui, troque por 'celular'
            apto=self.apto               # <--- O NOME CORRETO É 'apto'
        )

    def test_criar_encomenda_com_sucesso(self):
        """Teste 1: Verifica se conseguimos salvar uma encomenda"""
        encomenda = Encomenda.objects.create(
            morador=self.morador,
            funcionario_registro=self.porteiro,
            codigo_encomenda='BR123456',
            descricao='Caixa de Sapato'
        )
        
        self.assertIsNotNone(encomenda.id)
        self.assertEqual(encomenda.status, 'PENDENTE')
        print("\n✅ Teste 1: Encomenda criada com sucesso!")

    def test_geracao_automatica_codigo_retirada(self):
        """Teste 2: Verifica o código automático"""
        encomenda = Encomenda.objects.create(
            morador=self.morador,
            funcionario_registro=self.porteiro,
            codigo_encomenda='XYZ987'
        )
        
        self.assertTrue(encomenda.codigo_retirada)
        self.assertEqual(len(encomenda.codigo_retirada), 6)
        print(f"\n✅ Teste 2: Código gerado: {encomenda.codigo_retirada}")