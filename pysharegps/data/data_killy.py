#http:(//www.mapcoordinates.net
from pysharegps.utils import gpsPoint, gpsSimpleLine

### user list ###
uid_list = {}

### point_list ###
point_list = {"UCPA Val d'isere" : gpsPoint(45.447536,6.982068)}
    #ucpa
    #...

### lines_list ###
line_list = {
"TCD6 de la Sache"              :gpsSimpleLine(gpsPoint(45.50645718,6.92097366),gpsPoint(45.49042172,6.9146812 )),
"TCD8/10 des Boisses"           :gpsSimpleLine(gpsPoint(45.49813671,6.92353249),gpsPoint(45.4901309 ,6.91490114),
"TKD des Almes"                 :gpsSimpleLine(gpsPoint(45.4700907 ,6.90672576),gpsPoint(45.47310897,6.90124601)),
"TKD Chardonnet"                :gpsSimpleLine(gpsPoint(45.46796139,6.90226793),gpsPoint(45.46961794,6.89162493)),	
#"TKD Claret"                    :((,,,),#TODO entre tuff et bollin
"TKD Col du Palet"              :gpsSimpleLine(gpsPoint(45.45177071,6.881513  ),gpsPoint(45.45343025,6.86450243)),
"TKD Combe Folle"               :gpsSimpleLine(gpsPoint(45.46277445,6.91362977),gpsPoint(45.45847192,6.92268491)),
"TKD Millonex 1 et 2"           :gpsSimpleLine(gpsPoint(45.46938846,6.90562874),gpsPoint(45.47068885,6.90167785)),
#    gliss'park
"TKD Pitots"                    :gpsSimpleLine(gpsPoint(45.50617271,6.92117482),gpsPoint(45.50288112,6.91940188)),#+-
"TKE Lavachet"                  :gpsSimpleLine(gpsPoint(45.47080484,6.91117287),gpsPoint(45.46858213,6.91223502)),
"TKE2 3500 1 & 2"               :gpsSimpleLine(gpsPoint(45.410496  ,6.87983394),gpsPoint(45.41254087,6.88916802)),	 #aussi appeler stade sur le plan
"TKE2 Champagny"                :gpsSimpleLine(gpsPoint(45.42081751,6.88784838),gpsPoint(45.41479278,6.88219965)),
"TKE2 Rosolin 1 & 2"            :gpsSimpleLine(gpsPoint(45.42746279,6.88537002),gpsPoint(45.41922478,6.88572407)),
"TPH V de la Grande Motte"      :gpsSimpleLine(gpsPoint(45.42329123,6.89046621),gpsPoint(45.41353127,6.8745178 )),
"funiculaire de la grande motte":gpsSimpleLine(gpsPoint(45.45232389,6.89813733),gpsPoint(45.42384092,6.89161956)),
"TSD4 de la Vanoise"            :gpsSimpleLine(gpsPoint(45.43154746,6.89945161),gpsPoint(45.42384846,6.89099729)),
"TSD4B des Lanches"             :gpsSimpleLine(gpsPoint(45.45230131,6.89761162),gpsPoint(45.43012821,6.89737558)),
"TSD6 Chaudannes"               :gpsSimpleLine(gpsPoint(45.47236664,6.91073298),gpsPoint(45.48206377,6.90598547)),
"TSD6 des Merles"               :gpsSimpleLine(gpsPoint(45.46737575,6.88817561),gpsPoint(45.45977068,6.87607884)),
"TSD6 de Palafour"              :gpsSimpleLine(gpsPoint(45.46924801,6.90634489),gpsPoint(45.47618852,6.89396918)),
"TSD6 Paquis"                   :gpsSimpleLine(gpsPoint(45.47209203,6.91075444),gpsPoint(45.45826685,6.91430569)),
"TSD6 des Tufs"                 :gpsSimpleLine(gpsPoint(45.45456794,6.90106899),gpsPoint(45.45518507,6.92033798)),
"TSF3 Marais"                   :gpsSimpleLine(gpsPoint(45.48884475,6.91530347),gpsPoint(45.48415995,6.88896418)),
"TSF3 Panoramic"                :gpsSimpleLine(gpsPoint(45.42340418,6.89035892),gpsPoint(45.42131075,6.88698471)),
"TSF4 Grand-Huit"               :gpsSimpleLine(gpsPoint(45.466528  ,6.88565433),gpsPoint(45.47223122,6.87892199)),
"TSF4 de la Leisse"             :gpsSimpleLine(gpsPoint(45.41914194,6.89837873),gpsPoint(45.42320839,6.89084172)),
"TSF4 Rosset"                   :gpsSimpleLine(gpsPoint(45.46807048,6.90875888),gpsPoint(45.46665968,6.91221356)),
"TSD TOMMEUSES"                 :gpsSimpleLine(gpsPoint(45.4592138 ,6.94095075),gpsPoint(45.45613207,6.92019582)),
"AEROSKI"                       :gpsSimpleLine(gpsPoint(45.4683075 ,6.90713346),gpsPoint(45.45563537,6.91980958)),
"TSD FRESSE"                    :gpsSimpleLine(gpsPoint(45.45112343,6.90577626),gpsPoint(45.44213549,6.92577213)),
"BOLLIN"                        :gpsSimpleLine(gpsPoint(45.45294104,6.89848602),gpsPoint(45.45122504,6.90546513)),
"TSF BREVIERES"                 :gpsSimpleLine(gpsPoint(45.5059346 ,6.92063034),gpsPoint(45.49638823,6.92242205)),
"TSF AIGUILLE ROUGE"            :gpsSimpleLine(gpsPoint(45.48847996,6.91462219),gpsPoint(45.48409978,6.90394431)),
"TSF AIGUILLE PERCEE"           :gpsSimpleLine(gpsPoint(45.47550015,6.88604593),gpsPoint(45.48451976,6.88872814)),
"TSD TICHOT"                    :gpsSimpleLine(gpsPoint(45.45405492,6.8969357 ),gpsPoint(45.45528165,6.8826288 )),
"TSF COL DES VES"               :gpsSimpleLine(gpsPoint(45.45169168,6.88247323),gpsPoint(45.44246733,6.86382651)),
"TSD GRATTALU"                  :gpsSimpleLine(gpsPoint(45.45193629,6.88165247),gpsPoint(45.46125315,6.87034428)),
"TRANSCORDE"                    :((,,,),#TODO au pied de tichot

"TPH OLYMPIQUE"                 :gpsSimpleLine(gpsPoint(45.44670397,6.97617888),gpsPoint(45.44295537,6.95164204)),
"FUNIVAL"                       :gpsSimpleLine(gpsPoint(45.45926899,6.96436644),gpsPoint(45.44320002,6.95014536)),
"TC DAILLE"                     :gpsSimpleLine(gpsPoint(45.46075523,6.96384072),gpsPoint(45.45687963,6.94386363)),
"TSD BELLEVARDE"                :gpsSimpleLine(gpsPoint(45.44737764,6.97654903),gpsPoint(45.4459362 ,6.96433425)),
"TSD BORSAT"                    :gpsSimpleLine(gpsPoint(45.44925558,6.93813443),gpsPoint(45.43289013,6.92543149)),
"TSD LOYES EXPRESS"             :gpsSimpleLine(gpsPoint(45.44268438,6.9683522 ),gpsPoint(45.44270696,6.95162058)),
"TSD MARMOTTES"                 :gpsSimpleLine(gpsPoint(45.44842764,6.93758726),gpsPoint(45.44074975,6.94916904)),
"TS ETROITS"                    :gpsSimpleLine(gpsPoint(45.46045422,6.96387291),gpsPoint(45.45595396,6.94434643)),
"TS FONTAINE FR"                :gpsSimpleLine(gpsPoint(45.43272073,6.95315212),gpsPoint(45.44297419,6.94952577)),
"TS GRAND PRE"                  :gpsSimpleLine(gpsPoint(45.43072177,6.94512427),gpsPoint(45.42290969,6.94562316)),
"TS MONT BLANC"                 :gpsSimpleLine(gpsPoint(45.44980879,6.93273246),gpsPoint(45.45749297,6.94179833)),
"TK LANCHES 1 2"                :gpsSimpleLine(gpsPoint(45.45899243,6.96480364),gpsPoint(45.45749109,6.96317017)),
"TK SEMANMILLE"                 :gpsSimpleLine(gpsPoint(45.45988418,6.9458431 ),gpsPoint(45.45715055,6.94356859)),
"TK SLALOM"                     :gpsSimpleLine(gpsPoint(45.45029614,6.93419158),gpsPoint(45.44998943,6.93857968)),
"TK SNOWPARK"                   :gpsSimpleLine(gpsPoint(45.45036388,6.93419427),gpsPoint(45.45003647,6.9386065 )),
"FIL NEIGE BOZETTO"             :gpsSimpleLine(gpsPoint(45.45188235,6.93852067),gpsPoint(45.45033566,6.93843484)),# not found on the map

"TPH SOLAISE"                   :gpsSimpleLine(gpsPoint(45.44425762,6.97719812),gpsPoint(45.43480997,6.99230433)),
"TSD GLACIER EXP"               :gpsSimpleLine(gpsPoint(45.42889591,7.0007962 ),gpsPoint(45.41763829,7.01619208)),
"TSD LEISSIERES EXP"            :gpsSimpleLine(gpsPoint(45.42095933,7.01310754),gpsPoint(45.42195711,7.02547252)),
"TSD MADELAINE EXP"             :gpsSimpleLine(gpsPoint(45.42946814,6.99549615),gpsPoint(45.42164837,6.99745417)),
"TSD MANCHET EXP"               :gpsSimpleLine(gpsPoint(45.42283816,6.97286367),gpsPoint(45.42381896,6.99584752)),
"TSD SOLAISE EXP"               :gpsSimpleLine(gpsPoint(45.44666257,6.97746098),gpsPoint(45.4342679 ,6.99331284)),
"TS CUGNAI"                     :gpsSimpleLine(gpsPoint(45.41786798,7.00716913),gpsPoint(45.41154543,7.01076865)),
"TS DATCHA"                     :gpsSimpleLine(gpsPoint(45.43155938,7.00094104),gpsPoint(45.42445714,6.99703574)),
"TS LAC"                        :gpsSimpleLine(gpsPoint(45.4301646 ,6.99554443),gpsPoint(45.43188125,6.99382782)),
"TS ROGONEY"                    :gpsSimpleLine(gpsPoint(45.44607169,6.976946  ),gpsPoint(45.4426618 ,6.98162913)),
"TS VILLAGE"                    :gpsSimpleLine(gpsPoint(45.44753194,6.97820663),gpsPoint(45.44470926,6.98033094)),
"TK LEGETTAZ"                   :gpsSimpleLine(gpsPoint(45.44249242,6.97728932),gpsPoint(45.44121648,6.98070109)),
#"TK OUILLETTE":(( #pas sur le plan officiel :(/),
"TK SAVONETTE 1 2"              :gpsSimpleLine(gpsPoint(45.44677548,6.98054552),gpsPoint(45.44495014,6.98096931)),
"TELECORDE OUILLETT"            :gpsSimpleLine(gpsPoint(45.42998014,6.99647248),gpsPoint(45.42771942,7.000705  )),
#"TELECORDE TETE SOL"            :(( #TODO dur a voir sur gmpas,voir sur opensm),
"TS TERASSE"                    :gpsSimpleLine(gpsPoint(45.43371454,6.99104905),gpsPoint(45.43174573,6.99332893)),

"TPH FORNET"                    :gpsSimpleLine(gpsPoint(45.45033942,7.01155186),gpsPoint(45.44271072,7.01758951)),
"TC VALLON"                     :gpsSimpleLine(gpsPoint(45.44246608,7.01779068),gpsPoint(45.4208765 ,7.03330457)),
"TSD LAISINANT EXP"             :gpsSimpleLine(gpsPoint(45.44709349,6.99432939),gpsPoint(45.43684643,7.00997472)),
"TSD PYRAMIDES EXP"             :gpsSimpleLine(gpsPoint(45.44214992,7.017214  ),gpsPoint(45.43399687,7.02873945)),
"TK COL 1 2"                    :gpsSimpleLine(gpsPoint(45.42955473,7.02376127),gpsPoint(45.42164648,7.03481197)),
"TK SIGNAL 1 2"                 :gpsSimpleLine(gpsPoint(45.43402134,7.02892989),gpsPoint(45.43480809,7.03541547)),

"TSD CASCADES EXP"              :gpsSimpleLine(gpsPoint(45.42153165,7.04004228),gpsPoint(45.42205124,7.06038415)),
"TS CEMA"                       :gpsSimpleLine(gpsPoint(45.42088403,7.03395903),gpsPoint(45.4212982 ,7.04007983)),
"TK MONTETS"                    :gpsSimpleLine(gpsPoint(45.42423688,7.05402732),gpsPoint(45.42259719,7.06546962)),
"TK PAYS DESERT"                :gpsSimpleLine(gpsPoint(45.421125  ,7.04107493),gpsPoint(45.4170697 ,7.03892648))}
