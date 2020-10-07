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
#     Róbert Kjaran <robert@kjaran.com>

import sh
import tempfile
from os import getcwd, environ, mkdir
from os.path import join, dirname,  exists
import re
import sys
from multiprocessing import Process
from config import conf
from modules.utils import simpleLog

from modules.MarosijoModule import MarosijoCommon

def genGraphs(tokensPath:list):
    """
    Generate decoding graphs for each token for our Marosijo module.
    
    Only needs to be run once (for each version of the tokens).

    Parameters:
        tokensPath      path to the token list on format "tokId token"
        output_folder   the name of the output folder
    """
    output_folder = join(getcwd(), 'modules', 'local')
    if not exists(output_folder):
        mkdir(output_folder)

    graphsArkPath = join(output_folder, 'graphs.ark')
    graphsScpPath = join(output_folder, 'graphs.scp')

    common = MarosijoCommon(join('modules', 'local'), graphs=False)

    #: Shell commands
    makeUtteranceFsts = sh.Command(join(dirname(__file__),'./marosijo_make_utterance_fsts.sh'))
    
    fstEnv = environ.copy()
    fstEnv['PATH'] = '{}/tools/openfst/bin:{}'.format(conf['kaldi_root'], fstEnv['PATH'])
    print(fstEnv['PATH'])
    makeUtteranceFsts = makeUtteranceFsts.bake(_env=fstEnv)
    compileTrainGraphsFsts = sh.Command('{}/src/bin/compile-train-graphs-fsts'
                                        .format(conf['kaldi_root']))

    tokensLines = []
    with open(tokensPath) as tokensF:
        # These tok_keys should correspond to mysql id's
        #   of tokens (because this is crucial, since the cleanup module relies
        #   on the ids, we make sure to verify this by querying the database for each token
        #   see util.DbWork)
        for line in tokensF:
            line = line.rstrip('\n')
            #tokenKey = line.split(' ')[0]
            #token = ' '.join(line.split(' ')[1:]) # split(' ') needed because split() rstrips the space by default
            tokenKey, token = line.split('\t')
            tokenInts = common.symToInt(token.lower())
            tokensLines.append('{} {}'.format(tokenKey, tokenInts))
    simpleLog('Compiling the decoding graphs (files {} and {}).  This will take a long time.'
              .format(graphsArkPath, graphsScpPath))

    compileTrainGraphsFsts(
        makeUtteranceFsts(
            common.phoneLmPath,
            common.symbolTablePath,
            _in='\n'.join(tokensLines) + '\n',
            _piped=True,
            _err=simpleLog
        ),
        '--verbose=4',
        '--batch-size=1',
        '--transition-scale=1.0',
        '--self-loop-scale=0.1',
        '--read-disambig-syms={}'.format(common.disambigIntPath),
        '{tree}'.format(tree=common.treePath),
        common.acousticModelPath,
        common.lexiconFstPath,
        'ark:-',
        'ark,scp:{ark},{scp}'.format(ark=graphsArkPath,
                                     scp=graphsScpPath),
        _err=simpleLog
    )

