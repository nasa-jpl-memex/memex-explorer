# npm-gyp fails if "node" doesn't resolve to nodejs.  This fixes that issue
nodejs-legacy:
  pkg.installed

npm:
  pkg.installed:
    - require:
        - pkg: nodejs-legacy

# npm.installed does NOT do the right thing here, hardcoding an install
logio:
  cmd.run:
    - name: "sudo npm install -g log.io"
    - require:
      - pkg: npm