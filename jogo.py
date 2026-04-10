import os
import time

def run(cmd):
    print(f"\n>>> {cmd}")
    os.system(cmd)

print("=== SETUP INICIAL: SIMULAÇÃO DE JOGO ONLINE ===")

# 1. Limpar ambiente
run("sudo mn -c")

# 2. Criar script de comandos para o Mininet
mininet_commands = """
echo "=== INICIANDO SERVIDOR (h2) ==="
h2 iperf -s -u -i 1 &

sleep 2

echo "=== INICIANDO CLIENTE (h1) ==="
h1 iperf -c 10.0.0.2 -u -b 1M -t 15 &

sleep 2

echo "=== COLETANDO LATÊNCIA NORMAL ==="
h1 ping -c 5 10.0.0.2

echo "=== APLICANDO CONDIÇÕES DE LAG ==="
h1 tc qdisc add dev h1-eth0 root netem delay 120ms 40ms loss 5%

sleep 2

echo "=== COLETANDO LATÊNCIA COM LAG ==="
h1 ping -c 5 10.0.0.2

echo "=== TESTE FINALIZADO ==="
"""

# 3. Salvar comandos em arquivo
with open("mn_commands.txt", "w") as f:
    f.write(mininet_commands)

# 4. Executar Mininet com topologia simples
run("sudo mn --topo single,2 --link tc --controller=none < mn_commands.txt")

print("\n=== DEMONSTRAÇÃO CONCLUÍDA ===")
