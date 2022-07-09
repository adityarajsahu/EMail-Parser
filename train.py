import spacy
import random
from spacy.util import minibatch, compounding
from spacy.training.example import Example
from spacy.tokens import DocBin
from pathlib import Path
nlp = spacy.blank("en")

training_data = [
    (
        'Dear SIR, Pls propose suitable vsl for below our cgo: CARGO: 39 X 40`SOC EMPTY TANK CONTAINERS WITH RESIDUE INSIDE RESIDUE: AROUND 300KG PER CONTAINER. DG 2.2, UN 1963, HELIUM REFRIGERATED. MSDS ATTACHED. CONTAINER WEIGHT: 17000KG VLADIVOSTOK COMMERCIAL PORT, RUSSIA – JEBEL ALI,UAE FREE TIME 48HRS IN TOTAL FULLY REVERSIBLE SPOT CARGO, PLEASE OFFER A FIRM VESSEL FRT INVITE OWNER BEST OFFER FIOS TERMS BSS 1/1 COMM: 2.5% TTL ***RUSSIAN FLAG VESSELS ARE NOT ACCEPTABLE DUE TO INSURANCE ISSUES Awaiting yours Kind regards/Mr Frank MOB: +84 933 123 923 ============================================== HAI LANG TRADING AND TRANSPORT CO.,LTD Head office: 14/23C Van Chung Str, Ward 13, Tan Binh Dist, HCMC, Vietnam Tel/Fax: +84 28 2212 3232 Website: www.hailangtraco.com Email: charter@hailangtraco.com ( For chartering only)',
        {"entities": [(773, 797, 'email'), (73, 114, 'cargo'), (231, 258, 'origin_port'), (260, 266, 'origin_country'), (269, 278, 'des_port'), (279, 282, 'des_country'), (223, 230, 'weight')]}
    ),
    (
        'EXODUS CHARTERING SERVICES., INDIA TEL: 0091-44-26542962 EMAIL: chartering@exoduschartering.info --------------------------------------------------------------- GOOD DAY 5000MT BGD RICE PART CARGO OK / SEPARATE HATCH ANGRE / MERSIN 1500 / 1500 PROMPT COMM 2.5 PCT B.RGDS / MANUEL MOB: 91-9840446665, AS BROKERS ONLY E. & O. E. All details about and given in good faith. SKYPE: manuel13291 ================================================== This is email broadcast to shipbroking & shipping community and not spam. If you are not interested please notify us in return with subject "remove us" ================================================== *Treat hyperlinks and attachments if any in this email with caution.*',
        {"entities": [(64, 96, 'email'), (181, 185, 'cargo'), (217, 222, 'origin_port'), (225, 231, 'des_port'), (232, 236, 'weight')]}
    ),
    (
        'Good day Please propose suitable vessel for fixing Acc Bulk asia SMX 1 TCT WITH COAL DEL GANGAVARAM REDEL NEW MANGALORE LAYCAN 19-21 APR DURATION ABT 10-12 DAYS WOG 5% TTL COMM Best regards / Stavros Tassios mob  : 0030 6973862967 skype: staurostassios ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ United Seas Corp. Konitsis 5 & Kifisias ave,4th floor Marousi 151-25, greece Tel     : 0030 210 8064867/8066243 Email   : chartering@unitedseascorp.gr position@unitedseascorp.gr Web     : www.unitedseascorp.gr Members : Bimco reg.no.178704,Baltic Exchange,H.S.A ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~',
        {"entities": [(427, 455, 'email'), (80, 84, 'cargo'), (89, 99, 'origin_port'), (110, 119, 'des_port')]}
    ),
    (
        'Dear Sir, Please find attached Noon at Sea report with thanks. Best Regards, Capt. Vicente Almerol Master | MV Agia Doxa SAT.Phone (Master): +30 211 1986 260 SAT.Phone (Bridge): +30 211 1985 472 Mob.+306947566433 INM-C (1/2): 463722361 / 463727341 E-mail: master@agiadoxa.samiosfleet.com',
        {"entities": [(256, 286, 'email')]}
    ),
    (
        'Please propose for: Cargill Handy Del SW Pass Redel Rio Haina 1 tct w grains abt 30 days April 22-24 3.75 addcom pus Best regards, Martin Sarli Atlantic Brokers - As brokers only - Ph +541152370267 Cel +5491170169749 Skype: Martin Sarli',
        {"entities": [(48, 61, 'origin_port')]}
    ),
    (
        'Cargill open Can do 1tct or consider period on below handy requirement MR/Rio Haina 30k 5pct two grades as below 7500sshex/4000satpmshex April 20-25 3.75 adc + 1.25 Peraco 21k corn & 9k sbm – 5pct each Best Regards, Ed Lundin Office: 203 977 7600 Direct: 203 977 7603 Mobile:203 219 2500',
        {"entities": [(8, 37, 'cargo'), (91, 103, 'origin_port'), (105, 114, 'origin_country'), (121, 132, 'des_port'), (134, 139, 'des_country'), (45, 54, 'weight')]}
    ),
    (
        'Dear Sir PLEASE OFFER FOR BELOW PRACELS: 9/10,000 MT FLY ASH IN JUMBO BAGS (1.4 MT EACH) POL: MUNDRA, WC INDIA POD: DAMMAM OR JEDDAH, S.ARABIA LAYCAN: PROMPT (TRY VSL DATES)  L.RATE: 750 MT PWWD SSHEX UU PER HOOK D RATE: LINER OUT PART CARGO OK FILO - 1/1 3.75% TTL',
        {"entities": [(53, 60, 'cargo'), (94, 100, 'origin_port'), (105, 110, 'origin_country'), (126, 132, 'des_port'), (134, 142, 'des_country'), (41, 52, 'weight')]}
    ),
    (
        'APRIL 15TH, 2022 MID-SHIP DUBAI GOOD DAY PLEASE OFFER FIRM FOR: A/C MAADEN 25,000 MTS 10% MOLOO BULK MAP RAS AL KHAIR / NOLA LAYCAN 22-24 APRIL 10,000 FHEX UU / 10,000 SHINC 2.5ADCOM PUS PLEASED TO HEAR BEST REGARD THOMAS TSIMOURTOS+PUSHKAR POTDAR (AS BROKERS ONLY) ( PLEASE CONTACT US ON OUR MOBILE NUMBERS AS WE MIGHT BE WORKING REMOTELY ) MOBILE: +971 50 6528195  SKYPE –  TSIMOURTOS@LIVE.COM E-MAIL – TTSIMOURTOS@MIDSHIP.COM | INDIVIDUALLY STRONG - UNBEATABLE AS A TEAM ! SHIP BROKERS * CARGO BROKERS * LOGISTICS * CONSULTING * SURVEYING * WAREHOUSING * TRUCKING * PROJECT CARGO NEW YORK * CORAL GABLES * NEW ORLEANS * HOUSTON* PITTSBURGH * SEOUL * CARTAGENA ISTANBUL * BELO HORIZONTE * SAO PAULO * BEIJING * MEXICO * DUBAI * ABU DHABI',
        {"entities": [(405, 428, 'email'), (75, 85, 'weight')]}
    ),
    (
        'APRIL 15TH, 2022 MID-SHIP DUBAI GOOD DAY PLEASE OFFER FIRM FOR: A/C MAADEN 25,000 MTS 10% MOLOO BULK MAP RAS AL KHAIR / NOLA LAYCAN 22-24 APRIL 10,000 FHEX UU / 10,000 SHINC 2.5ADCOM PUS PLEASED TO HEAR BEST REGARD THOMAS TSIMOURTOS+PUSHKAR POTDAR (AS BROKERS ONLY) ( PLEASE CONTACT US ON OUR MOBILE NUMBERS AS WE MIGHT BE WORKING REMOTELY ) MOBILE: +971 50 6528195  SKYPE –  TSIMOURTOS@LIVE.COM E-MAIL – TTSIMOURTOS@MIDSHIP.COM | INDIVIDUALLY STRONG - UNBEATABLE AS A TEAM ! SHIP BROKERS * CARGO BROKERS * LOGISTICS * CONSULTING * SURVEYING * WAREHOUSING * TRUCKING * PROJECT CARGO NEW YORK * CORAL GABLES * NEW ORLEANS * HOUSTON* PITTSBURGH * SEOUL * CARTAGENA ISTANBUL * BELO HORIZONTE * SAO PAULO * BEIJING * MEXICO * DUBAI * ABU DHABI',
        {"entities": [(75, 85, 'weight')]}
    ),
    (
        "Doc-No. 171071180   15/APR/2022 (FRI)  16:21  (+0200)  PIA Howe Robinson Partners - Operations Dept. London and Hamburg To Vega Bulk Dear Saurabhh / Pia Good day, Pls find fllwg ntc from Ownrs. QU MV Four Rigoletto / Acct Vega Bulk Carriers - CP dated 25th March 2022 Good day, Please note as per latest update from Master vessel berthed at Algiers on 11th April and discharging commenced on 14th April. Estimated completion time is 20th April, agw wp uce. In view of the above, we hereby tender our daily notice of vessel's delivery to Charterers at DLOSP Algiers on about 20th April 2022, agw wp uce. Above delivery notice is given in good faith and basis all information present to Owners, where unforeseen circumstances are excepted. Best regards UNQU Many thanks & kind regards, Pia Dmuschewsky | Post Fixtures - dry cargo in Hamburg dir: +49 40 22630 8320/21 | mob: +49 162 216 5546 From : hrs.opsldn@howerobinson.co To : Vega Bulk Group - Ops (ops@vegabulk.com) / CC: Vega Bulk Group - Oslo (oslo@vegabulk.com) Subject : MV FOUR RIGOLETTO-9 / Acct Vega Bulk Carriers - CP dtd 25.03.22 - Delivery Notice Date : 14/04/2022 12:26:03",
        {"entities": [(896, 922, 'email')]}
    ),
    (
        'DIRECT/PLS PPS OPEN WARRI/NIGERIA O/A 30TH APRIL TCT ONLY GRAIN CLEAN // ALL DIR OKAY MV YANGTZE DAWN BULK CARRIER FLAG : MARSHALL ISLANDS CLASS : LR BULT: 2010 BY HANTONG DWAT/DRAFT/TPC: SSW ABT. 56700 MT ON 12.8 M/ 58.8 LOA/BEAM/DEP: 189.99 M / 32.26M/18M GT/NT: 32987/19231 HOLDS/HATCHES: 5 / 5 HATCH COVER : HYDRAULIC FOLDING TYPE HATCH DIMENSIONS: NO.1 : 18.86M X 18.26M NO. 2+3+4+5 : 21.32M X 18.26M CARGO CAPACITIES: GRAIN/M3 : 71634 BALE: 68200 CRANES 4 X 35.0T GRAB 4 X 12CBM SPEED/CONSUMPTION AS VESSEL TRADING AT OPEN SEA FOR 24 HOURS: BALLAST : ABT 13.5KN ON ABT30.2MT VLSFO + 0.1MT LSMGO LADEN : ABT 13KN ON ABT30.2MT VLSFO + 0.1MT LSMGO ECO SPD/CONS BALLAST : ABT 12.25KN ON ABT 25MT VLSFO + 0.1MT LSMGO LADEN : ABT 12.0KN ON ABT 25MT VLSFO + 0.1MT LSMGO IN PORT : ABT 3.5 MT VLSFO +0.1MT LSMGO IDLE ABT 6.0MT VLSFO +0.1MT LSMGO BSS CRANE WORKING ADA',
        {"entities": [(197, 205, 'weight')]}
    ),
    (
        'TO : VEGA BULK CARRIERS AS/George Gd day our close head ows try any aussie/seasia cgo/trip incl coal mv Sand Topic - (Onomichi 60k dwt) – Dung Quat, Vietnam 24 Apr. Bod abt 1,050 mts vlsfo rm/abt 290 mts ulsfo dm (lsmgo.) _____ full specs/plans/certs avail here Best regards, Mobile/WhatsApp : +30 6948 529020 / S : giorgos.kourounis',
        {"entities": [(96, 100, 'cargo'), (173, 182, 'weight')]}
    ),
    (
        "EASTWEST CHARTERING - FAREAST DESK Tel : 1 301 540 8631 Fax : 1 801 409 3572 Eml :chartering@ewship.com Skp : ewship / Wechat: ewship ______________________________________ 1) - A/c Times Shipping Pte. Ltd. - About 20000 dwt upto Supramax - Del Vladivostok-Vostochny rge, CIS - Laycan: 20/30th Apr - TCT with steel billets/slabs - Dur 1bt 15/20 dys wog - Redel Taiwan - 3.75adc pus  +++ 2) - A/c Times Shipping - About 17000-35000 dwt - max 25ys - Del CJK, China - 22/27 April (try bit late) - tct with intn steel - Dur abt 15/20 dys wog - Redel SE Asia (Pico) - 3.75adc pus end.. Regards / Sameer",
        {"entities": [(82, 103, 'email'), (309, 322, 'cargo'), (245, 256, 'origin_port'), (257, 266, 'des_port'), (215, 224, 'weight')]}
    ),
    (
        "PLS OFFER FIRM FOR - 20.000/30.000 MTS BULK SALT - SFAX/SOUTHAMPTON - 2/7 MAY - 8.000 SC/8.000 SX - 3,75% TTL PLSD TO HEAR TKS&RGD +++ ERNA SHIPPING&TRAD.LTD.CO.-ISTANBUL Phn: +905324707916 Skype: ernaship",
        {"entities": [(44, 48, 'cargo'), (51, 55, 'origin_port'), (56, 67, 'des_port'), (21, 38, 'weight')]}
    ),
    (
        "Dear sir, Good day. Kindly note that ETA Damietta, Egypt is 29 Apr 2022 / 1200 LT  (29 / 1000 UTC) if AGW WP. Please inform all concerned parties accordingly and acknowledge safe receipt of this message. Thanks and Best Regards, Capt. Soumen Sen. M.V. Vega Falktind IMO NO: 9497426 | Call Sign: V7A5267 MMSI:  |  OFFICIAL NO: FBB#: +870773244547 Inm C Telex 1 #: Inm. Fax: E-mail: vega.falktind@thomefleet.net",
        {"entities": [(381, 408, 'email')]}
    ),
    (
        "Dear sir, Good day. Kindly note that ETA Suez Canal, Egypt is 28 Apr 2022 / 1200 LT  (28 / 1000 UTC) if AGW WP. Please inform all concerned parties accordingly and acknowledge safe receipt of this message. Thanks and Best Regards, Capt. Soumen Sen. M.V. Vega Falktind IMO NO: 9497426 | Call Sign: V7A5267 MMSI:  |  OFFICIAL NO:  FBB#: +870773244547 Inm C Telex 1 #: Inm. Fax: E-mail: vega.falktind@thomefleet.net",
        {"entities": [(384, 411, 'email')]}
    ),
    (
        "Doc-No. 171006443   07/APR/2022 (THU)  11:31  (+0200)  MSB Howe Robinson Partners - Operations Dept. London and Hamburg Saurabh / Mads 4th reminder to below. Please advise. Best regards Mads Bjornerem | Post Fixtures - Dry Cargo Bergen Mob: + 47 92446773 Email: hrs.opsldn@howerobinson.com",
        {"entities": [(262, 288, 'email')]}
    )
]

LABEL = ['email', 'cargo', 'origin_port', 'origin_country', 'des_port', 'des_country', 'weight']

nlp = spacy.blank('en')

if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
else:
    ner = nlp.get_pipe('ner')

for i in LABEL:
    ner.add_label(i)

optimizer = nlp.begin_training()
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):
    for itn in range(10):
        random.shuffle(training_data)
        losses = {}
        batches = minibatch(training_data, size=compounding(4., 32., 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            example = Example.from_dict(texts, annotations)
            nlp.update([example], sgd=optimizer, drop=0.35, losses=losses)
        print("Losses", losses)

