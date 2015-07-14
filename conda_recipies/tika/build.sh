mkdir -vp ${PREFIX}/bin;
mkdir -vp ${PREFIX}/lib/tika-rest-server/bin;
mkdir -vp ${PREFIX}/lib/tika-rest-server/lib;

cp tika-server-1.9.jar ${PREFIX}/lib/tika-rest-server/lib/;

cp ${RECIPE_DIR}/tika-rest-server ${PREFIX}/lib/tika-rest-server/bin/;
cp ${RECIPE_DIR}/tika-rest-server ${PREFIX}/bin/;
chmod +x ${PREFIX}/lib/tika-rest-server/bin/tika-rest-server;

echo -e '#!/bin/bash\nexec java -jar ../lib/tika-rest-server/lib/tika-server-1.9.jar "$@"' > ${PREFIX}/bin/tika-rest-server;
chmod +x "${PREFIX}/bin/tika-rest-server";
