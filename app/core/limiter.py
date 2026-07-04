"""
limiter.py - Configuração Global de Controle de Taxa de Requisições (Rate Limiting)

Este arquivo define e expõe a instância global do Limiter.
Utiliza a função 'get_remote_address' para identificar e limitar requisições baseando-se no endereço IP do cliente.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
