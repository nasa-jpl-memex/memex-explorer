import jinja2
import os

conda_env_location = os.environ["CONDA_ENV_PATH"]

p = jinja2.Template(
"""exports.config = {
  nodeName: "application_server",
  logStreams: {
    nutch: [
      "{{ conda_env_location }}/lib/nutch/logs/hadoop.log"
    ]
  },
  server: {
    host: '0.0.0.0',
    port: 28777
  }
}"""
)

f = open("harvester.conf", "w")
f.write(p.render(conda_env_location=conda_env_location))
f.close()
