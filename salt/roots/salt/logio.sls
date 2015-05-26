# npm-gyp fails if "node" doesn't resolve to nodejs.  This fixes that issue
nodejs-legacy:
  pkg.installed

npm:
  pkg.installed

logio:
  npm.installed
