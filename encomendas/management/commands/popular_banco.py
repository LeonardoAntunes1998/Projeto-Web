from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

# Imports para Permissões e Grupos
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Imports dos seus Models
from blocos.models import Bloco, Apartamento, Torre
from usuarios.models import Morador # Removemos Funcionario daqui pois ele é o User
from encomendas.models import Encomenda, Transportadora

class Command(BaseCommand):
    help = 'Popula o banco com dados reais, datas retroativas e usuários configurados'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')
        # Aqui pegamos o seu modelo de usuário (que é o Funcionario)
        FuncionarioUser = get_user_model()

        self.stdout.write("🧹 Limpando dados antigos...")
        Encomenda.objects.all().delete()
        Transportadora.objects.all().delete()
        
        self.stdout.write("🔨 Iniciando a fábrica de dados...")

        # --- 1. CONFIGURAÇÃO DE USUÁRIOS E PERMISSÕES ---
        self.stdout.write("🔑 Configurando acessos...")

        # A. Criar Grupo de Porteiros
        grupo_porteiros, _ = Group.objects.get_or_create(name='Porteiros')
        
        # B. Definir Permissões
        ct_encomenda = ContentType.objects.get_for_model(Encomenda)
        permissoes = Permission.objects.filter(
            content_type=ct_encomenda,
            codename__in=['view_encomenda', 'add_encomenda', 'change_encomenda']
        )
        grupo_porteiros.permissions.set(permissoes)

        # C. Criar Super Usuário (Admin)
        if not FuncionarioUser.objects.filter(username='admin').exists():
            FuncionarioUser.objects.create_superuser('admin', 'admin@gobox.com', 'admin123')
            self.stdout.write("   👤 Admin criado: user 'admin' / senha 'admin123'")

        # D. Criar Usuário Porteiro (Que já é um funcionário)
        if not FuncionarioUser.objects.filter(username='porteiro').exists():
            u_porteiro = FuncionarioUser.objects.create_user('porteiro', 'porteiro@gobox.com', 'porteiro123')
            u_porteiro.is_staff = True 
            u_porteiro.groups.add(grupo_porteiros)
            
            # Se o seu model Funcionario tiver campos obrigatórios extras (ex: cargo), adicione aqui:
            # u_porteiro.cargo = 'Porteiro' 
            
            u_porteiro.save()
            self.stdout.write("   👤 Porteiro criado: user 'porteiro' / senha 'porteiro123'")
        
        # Define quem será o responsável pelos registros (usamos o objeto do porteiro direto)
        funcionario_registro = FuncionarioUser.objects.get(username='porteiro')

        # --- 2. Criar Transportadoras ---
        transp_nomes = ['Correios', 'Sedex', 'Loggi', 'Jadlog', 'Amazon Logistics', 'Mercado Livre']
        transp_objs = []
        for nome in transp_nomes:
            t, _ = Transportadora.objects.get_or_create(nome=nome)
            transp_objs.append(t)
        self.stdout.write(f"🚚 {len(transp_objs)} Transportadoras criadas.")

        # --- 3. Estrutura (Blocos > Torres > Aptos) ---
        self.stdout.write("🏗️ Verificando estrutura...")
        blocos_letras = ['A', 'B']
        aptos_lista = []
        
        for letra in blocos_letras:
            bloco, _ = Bloco.objects.get_or_create(nome=letra)
            for i in range(1, 3): 
                torre, _ = Torre.objects.get_or_create(nome=f"Torre {i}", bloco=bloco)
                for andar in range(1, 5):
                    for final in range(1, 5):
                        num = f"{andar}0{final}"
                        apto, _ = Apartamento.objects.get_or_create(numero=num, torre=torre)
                        aptos_lista.append(apto)

        # --- 4. Moradores ---
        if Morador.objects.count() < 10:
            self.stdout.write("👥 Criando Moradores...")
            campos_morador = [f.name for f in Morador._meta.get_fields()]
            campo_tel = 'telefone' if 'telefone' in campos_morador else 'celular'

            for _ in range(20):
                nome = fake.name()
                tel = f"({random.randint(11, 99)}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
                apto_random = random.choice(aptos_lista)
                
                try:
                    dados = {'nome': nome, campo_tel: tel}
                    morador = Morador.objects.create(**dados)
                    
                    if hasattr(apto_random, 'moradores'):
                        apto_random.moradores.add(morador)
                    elif hasattr(morador, 'apartamento'):
                        morador.apartamento = apto_random
                        morador.save()
                    elif hasattr(morador, 'apto'):
                        morador.apto = apto_random
                        morador.save()
                except Exception:
                    pass

        # --- 5. ENCOMENDAS ---
        self.stdout.write("📦 Gerando histórico de Encomendas...")
        moradores = Morador.objects.all()
        
        if moradores.exists():
            qtd_encomendas = 40
            for i in range(qtd_encomendas):
                morador = random.choice(moradores)
                transportadora = random.choice(transp_objs)
                status = 'RETIRADA' if random.random() > 0.3 else 'PENDENTE'
                
                dias_atras = random.randint(0, 30)
                hora_aleatoria = random.randint(8, 20) 
                data_entrada_fake = timezone.now() - timedelta(days=dias_atras, hours=hora_aleatoria)
                
                codigo_rastreio = fake.bothify(text='??#########BR').upper()

                encomenda = Encomenda.objects.create(
                    morador=morador,
                    funcionario_registro=funcionario_registro, # Agora passa o User direto
                    transportadora=transportadora,
                    codigo_encomenda=codigo_rastreio,
                    status=status,
                    descricao=random.choice(['Caixa pequena', 'Envelope', 'Pacote grande', 'Caixa Amazon', 'Saco plástico']),
                )

                Encomenda.objects.filter(pk=encomenda.pk).update(data_entrada=data_entrada_fake)
                
                if status == 'RETIRADA':
                    tempo_espera = timedelta(hours=random.randint(2, 72))
                    data_saida_fake = data_entrada_fake + tempo_espera
                    if data_saida_fake > timezone.now():
                        data_saida_fake = timezone.now()
                    
                    Encomenda.objects.filter(pk=encomenda.pk).update(data_retirada=data_saida_fake)

            self.stdout.write(self.style.SUCCESS(f'🚀 SUCESSO!'))
        else:
            self.stdout.write("⚠️ Sem moradores para criar encomendas.")