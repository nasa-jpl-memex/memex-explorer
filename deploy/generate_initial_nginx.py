import sys
import os

from jinja2 import Template
from jinja2.runtime import Context


context = {
    'ip_addr': os.environ.get('IP_ADDR', ''),
    'hostname': os.environ.get('AWS_DOMAIN', ''),
    'root_port': os.environ.get('ROOT_PORT', '') 
    'containers': []
}
with open(sys.argv[1], 'r') as f:
    template_text = f.read()
    template = Template(template_text, trim_blocks = True, lstrip_blocks = True)
    nginx_config = template.render(**context)
    
with open(sys.argv[2], 'w') as f:
    f.write(nginx_config)
    f.flush() 
