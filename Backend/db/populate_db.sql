/*
Copyright 2016 The Eyra Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

/*
File author/s:
    Matthias Petursson <oldschool01123@gmail.com>
*/

-- basic inserts to start with the "dummy" instructors/devices etc
start transaction;

insert into device (userAgent, imei)
values
    ('Mobile Browser Mozilla etc.', 'NOTAVALIDPHONEID');
insert into instructor (name, email, phone, address)
values
    ('Jane Doe', 'dummy@jk.is', '1-800-DONT-CALL', 'Australia');
insert into speaker (name, deviceImei)
values
    ('John Doe', 'NOTAVALIDPHONEID');
insert into speaker_info (speakerId, s_key, s_value)
values
    (1, 'sex', 'male'),
    (1, 'dob', '1991-1995'),
    (1, 'height', '170');
insert into session (speakerId, instructorId, deviceId, location, start, end, comments)
values 
    (1, 1, 1, 'Norway etc.', '2015/10/1 15:00:00.00', '2015/10/1 15:00:30.05', 'Much wind.');
-- add the special set Random
insert into recording (tokenId, speakerId, sessionId, filename, rec_method)
values
    (1, 1, 1, 'NOTAREALRECORDING', 'eyra');
insert into evaluation_sets (eval_set, recordingId)
values
    ('Random', 1);
insert into recording_agreement (agreement)
values
    ('                 <div class="agreement"><p>SAMÞYKKISYFIRLÝSING</p><h2>===============</h2><p>Háskólinn á Akureyri hefur hér með leyfi til þess að taka upp taldæmi frá þér, ásamt því að skrá ópersónugreinanlegar upplýsingar um þig, eins og kyn og aldur.<p>Þú staðfestir hér með að þú sért sjálfráða og getir þar með skrifað undir samkomulag sem þetta.</p><p>Með því að taka þátt:</p><p>1. Samþykkir þú að lesa inn texta á íslensku með aðstoð þess hugbúnaðar sem notaður er í verkefninu.</p><p>2. Samþykkir þú að upptökurnar og þau lýsigögn sem fylgja megi vera opin og aðgengileg á vefnum og að þau megi nota til þess að þróa máltæknihugbúnað fyrir íslensku. Þér er ljóst að mögulegt gæti verið að þekkja þína rödd í gagnasafninu, þó engin önnur persónugreinanleg gögn verði vistuð með upptökunum sem þú lest upp.</p> <p>Þú skilur og samþykkir að:</p><p>1. Textarnir sem þér er ætlað að lesa eru að stórum hluta af fréttamiðlum og geta innihaldið lýsingar sem ganga gegn skoðunum þínum eða siðferðiskennd. Þér er frjálst að sleppa því að lesa slíka texta, en gagnlegt væri að fá ábendingu um slíkt efni í safninu.</p> <p> 2. Engin skylda hvílir á Háskólanum á Akureyri eða öðrum, að nýta sér þær upptökur sem þú lest inn. Engin laun eru veitt fyrir þátttöku í verkefninu.</p></div>');

commit;