mkdir -vp ${PREFIX}/bin;
mkdir -vp ${PREFIX}/lib/tika-rest-server/bin;
mkdir -vp ${PREFIX}/lib/tika-rest-server/lib;

cp tika-server-1.9.jar ${PREFIX}/lib/tika-rest-server/lib/;

echo -e '#!/bin/bash\nexec java -jar $(dirname $(dirname $(which tika-rest-server)))/lib/tika-server-1.9.jar "$@"' > ${PREFIX}/lib/tika-rest-server/bin/tika-rest-server;
chmod +x "${PREFIX}/lib/tika-rest-server/bin/tika-rest-server";

echo -e '#!/bin/bash\nexec java -jar $(dirname $(dirname $(which tika-rest-server)))/lib/tika-rest-server/lib/tika-server-1.9.jar "$@"' > ${PREFIX}/bin/tika-rest-server;
chmod +x "${PREFIX}/bin/tika-rest-server";
