#/bin/bash
sudo /usr/bin/salt-call state.highstate --retcode-passthrough --log-level=debug
