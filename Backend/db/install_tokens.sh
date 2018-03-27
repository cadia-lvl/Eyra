#!/bin/bash
# Copyright 2018 The Eyra Authors. All Rights Reserved.
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
#     Judy Fong <judyfong@ru.is>


#Check if Eyra_was_here file was not created, if so do the following
if [ ! -f "./Eyra_was_here" ]; then
	BDIR=$( dirname $( readlink -f $0 ) )
	cd $BDIR && mysql -u default < malromur_tokens.sql
	touch Eyra_was_here
fi
#else do nothing because the tokens have already been inserted once via Docker