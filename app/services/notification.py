from datetime import datetime

def send_appointment_email(email_to: str, provider_name: str, start_time: datetime):
    # Simula o envio de e-mail escrevendo no console/log.
    # Em produção, usaríamos smtplib ou uma biblioteca como fastapi-mail.
    print(f"\n==================================================")
    print(f"📧 ENVIANDO E-MAIL DE CONFIRMAÇÃO")
    print(f"Para: {email_to}")
    print(f"Assunto: Agendamento Confirmado!")
    print(f"Mensagem: Olá! Seu agendamento com {provider_name} "
          f"para o dia {start_time.strftime('%d/%m/%Y às %H:%M')} foi confirmado.")
    print(f"==================================================\n")
