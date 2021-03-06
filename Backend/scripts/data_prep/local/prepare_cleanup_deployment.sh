#!/bin/bash -eu
#
# Copyright 2016 The Eyra Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# File author/s:
#     Robert Kjaran <robert@kjaran.com>
#     Matthias Petursson <oldschool01123@gmail.com>

# Prepares a tarball with files necessary for the Cleanup QC module
# in Eyra

help_message="Usage: $0 <lang-dir> <exp-dir> <sample-freq> <out-tgz>"

err() {
  msg=$1
  code=${2:-1}
  echo "$msg" >&2
  exit $code
}

msg() {
  echo "$1" >&2
}

if [ $# -ne 4 ]; then
  err "$help_message"
fi

lang=$1
exp=$2
sample_freq=$3
out_tgz=$4

tmp="$(mktemp -d)"
trap "rm -rf $tmp" EXIT

msg "Copying files from $lang"
cp $lang/L_disambig.fst $tmp/L_disambig.fst \
  || err "Lexicon FST missing from $lang"
cp $lang/oov.int $tmp/oov.int \
  || err "oov.int missing from $lang"
cp $lang/words.txt $tmp/words.syms \
  || err "words.txt missing from $lang"
cp $lang/phones/disambig.int $tmp/disambig.int \
  || err "phones/disambig.int missing from $lang"

msg "Copying files from $exp"
cp $exp/tree $tmp/tri1.tree || err "tree missing from $exp"
cp $exp/final.mdl $tmp/tri1.acoustic_mdl || err "final.mdl missing from $exp"

msg "Sample frequency of WAV files is $sample_freq"
echo "$sample_freq" > $tmp/sample_freq

tar --transform 's/.*\///g' -cvzf $out_tgz $tmp/*

msg "Done."
msg "Output in $out_tgz"
