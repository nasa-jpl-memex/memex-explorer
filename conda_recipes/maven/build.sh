#!/bin/bash

# Build dependencies:
# - > Java 1.7


mkdir -vp ${PREFIX}/bin;
mkdir -vp ${PREFIX}/lib;
mkdir -vp ${PREFIX}/lib/maven/bin;
mkdir -vp ${PREFIX}/lib/maven/boot;
mkdir -vp ${PREFIX}/lib/maven/conf;
mkdir -vp ${PREFIX}/lib/maven/lib;

cp -va bin/* ${PREFIX}/lib/maven/bin/;
cp -va boot/* ${PREFIX}/lib/maven/boot/;
cp -va conf/* ${PREFIX}/lib/maven/conf/;
cp -va lib/* ${PREFIX}/lib/maven/lib/;

chmod +x ${PREFIX}/lib/maven/bin/*;

pushd "${PREFIX}/bin"
ln -vs "../lib/maven/bin/mvn" mvn
ln -vs "../lib/maven/bin/mvnDebug" mvnDebug
ln -vs "../lib/maven/bin/mvnyjp" mvnyjp
popd
