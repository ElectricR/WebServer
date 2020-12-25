import os
from dotenv import load_dotenv

INITIAL_PORT = 10050
REDIS_INITIAL_PORT = 6379

load_dotenv()

instance_count = int(os.getenv('INSTANCE_COUNT'))

with open('.env', 'w') as f:
    f.write(f'INSTANCE_COUNT={os.getenv("INSTANCE_COUNT")}\n')
    f.write(f'SERVER_VERSION={os.getenv("SERVER_VERSION")}\n')
    f.write(f'BALANCER_VERSION={os.getenv("BALANCER_VERSION")}\n')
    f.write('\n')
    f.write(f'BALANCER_PORT={INITIAL_PORT}\n')
    f.write(f'DATABASE_PORT={os.getenv("DATABASE_PORT")}\n')
    f.write('\n')
    for i in range(instance_count):
        f.write(f'SERVER{i + 1}_PORT={INITIAL_PORT + i + 1}\n')
        f.write(f'REDIS{i + 1}_PORT={REDIS_INITIAL_PORT + i}\n')
        f.write('\n')

COMPOSE_HEADER = '''version: "3.7"

services:
'''

COMPOSE_BALANCER_BASE = '''    balancer:
        image: electricrainbow/pm-balancer-server-image:${{BALANCER_VERSION}}
        ports:
          - ${{BALANCER_PORT}}:${{BALANCER_PORT}}
        depends_on:
{0}        networks:
          - pm-network
        environment:
          - PORT=${{BALANCER_PORT}}
          - INSTANCE_COUNT=${{INSTANCE_COUNT}}
'''

COMPOSE_SERVER_BASE = '''    server{0}:
        image: electricrainbow/pm-default-server-image:${{SERVER_VERSION}}
        container_name: pm-default-server-container-{0}
        networks:
          - pm-network
        depends_on:
          - redis{0}
          - mongo
        environment:
          - PORT=${{SERVER{0}_PORT}}
          - REDIS_PORT=${{REDIS{0}_PORT}}
          - REDIS_HOST=redis{0}
          - DATABASE_PORT=${{DATABASE_PORT}}
'''

COMPOSE_REDIS_BASE = '''    redis{0}:
        image: redis
        container_name: redis{0}
        command: --port {1}
        networks:
          - pm-network
'''

COMPOSE_FOOTER_BASE = '''    mongo:
        image: mongo
        container_name: mongo
        networks:
          - pm-network

networks:
    pm-network:'''

with open('compose.yaml', 'w') as f:
    f.write(COMPOSE_HEADER)
    balancer_format_string = ''
    for i in range(instance_count):
        balancer_format_string += f'          - server{i + 1}\n'
    f.write(COMPOSE_BALANCER_BASE.format(balancer_format_string))
    for i in range(instance_count):
        f.write(COMPOSE_SERVER_BASE.format(i + 1))
        f.write(COMPOSE_REDIS_BASE.format(i + 1, REDIS_INITIAL_PORT + i))
    f.write(COMPOSE_FOOTER_BASE)
