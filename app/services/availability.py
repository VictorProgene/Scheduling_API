"""
availability.py - Regras de Negócio para Cálculo de Disponibilidade

Este arquivo da camada Service contém a regra de negócio para calcular horários disponíveis.
Responsabilidades:
1. Obter o expediente de trabalho do prestador (start_work_hour e end_work_hour).
2. Gerar slots de horários de hora em hora.
3. Filtrar e retornar apenas os slots que não conflitam com agendamentos já salvos no banco.
"""

from datetime import datetime, timedelta, date
from sqlmodel import Session, select
from app.models.appointment import Appointment
from app.models.provider import Provider


def get_available_slots(db: Session, provider_id: int, target_date: date):
    # 1. Busca o profissional para obter o horário de trabalho
    provider = db.exec(select(Provider).where(Provider.id == provider_id)).first()
    if not provider:
        return []

    # 2. Busca todos os agendamentos do profissional para a data informada
    appointments = db.exec(
        select(Appointment).where(
            Appointment.provider_id == provider_id,
            # Filtra onde a data do agendamento é a target_date
            # Usamos cast para comparar apenas a data (ignorando hora)
        )
    ).all()

    # 3. Define o início e fim do expediente
    start_dt = datetime.combine(target_date, datetime.min.time().replace(hour=provider.start_work_hour))
    end_dt = datetime.combine(target_date, datetime.min.time().replace(hour=provider.end_work_hour))

    slots = []
    current_time = start_dt

    # 4. Loop pelos horários (gerando slots de 1 hora)
    while current_time < end_dt:
        # Verifica se o horário atual coincide com algum agendamento existente
        is_busy = any(
            apt.start_time <= current_time < apt.end_time
            for apt in appointments
        )

        if not is_busy:
            slots.append(current_time)

        current_time += timedelta(hours=1)

    return slots