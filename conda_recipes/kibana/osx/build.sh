mkdir -vp ${PREFIX}/bin;
mkdir -vp ${PREFIX}/lib/kibana/bin;
mkdir -vp ${PREFIX}/lib/kibana/config;
mkdir -vp ${PREFIX}/lib/kibana/plugins;
mkdir -vp ${PREFIX}/lib/kibana/node;
mkdir -vp ${PREFIX}/lib/kibana/src;

cp -r src/* ${PREFIX}/lib/kibana/src/;
cp -r plugins/* ${PREFIX}/lib/kibana/plugins/;
cp -r node/* ${PREFIX}/lib/kibana/node/;
cp -r config/* ${PREFIX}/lib/kibana/config/;

cp bin/kibana ${PREFIX}/lib/kibana/bin/kibana;
cp README.txt ${PREFIX}/lib/kibana/;
cp LICENSE.txt ${PREFIX}/lib/kibana/;

chmod +x ${PREFIX}/lib/kibana/bin/kibana;

pushd "${PREFIX}/bin";
ln -vs "../lib/kibana/bin/kibana" kibana;
