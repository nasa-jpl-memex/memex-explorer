#!/bin/bash

mkdir -vp ${PREFIX}/data;

curl https://s3.amazonaws.com/vida-nyu/DDT/D_cbow_pdw_8B.pkl -o ${PREFIX}/data/D_cbow_pdw_8B.pkl
