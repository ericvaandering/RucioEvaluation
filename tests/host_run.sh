#!/bin/bash

function usage {
  echo "Usage: $0 [OPTION]..."
  echo 'Run CMSRucio test suite'
  echo ''
  echo '  -h    Show usage.'
  echo '  -i    Start an interactive shell rather than run tests'
  exit
}

while getopts hir opt
do
  case "$opt" in
    h) usage;;
    i) interactive="true";;
  esac
done


if [[ ! -d rucio ]]; then
  git clone -b cms_nano1 https://github.com/ericvaandering/rucio.git
  pushd rucio
  git apply ../mocktool.patch
  popd
fi
docker-compose --file docker-compose.yml up -d
docker exec tests_rucio_1 /tests/setup.sh
if test ${interactive}; then
  docker exec -w /tests -it tests_rucio_1 bash
else
  docker exec -w /tests tests_rucio_1 ./run_tests.sh
fi
docker-compose --file docker-compose.yml down