# test_praiometro.py

import pytest
import sys
import os
import re
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from praiometro import get_visitor_ip  #

@patch('urllib.request.urlopen')
def test_get_visitor_ip(mock_urlopen):
    
    # Chama a função
    ip = get_visitor_ip()
    #ip = "390.10.1.5"
    
    # Verifica se o IP está no formato correto
    assert re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip), f"IP '{ip}' está em formato inválido"
    
    # Verifica se cada octeto do IP está no intervalo válido (0-255)
    octets = ip.split('.')
    for octet in octets:
        assert 0 <= int(octet) <= 255, f"Octeto '{octet}' está fora do intervalo válido (0-255)"
