import jinja2
import os

conda_env_location = os.environ["CONDA_ENV_PATH"]
conda_env_name = os.environ["CONDA_DEFAULT_ENV"]

p = jinja2.Template(
"""exports.config = {
  nodeName: "application_server",
  logStreams: {
    nutch: [
      "{{ conda_env_location }}/envs/{{ conda_env_name }}/lib/nutch/logs/hadoop.log"
    ]
  },
  server: {
    host: '0.0.0.0',
    port: 28777
  }
}"""
)

f = open(os.path.join(os.environ["HOME"], ".log.io", "harvester.conf"), "w")
f.write(p.render(conda_env_location=conda_env_location, conda_env_name=conda_env_name))
f.close()
