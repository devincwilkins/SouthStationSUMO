import numpy as np
import csv
import pandas as pd
from utils import import_test_configuration, set_sumo

config = import_test_configuration(config_file='settings/settings.ini')
schedule_path = 'schedules/'+config['schedule_file_name']


class TrafficGenerator:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def generate_routefile(self, seed):
        with open("scene/routefile.rou.xml", "w") as routes:
            print("""<routes>
            <vType id="CR" vClass="rail" accel="0.8" decel="0.8" sigma="0.5" length="80" minGap="8" maxSpeed="4.5" guiShape="rail" carFollowModel="Rail" trainType="ICE1" >
                <param key="carriageLength" value="20"/>
                <param key="carriageGap" value="1"/>
                <param key="locomotiveLength" value="6"/> 
            </vType>
            <route edges="Start2toAB2 AB2toAC ACtoU UtoS StoR RtoQ QtoS1 L1_in DummyLink1" color="yellow" id="Track5toL1"/>
            <route edges="Start2toAB2 AB2toAC ACtoU UtoS StoR RtoQ QtoS2 L2_in DummyLink2" color="yellow" id="Track5toL2"/>
            <route edges="Start2toAB2 AB2toAC ACtoU UtoS StoR RtoN NtoO OtoP PtoS3 L3_in DummyLink3" color="yellow" id="Track5toL3"/>
            <route edges="Start2toAB2 AB2toAC ACtoU UtoS StoR RtoN NtoO OtoP PtoS4 L4_in DummyLink4" color="yellow" id="Track5toL4"/>
            <route edges="Start2toAB2 AB2toAC ACtoU UtoS StoL LtoM MtoS5 L5_in DummyLink5" color="yellow" id="Track5toL5"/>
            <route edges="Start2toAB2 AB2toAC ACtoU UtoS StoL LtoM MtoS6 L6_in DummyLink6" color="yellow" id="Track5toL6"/>
            <route edges="Start2toAB2 AB2toAB ABtoAD ADtoX XtoK KtoZ2 Z2toZ3 Z3toS7 L7_in DummyLink7" color="yellow" id="Track5toL7"/>
            <route edges="Start2toAB2 AB2toAB ABtoAD ADtoX XtoK KtoZ2 Z2toZ3 Z3toS8 L8_in DummyLink8" color="yellow" id="Track5toL8"/>
            <route edges="Start2toAB2 AB2toAB ABtoAD ADtoX XtoK KtoZ2 Z2toZ ZtoZ4 Z4toS9 L9_in DummyLink9" color="yellow" id="Track5toL9"/>
            <route edges="Start2toAB2 AB2toAB ABtoAD ADtoX XtoK KtoZ2 Z2toZ ZtoZ4 Z4toY YtoS10 L10_in DummyLink10" color="yellow" id="Track5toL10"/>

            <route edges="Start4toW2 W2toX XtoK KtoL LtoN NtoO OtoQ QtoS1 L1_in DummyLink1" color="yellow" id="Track1toL1"/>
            <route edges="Start4toW2 W2toX XtoK KtoL LtoN NtoO OtoQ QtoS2 L2_in DummyLink2" color="yellow" id="Track1toL2"/>
            <route edges="Start4toW2 W2toX XtoK KtoL LtoN NtoO OtoP PtoS3 L3_in DummyLink3" color="yellow" id="Track1toL3"/>
            <route edges="Start4toW2 W2toX XtoK KtoL LtoN NtoO OtoP PtoS4 L4_in DummyLink4" color="yellow" id="Track1toL4"/>
            <route edges="Start4toW2 W2toX XtoK KtoL LtoM MtoS5 L5_in DummyLink5" color="yellow" id="Track1toL5"/>
            <route edges="Start4toW2 W2toX XtoK KtoL LtoM MtoS6 L6_in DummyLink6" color="yellow" id="Track1toL6"/>
            <route edges="Start4toW2 W2toX XtoK KtoZ2 Z2toZ3 Z3toS7 L7_in DummyLink7" color="yellow" id="Track1toL7"/>
            <route edges="Start4toW2 W2toX XtoK KtoZ2 Z2toZ3 Z3toS8 L8_in DummyLink8" color="yellow" id="Track1toL8"/>
            <route edges="Start4toW2 W2toX XtoK KtoZ2 Z2toZ ZtoZ4 Z4toS9 L9_in DummyLink9" color="yellow" id="Track1toL9"/>
            <route edges="Start4toW2 W2toX XtoK KtoZ2 Z2toZ ZtoZ4 Z4toY YtoS10 L10_in DummyLink10" color="yellow" id="Track1toL10"/>
            <route edges="Start4toW2 W2toW WtoA AtoB BtoV2 V2toV VtoV4 V4toG GtoH HtoS11 L11_in DummyLink11" color="yellow" id="Track1toL11"/>
            <route edges="Start4toW2 W2toW WtoA AtoB BtoV2 V2toV VtoV4 V4toG GtoH HtoJ JtoS12 L12_in DummyLink12" color="yellow" id="Track1toL12"/>
            <route edges="Start4toW2 W2toW WtoA AtoB BtoV2 V2toV VtoV4 V4toG GtoH HtoJ JtoS13 L13_in DummyLink13" color="yellow" id="Track1toL13"/>

            <route edges="Start6toA AtoB BtoK KtoL LtoN NtoO OtoQ QtoS1 L1_in DummyLink1" color="yellow" id="TrackDB1toL1"/>
            <route edges="Start6toA AtoB BtoK KtoL LtoN NtoO OtoQ QtoS2 L2_in DummyLink2" color="yellow" id="TrackDB1toL2"/>
            <route edges="Start6toA AtoB BtoK KtoL LtoN NtoO OtoP PtoS3 L3_in DummyLink3" color="yellow" id="TrackDB1toL3"/>
            <route edges="Start6toA AtoB BtoK KtoL LtoN NtoO OtoP PtoS4 L4_in DummyLink4" color="yellow" id="TrackDB1toL4"/>
            <route edges="Start6toA AtoB BtoK KtoL LtoM MtoS5 L5_in DummyLink5" color="yellow" id="TrackDB1toL5"/>
            <route edges="Start6toA AtoB BtoK KtoL LtoM MtoS6 L6_in DummyLink6" color="yellow" id="TrackDB1toL6"/>
            <route edges="Start6toA AtoB BtoK KtoZ2 Z2toZ3 Z3toS7 L7_in DummyLink7" color="yellow" id="TrackDB1toL7"/>
            <route edges="Start6toA AtoB BtoK KtoZ2 Z2toZ3 Z3toS8 L8_in DummyLink8" color="yellow" id="TrackDB1toL8"/>
            <route edges="Start6toA AtoB BtoV2 V2toV3 V3toZ ZtoZ4 Z4toS9 L9_in DummyLink9" color="yellow" id="TrackDB1toL9"/>
            <route edges="Start6toA AtoB BtoV2 V2toV VtoV4 V4toY YtoS10 L10_in DummyLink10" color="yellow" id="TrackDB1toL10"/>
            <route edges="Start6toA AtoB BtoV2 V2toV VtoV4 V4toG GtoH HtoS11 L11_in DummyLink11" color="yellow" id="TrackDB1toL11"/>
            <route edges="Start6toA AtoB BtoV2 V2toV VtoV4 V4toG GtoH HtoJ JtoS12 L12_in DummyLink12" color="yellow" id="TrackDB1toL12"/>
            <route edges="Start6toA AtoB BtoV2 V2toV VtoV4 V4toG GtoH HtoJ JtoS13 L13_in DummyLink13" color="yellow" id="TrackDB1toL13"/>

            <route edges="L1_in L1_out S1toQ QtoO OtoN NtoL LtoK KtoB BtoA AtoStart6" color="yellow" id="L1toTrackDB1"/>
            <route edges="L2_in L2_out S2toQ QtoO OtoN NtoL LtoK KtoB BtoA AtoStart6" color="yellow" id="L2toTrackDB1"/>
            <route edges="L3_in L3_out S3toP PtoO OtoN NtoL LtoK KtoB BtoA AtoStart6" color="yellow" id="L3toTrackDB1"/>
            <route edges="L4_in L4_out S4toP PtoO OtoN NtoL LtoK KtoB BtoA AtoStart6" color="yellow" id="L4toTrackDB1"/>
            <route edges="L5_in L5_out S5toM MtoL LtoK KtoB BtoA AtoStart6" color="yellow" id="L5toTrackDB1"/>
            <route edges="L6_in L6_out S6toM MtoL LtoK KtoB BtoA AtoStart6" color="yellow" id="L6toTrackDB1"/>
            <route edges="L7_in L7_out S7toZ3 Z3toZ2 Z2toK KtoB BtoA AtoStart6" color="yellow" id="L7toTrackDB1"/>
            <route edges="L8_in L8_out S8toZ3 Z3toZ2 Z2toK KtoB BtoA AtoStart6" color="yellow" id="L8toTrackDB1"/>
            <route edges="L9_in L9_out S9toZ4 Z4toZ ZtoV3 V3toV2 V2toB BtoA AtoStart6" color="yellow" id="L9toTrackDB1"/>
            <route edges="L10_in L10_out S10toY YtoV4 V4toV VtoV2 V2toB BtoA AtoStart6" color="yellow" id="L10toTrackDB1"/>
            <route edges="L11_in L11_out S11toH HtoG GtoV4 V4toV VtoV2 V2toB BtoA AtoStart6" color="yellow" id="L11toTrackDB1"/>
            <route edges="L12_in L12_out S12toJ JtoH HtoG GtoV4 V4toV VtoV2 V2toB BtoA AtoStart6" color="yellow" id="L12toTrackDB1"/>
            <route edges="L13_in L13_out S13toJ JtoH HtoG GtoV4 V4toV VtoV2 V2toB BtoA AtoStart6" color="yellow" id="L13toTrackDB1"/>

            <route edges="Start7toEnt4 Ent4toC CtoB BtoK KtoL LtoN NtoO OtoQ QtoS1 L1_in DummyLink1" color="yellow" id="TrackDB2toL1"/>
            <route edges="Start7toEnt4 Ent4toC CtoB BtoK KtoL LtoN NtoO OtoQ QtoS2 L2_in DummyLink2" color="yellow" id="TrackDB2toL2"/>
            <route edges="Start7toEnt4 Ent4toC CtoB BtoK KtoL LtoN NtoO OtoP PtoS3 L3_in DummyLink3" color="yellow" id="TrackDB2toL3"/>
            <route edges="Start7toEnt4 Ent4toC CtoB BtoK KtoL LtoN NtoO OtoP PtoS4 L4_in DummyLink4" color="yellow" id="TrackDB2toL4"/>
            <route edges="Start7toEnt4 Ent4toC CtoB BtoK KtoL LtoM MtoS5 L5_in DummyLink5" color="yellow" id="TrackDB2toL5"/>
            <route edges="Start7toEnt4 Ent4toC CtoB BtoK KtoL LtoM MtoS6 L6_in DummyLink6" color="yellow" id="TrackDB2toL6"/>
            <route edges="Start7toEnt4 Ent4toC CtoB BtoK KtoZ2 Z2toZ3 Z3toS7 L7_in DummyLink7" color="yellow" id="TrackDB2toL7"/>
            <route edges="Start7toEnt4 Ent4toC CtoB BtoK KtoZ2 Z2toZ3 Z3toS8 L8_in DummyLink8" color="yellow" id="TrackDB2toL8"/>
            <route edges="Start7toEnt4 Ent4toC CtoB BtoV2 V2toV3 V3toZ ZtoZ4 Z4toS9 L9_in DummyLink9" color="yellow" id="TrackDB2toL9"/>
            <route edges="Start7toEnt4 Ent4toC CtoV1 V1toV4 V4toY YtoS10 L10_in DummyLink10" color="yellow" id="TrackDB2toL10"/>
            <route edges="Start7toEnt4 Ent4toC CtoV1 V1toV4 V4toG GtoH HtoS11 L11_in DummyLink11" color="yellow" id="TrackDB2toL11"/>
            <route edges="Start7toEnt4 Ent4toC CtoV1 V1toV4 V4toG GtoH HtoJ JtoS12 L12_in DummyLink12" color="yellow" id="TrackDB2toL12"/>
            <route edges="Start7toEnt4 Ent4toC CtoV1 V1toV4 V4toG GtoH HtoJ JtoS13 L13_in DummyLink13" color="yellow" id="TrackDB2toL13"/>

            <route edges="L1_in L1_out S1toQ QtoO OtoN NtoL LtoK KtoB BtoC CtoEnt4 Ent4toStart7" color="yellow" id="L1toTrackDB2"/>
            <route edges="L2_in L2_out S2toQ QtoO OtoN NtoL LtoK KtoB BtoC CtoEnt4 Ent4toStart7" color="yellow" id="L2toTrackDB2"/>
            <route edges="L3_in L3_out S3toP PtoO OtoN NtoL LtoK KtoB BtoC CtoEnt4 Ent4toStart7" color="yellow" id="L3toTrackDB2"/>
            <route edges="L4_in L4_out S4toP PtoO OtoN NtoL LtoK KtoB BtoC CtoEnt4 Ent4toStart7" color="yellow" id="L4toTrackDB2"/>
            <route edges="L5_in L5_out S5toM MtoL LtoK KtoB BtoC CtoEnt4 Ent4toStart7" color="yellow" id="L5toTrackDB2"/>
            <route edges="L6_in L6_out S6toM MtoL LtoK KtoB BtoC CtoEnt4 Ent4toStart7" color="yellow" id="L6toTrackDB2"/>
            <route edges="L7_in L7_out S7toZ3 Z3toZ2 Z2toK KtoB BtoC CtoEnt4 Ent4toStart7" color="yellow" id="L7toTrackDB2"/>
            <route edges="L8_in L8_out S8toZ3 Z3toZ2 Z2toK KtoB BtoC CtoEnt4 Ent4toStart7" color="yellow" id="L8toTrackDB2"/>
            <route edges="L9_in L9_out S9toZ4 Z4toZ ZtoV3 V3toV2 V2toB BtoC CtoEnt4 Ent4toStart7" color="yellow" id="L9toTrackDB2"/>
            <route edges="L10_in L10_out S10toY YtoV4 V4toV1 V1toC CtoEnt4 Ent4toStart7" color="yellow" id="L10toTrackDB2"/>
            <route edges="L11_in L11_out S11toH HtoG GtoV4 V4toV1 V1toC CtoEnt4 Ent4toStart7" color="yellow" id="L11toTrackDB2"/>
            <route edges="L12_in L12_out S12toJ JtoH HtoG GtoV4 V4toV1 V1toC CtoEnt4 Ent4toStart7" color="yellow" id="L12toTrackDB2"/>
            <route edges="L13_in L13_out S13toJ JtoH HtoG GtoV4 V4toV1 V1toC CtoEnt4 Ent4toStart7" color="yellow" id="L13toTrackDB2"/>

            <route edges="Start9toEnt5 Ent5toE EtoD DtoC CtoB BtoK KtoL LtoN NtoO OtoQ QtoS1 L1_in DummyLink1" color="yellow" id="TrackOC21toL1"/>
            <route edges="Start9toEnt5 Ent5toE EtoD DtoC CtoB BtoK KtoL LtoN NtoO OtoQ QtoS2 L2_in DummyLink2" color="yellow" id="TrackOC21toL2"/>
            <route edges="Start9toEnt5 Ent5toE EtoD DtoC CtoB BtoK KtoL LtoN NtoO OtoP PtoS3 L3_in DummyLink3" color="yellow" id="TrackOC21toL3"/>
            <route edges="Start9toEnt5 Ent5toE EtoD DtoC CtoB BtoK KtoL LtoN NtoO OtoP PtoS4 L4_in DummyLink4" color="yellow" id="TrackOC21toL4"/>
            <route edges="Start9toEnt5 Ent5toE EtoD DtoC CtoB BtoK KtoL LtoM MtoS5 L5_in DummyLink5" color="yellow" id="TrackOC21toL5"/>
            <route edges="Start9toEnt5 Ent5toE EtoD DtoC CtoB BtoK KtoL LtoM MtoS6 L6_in DummyLink6" color="yellow" id="TrackOC21toL6"/>
            <route edges="Start9toEnt5 Ent5toE EtoD DtoC CtoB BtoK KtoZ2 Z2toZ3 Z3toS7 L7_in DummyLink7" color="yellow" id="TrackOC21toL7"/>
            <route edges="Start9toEnt5 Ent5toE EtoD DtoC CtoB BtoK KtoZ2 Z2toZ3 Z3toS8 L8_in DummyLink8" color="yellow" id="TrackOC21toL8"/>
            <route edges="Start9toEnt5 Ent5toE EtoD DtoC CtoB BtoV2 V2toV3 V3toZ ZtoZ4 Z4toS9 L9_in DummyLink9" color="yellow" id="TrackOC21toL9"/>
            <route edges="Start9toEnt5 Ent5toE EtoD DtoC CtoV1 V1toV4 V4toY YtoS10 L10_in DummyLink10" color="yellow" id="TrackOC21toL10"/>
            <route edges="Start9toEnt5 Ent5toE EtoF FtoG GtoH HtoS11 L11_in DummyLink11" color="yellow" id="TrackOC21toL11"/>
            <route edges="Start9toEnt5 Ent5toE EtoF FtoG GtoH HtoJ JtoS12 L12_in DummyLink12" color="yellow" id="TrackOC21toL12"/>
            <route edges="Start9toEnt5 Ent5toE EtoF FtoG GtoH HtoJ JtoS13 L13_in DummyLink13" color="yellow" id="TrackOC21toL13"/>

            <route edges="L1_in L1_out S1toQ QtoO OtoN NtoL LtoK KtoB BtoA AtoW WtoExt3 Ext3toStart5" color="yellow" id="L1toTrack2"/>
            <route edges="L2_in L2_out S2toQ QtoO OtoN NtoL LtoK KtoB BtoA AtoW WtoExt3 Ext3toStart5" color="yellow" id="L2toTrack2"/>
            <route edges="L3_in L3_out S3toP PtoO OtoN NtoL LtoK KtoB BtoA AtoW WtoExt3 Ext3toStart5" color="yellow" id="L3toTrack2"/>
            <route edges="L4_in L4_out S4toP PtoO OtoN NtoL LtoK KtoB BtoA AtoW WtoExt3 Ext3toStart5" color="yellow" id="L4toTrack2"/>
            <route edges="L5_in L5_out S5toM MtoL LtoK KtoB BtoA AtoW WtoExt3 Ext3toStart5" color="yellow" id="L5toTrack2"/>
            <route edges="L6_in L6_out S6toM MtoL LtoK KtoB BtoA AtoW WtoExt3 Ext3toStart5" color="yellow" id="L6toTrack2"/>
            <route edges="L7_in L7_out S7toZ3 Z3toZ2 Z2toK KtoB BtoA AtoW WtoExt3 Ext3toStart5" color="yellow" id="L7toTrack2"/>
            <route edges="L8_in L8_out S8toZ3 Z3toZ2 Z2toK KtoB BtoA AtoW WtoExt3 Ext3toStart5" color="yellow" id="L8toTrack2"/>
            <route edges="L9_in L9_out S9toZ4 Z4toZ ZtoV3 V3toV2 V2toB BtoA AtoW WtoExt3 Ext3toStart5" color="yellow" id="L9toTrack2"/>
            <route edges="L10_in L10_out S10toY YtoV4 V4toV VtoV2 V2toB BtoA AtoW WtoExt3 Ext3toStart5" color="yellow" id="L10toTrack2"/>
            <route edges="L11_in L11_out S11toH HtoG GtoV4 V4toV VtoV2 V2toB BtoA AtoW WtoExt3 Ext3toStart5" color="yellow" id="L11toTrack2"/>
            <route edges="L12_in L12_out S12toJ JtoH HtoG GtoV4 V4toV VtoV2 V2toB BtoA AtoW WtoExt3 Ext3toStart5" color="yellow" id="L12toTrack2"/>
            <route edges="L13_in L13_out S13toJ JtoH HtoG GtoV4 V4toV VtoV2 V2toB BtoA AtoW WtoExt3 Ext3toStart5" color="yellow" id="L13toTrack2"/>

            <route edges="L1_in L1_out S1toQ QtoR RtoT TtoAC2 AC2toStart1" color="yellow" id="L1toTrack7"/>
            <route edges="L2_in L2_out S2toQ QtoR RtoT TtoAC2 AC2toStart1" color="yellow" id="L2toTrack7"/>
            <route edges="L3_in L3_out S3toP PtoO OtoN NtoR RtoT TtoAC2 AC2toStart1" color="yellow" id="L3toTrack7"/>
            <route edges="L4_in L4_out S4toP PtoO OtoN NtoR RtoT TtoAC2 AC2toStart1" color="yellow" id="L4toTrack7"/>
            <route edges="L5_in L5_out S5toM MtoL LtoS StoU UtoAC ACtoAC2 AC2toStart1" color="yellow" id="L5toTrack7"/>
            <route edges="L6_in L6_out S6toM MtoL LtoS StoU UtoAC ACtoAC2 AC2toStart1" color="yellow" id="L6toTrack7"/>
            <route edges="L7_in L7_out S7toZ3 Z3toZ2 Z2toK KtoL LtoS StoU UtoAC ACtoAC2 AC2toStart1" color="yellow" id="L7toTrack7"/>
            <route edges="L8_in L8_out S8toZ3 Z3toZ2 Z2toK KtoL LtoS StoU UtoAC ACtoAC2 AC2toStart1" color="yellow" id="L8toTrack7"/>
            <route edges="L9_in L9_out S9toZ4 Z4toZ ZtoZ2 Z2toK KtoL LtoS StoU UtoAC ACtoAC2 AC2toStart1" color="yellow" id="L9toTrack7"/>
            <route edges="L10_in L10_out S10toY YtoZ4 Z4toZ ZtoZ2 Z2toK KtoL LtoS StoU UtoAC ACtoAC2 AC2toStart1" color="yellow" id="L10toTrack7"/>
            <route edges="L11_in L11_out S11toH HtoG GtoV4 V4toV VtoV2 V2toB BtoK KtoL LtoS StoU UtoAC ACtoAC2 AC2toStart1" color="yellow" id="L11toTrack7"/>
            <route edges="L12_in L12_out S12toJ JtoH HtoG GtoV4 V4toV VtoV2 V2toB BtoK KtoL LtoS StoU UtoAC ACtoAC2 AC2toStart1" color="yellow" id="L12toTrack7"/>
            <route edges="L13_in L13_out S13toJ JtoH HtoG GtoV4 V4toV VtoV2 V2toB BtoK KtoL LtoS StoU UtoAC ACtoAC2 AC2toStart1" color="yellow" id="L13toTrack7"/>

            <route edges="L1_in L1_out S1toQ QtoO OtoN NtoL LtoK KtoB BtoC CtoD DtoStart8" color="yellow" id="L1toTrackOC19"/>
            <route edges="L2_in L2_out S2toQ QtoO OtoN NtoL LtoK KtoB BtoC CtoD DtoStart8" color="yellow" id="L2toTrackOC19"/>
            <route edges="L3_in L3_out S3toP PtoO OtoN NtoL LtoK KtoB BtoC CtoD DtoStart8" color="yellow" id="L3toTrackOC19"/>
            <route edges="L4_in L4_out S4toP PtoO OtoN NtoL LtoK KtoB BtoC CtoD DtoStart8" color="yellow" id="L4toTrackOC19"/>
            <route edges="L5_in L5_out S5toM MtoL LtoK KtoB BtoC CtoD DtoStart8" color="yellow" id="L5toTrackOC19"/>
            <route edges="L6_in L6_out S6toM MtoL LtoK KtoB BtoC CtoD DtoStart8" color="yellow" id="L6toTrackOC19"/>
            <route edges="L7_in L7_out S7toZ3 Z3toZ ZtoV3 V3toV VtoV1 V1toF FtoD DtoStart8" color="yellow" id="L7toTrackOC19"/>
            <route edges="L8_in L8_out S8toZ3 Z3toZ ZtoV3 V3toV VtoV1 V1toF FtoD DtoStart8" color="yellow" id="L8toTrackOC19"/>
            <route edges="L9_in L9_out S9toZ4 Z4toZ ZtoV3 V3toV VtoV1 V1toF FtoD DtoStart8" color="yellow" id="L9toTrackOC19"/>
            <route edges="L10_in L10_out S10toY YtoV4 V4toV1 V1toF FtoD DtoStart8" color="yellow" id="L10toTrackOC19"/>
            <route edges="L11_in L11_out S11toH HtoG GtoF FtoD DtoStart8" color="yellow" id="L11toTrackOC19"/>
            <route edges="L12_in L12_out S12toJ JtoH HtoG GtoF FtoD DtoStart8" color="yellow" id="L12toTrackOC19"/>
            <route edges="L13_in L13_out S13toJ JtoH HtoG GtoF FtoD DtoStart8" color="yellow" id="L13toTrackOC19"/>""", file=routes)

            vehNr = 0

            defaultDict = {'CR-Fairmount':'TrackDB2toL1','CR-Providence':'Track1toL1','CR-Franklin':'Track1toL1', \
                'CR-Middleborough':'TrackOC21toL1','CR-Worcester':'Track5toL1','CR-Needham':'Track5toL1', \
                    'CR-Greenbush':'TrackOC21toL1','CR-Kingston':'TrackOC21toL1','Amtrak':'Track1toL1','Southcoast':'TrackOC21toL1'} 

            defaultYardDict = {'CR-Fairmount':'TrackOC21toL1','CR-Providence':'TrackOC21toL1','CR-Franklin':'TrackOC21toL1', \
                'CR-Middleborough':'TrackOC21toL1','CR-Worcester':'TrackOC21toL1','CR-Needham':'TrackOC21toL1', \
                    'CR-Greenbush':'TrackOC21toL1','CR-Kingston':'TrackOC21toL1','Amtrak':'TrackOC21toL1','Southcoast':'TrackOC21toL1'} 
            
            colorDict = {'CR-Fairmount':'yellow','CR-Providence':'yellow','CR-Franklin':'yellow', \
                'CR-Middleborough':'yellow','CR-Worcester':'yellow','CR-Needham':'yellow', \
                    'CR-Greenbush':'yellow','CR-Kingston':'yellow','Amtrak':'blue','Southcoast':'#51FF06'} 

            df = pd.read_csv(schedule_path)

            arrivals = df[df['Direction'] == 1]
            departures = df[df['Direction'] == 0]
            arrivals['low'] = arrivals['Minutes'] + 15
            arrivals['hi'] = arrivals['Minutes'] + 15

            tmp = arrivals.merge(departures, how='left', on=['Service'], suffixes=('', '_OB')) \
            .query('Minutes_OB.between(`low`, `hi`)')
            
            paired = (
            tmp.assign(
                Minutes_diff = tmp['Minutes_OB'] - tmp['Minutes']
            )
            .sort_values(['Minutes_diff'])
            )

            paired = paired.reset_index()  # make sure indexes pair with number of rows

            unique_ib_list = []
            unique_ob_list = []
            count = 0

            for index, row in paired.iterrows():
                if row['id'] not in unique_ib_list and row['id_OB'] not in unique_ob_list:
                    count +=1
                    unique_ib_list.append(row['id'])
                    unique_ob_list.append(row['id_OB'])
                else:
                    paired.drop(index, inplace=True)

            match_dict = dict(zip(paired.id, paired.id_OB))
            time_dict = dict(zip(paired.id_OB, paired.Minutes_OB))

            with open(schedule_path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(reader)
                sortedlist = sorted(reader, key=lambda row: int(row[3])*60, reverse=False)
                for row in sortedlist:
                    if row[2] == '1':
                        if row[0] in match_dict.keys():
                            print('    <vehicle id="%s_%s" type="CR" route="%s" color="%s" depart="%i" departSpeed="4.4"> <param key="assigned" value="False"/> <param key="next" value="%s"/> <param key="dispatched" value="False"/> <param key="dep_time" value="%i"/>  <param key="greenlit" value="False"/> <param key="loading" value="False"/> <param key="doneloading" value="False"/> <param key="name" value="%s_%s"/> <stop lane="L1_in_0" endPos="185" duration="200"/> </vehicle>' % (row[1], row[0], defaultDict[row[1]], colorDict[row[1]], int(row[3])*60, match_dict[row[0]], time_dict[match_dict[row[0]]]*60, row[1], row[0]),  file=routes)
                        else:
                            print('    <vehicle id="%s_%s" type="CR" route="%s" color="%s" depart="%i" departSpeed="4.4"> <param key="assigned" value="False"/> <param key="next" value="YARD"/> <param key="dispatched" value="False"/> <param key="dep_time" value="0"/>  <param key="greenlit" value="False"/> <param key="loading" value="False"/> <param key="doneloading" value="False"/> <param key="name" value="%s_%s"/> <stop lane="L1_in_0" endPos="185" duration="200"/> </vehicle>' % (row[1], row[0], defaultDict[row[1]], colorDict[row[1]], int(row[3])*60, row[1], row[0]),  file=routes)
                    else:
                        if row[0] not in match_dict.values():
                            print('    <vehicle id="%s_%s" type="CR" route="%s" color="#8FDBFF" depart="%i" departSpeed="4.4"> <param key="assigned" value="False"/><param key="dispatched" value="False"/> <param key="origin" value="YARD"/> <param key="dep_time" value="0"/><param key="greenlit" value="False"/> <param key="loading" value="False"/> <param key="doneloading" value="False"/> <param key="name" value="%s_%s"/> <stop lane="L1_in_0" endPos="185" duration="200"/> </vehicle>' % (row[1], row[0], defaultYardDict[row[1]], int(row[3])*60, row[1], row[0]),  file=routes)
            print("</routes>", file=routes)

            # def yard_departures():
            #     if departure scheduled before any arrivals:
            #         insert departure train from yard
            #     for arrival in set of arrivals:
            #         if there is a scheduled departure greater than 10 minutes less than 20 minutes, assign that departure to that arrival
            #         else, train should go to yard
            #     for all unassigned departures,
            #         come from yard

