mkdir -vp ${PREFIX}/bin;
mkdir -vp ${PREFIX}/lib/elasticsearch/bin;
mkdir -vp ${PREFIX}/lib/elasticsearch/lib;
mkdir -vp ${PREFIX}/lib/elasticsearch/config;
mkdir ${PREFIX}/lib/elasticsearch/lib/sigar;

mvn clean package -DskipTests;

cp -r target/lib/* ${PREFIX}/lib/elasticsearch/lib/;
cp target/elasticsearch-1.6.0.jar ${PREFIX}/lib/elasticsearch/lib/elasticsearch-1.6.0.jar;
cp -r target/bin/* ${PREFIX}/lib/elasticsearch/bin/;
cp -r config/* ${PREFIX}/lib/elasticsearch/config/;
cp ${RECIPE_DIR}/elasticsearch.yml ${PREFIX}/lib/elasticsearch/config/elasticsearch.yml;

rm ${PREFIX}/lib/elasticsearch/bin/*.exe;

chmod +x ${PREFIX}/lib/elasticsearch/bin/elasticsearch;

pushd "${PREFIX}/bin"
ln -vs "../lib/elasticsearch/bin/elasticsearch" elasticsearch
