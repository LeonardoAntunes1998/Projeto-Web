import requests
from django.utils.timesince import timesince  # <--- NOVA IMPORTAÇÃO AQUI

# Cole sua URL do N8N aqui
WEBHOOK_N8N = "https://n8n.dssnet.com.br/webhook/nova-encomenda"

def enviar_notificacao_n8n(encomenda, tipo):
    """
    Função central para enviar dados ao N8N.
    Tipos aceitos: 'chegada', 'saida', 'lembrete'
    """
    morador = encomenda.morador
    telefone = getattr(morador, 'telefone', None) or getattr(morador, 'celular', None)
    codigo = getattr(encomenda, 'codigo_retirada', 'N/A')

    # Define a mensagem baseada no tipo
    if tipo == "chegada":
        mensagem = (
            f"Olá *{morador}*! 👋\n"
            f"📦 Chegou uma encomenda para você!\n\n"
            f"🔐 *Código:* {codigo}\n\n"
            f"Apresente este código na portaria para retirar."
        )
    
    elif tipo == "saida":
        mensagem = (
            f"✅ *Confirmação de Retirada*\n\n"
            f"Olá *{morador}*, confirmamos que sua encomenda (Cód: {codigo}) foi retirada agora pouco.\n\n"
            f"Se não foi você, por favor, entre em contato com a administração!."
        )
    
    elif tipo == "lembrete":
        # --- A MÁGICA ACONTECE AQUI ---
        # Calcula o tempo (ex: "2 dias, 4 horas")
        tempo_parado = timesince(encomenda.data_entrada)
        
        mensagem = (
            f"⏳ *Lembrete de Encomenda*\n\n"
            f"Olá {morador}, sua encomenda (Cód: {codigo}) já está aguardando retirada há *{tempo_parado}*.\n\n"
            f"Por favor, venha buscar assim que possível para liberar espaço na portaria! 😉"
        )
    elif tipo == "reenvio_codigo":
        mensagem = (
            f"🔑 *Reenvio de Código*\n\n"
            f"Olá {morador}, aqui está o código da sua encomenda (ID: {encomenda.id}) novamente:\n\n"
            f"👉 *{codigo}*\n\n"
            f"Apresente este código na portaria para retirar."
        )
    
    else:
        mensagem = "Atualização sobre sua encomenda."

    # Monta o pacote
    dados = {
        "tipo_evento": tipo,
        "encomenda_id": encomenda.id,
        "codigo": codigo,
        "morador_nome": str(morador),
        "morador_telefone": str(telefone) if telefone else "Sem telefone",
        "mensagem_sugerida": mensagem
    }

    # Envia
    try:
        if telefone:
            requests.post(WEBHOOK_N8N, json=dados)
            print(f"✅ Enviado para N8N ({tipo}) com sucesso!")
            return True
        else:
            print(f"⚠️ Sem telefone para {morador}")
            return False
    except Exception as e:
        print(f"❌ Erro conexão N8N: {e}")
        return False