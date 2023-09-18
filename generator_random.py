import numpy as np
from utils import import_test_configuration, set_sumo

class TrafficGenerator:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def generate_routefile(self,seed):
        """
        Generation of the route of every train for one episode
        """
        np.random.seed(seed)  # make tests reproducible
        # demand per second from different directions
        pA1 = 1. / 600
        with open("scene/routefile.rou.xml", "w") as routes: #, open("gennedsched.csv","w") as outs:
            # writing = csv.writer(outs, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # outs.truncate()
            print("""<routes>
            <vType id="CR" vClass="rail" accel="0.8" decel="0.8" sigma="0.5" length="80" minGap="8" maxSpeed="4.5" guiShape="rail" carFollowModel="Rail" trainType="ICE1" >
                <param key="carriageLength" value="20"/>
                <param key="carriageGap" value="1"/>
                <param key="locomotiveLength" value="6"/> 
            </vType>
            <route edges="Start2toAB2 AB2toAC ACtoU UtoS StoR RtoQ QtoS1 L1_in DummyLink1" color="yellow" id="Track5toL1"/>
            <route edges="Start2toAB2 AB2toAC ACtoU UtoS StoR RtoN NtoO OtoP PtoS4 L4_in DummyLink4" color="yellow" id="Track5toL4"/>
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
            for i in range(self.start_time, self.end_time - 1200):
                if np.random.uniform(0, 1) < pA1:
                    print(
                        '''
                            <vehicle id="CR-Worcester_%i" type="CR" route="Track5toL1" depart="%i" departSpeed="4.4"> 
                            <param key="assigned" value="False"/> 
                            <param key="dispatched" value="False"/> 
                            <param key="dep_time" value="0"/> 
                            <param key="greenlit" value="False"/> <param key="loading" value="False"/> 
                            <param key="doneloading" value="False"/>
                            <stop lane="L1_in_0" endPos="185" duration="200"/> 
                            </vehicle>
                        '''
                        % (
                        vehNr, i,),  file=routes)
                    # writing.writerow(["%i" % (vehNr),"%i" % (i)])
                    vehNr += 1
                if np.random.uniform(0, 1) < pA1:
                    print(
                        '''
                            <vehicle id="CR-Kingston_%i" type="CR" route="TrackOC21toL1" depart="%i" departSpeed="4.4"> 
                            <param key="assigned" value="False"/> 
                            <param key="dispatched" value="False"/> 
                            <param key="dep_time" value="0"/> 
                            <param key="greenlit" value="False"/> <param key="loading" value="False"/> 
                            <param key="doneloading" value="False"/>
                            <stop lane="L1_in_0" endPos="185" duration="200"/> 
                            </vehicle>
                        '''
                        % (
                        vehNr, i,),  file=routes)
                    # writing.writerow(["%i" % (vehNr),"%i" % (i)])
                    vehNr += 1
            print("</routes>", file=routes)
