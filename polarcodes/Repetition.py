import numpy as np
from polarcodes.utils import *
from polarcodes.Construct import Construct

class Repetition(Construct):
    def __init__(self, myPC, design_SNR, manual=False):
        """
        In the future, this class will contain common Repetition algorithms.

        Parameters
        ----------
        myPC: `PolarCode`
        design_SNR: float
        manual: bool
        """

        super().__init__(myPC, design_SNR, True)
        if manual:
            return
        else:
            self.update_spcc(myPC, design_SNR)

    def update_spcc(self, myPC, design_SNR):
        #  Puncturing according to Valerio Bioglio: 'Design of Polar Codes in 5G New Radio'
        self.update_mpcc(myPC, design_SNR)

        myPC.punct_set = self.repeat_pattern(myPC)
        myPC.source_set = myPC.punct_set
       
       
        myPC.punct_set_lookup = myPC.get_lut(myPC.punct_set)
        myPC.source_set_lookup = myPC.get_lut(myPC.source_set)
        
        
        # myPC.frozen = self.frozen_from_pattern(myPC)
        myPC.frozen = myPC.frozen
        myPC.frozen_lookup = myPC.get_lut(myPC.frozen)
        if myPC.construction_type != '5g':
            myPC.FERestimate = self.FER_estimate(myPC.frozen, myPC.z)

    def repeat_pattern(self, myPC):
        """
        #  Repetition according to Valerio Bioglio: 'Design of Polar Codes in 5G New Radio'

        Parameters
        ----------
        myPC: `PolarCode`
            a polar code object created using the :class:`PolarCode` class

        Returns
        ----------
        ndarray<int>
            Puncturing set

        -------------
        **References:**
        Valerio Bioglio: 'Design of Polar Codes in 5G New Radio'
        """

        # punct_set = np.array(range(0, -myPC.s))
        punct_set = myPC.reliabilities[0:-myPC.s]
        return punct_set

    # gives same result as repeat_pattern()
    def frozen_pattern_5g(self, myPC):
        """
        selection of frozen pattern from reliability sequence according 
        to the rate matching scheme
        Prefreezing Q1
        Extra Freezing Q2
        Reliability Freezing Q3

        source: 'Design of Polar Codes in 5G New Radio'
        Valerio Bioglio, Member, IEEE, Carlo Condo, Member, IEEE, Ingmar Land, Senior Member, IEEE

        """

        Q1=myPC.reliabilities[:len(myPC.source_set)]
        if myPC.M >= myPC.N*3/4:
            T=((myPC.N*3/4) - (myPC.M/2)) -1
        else:
            T=((myPC.N*9/16) - (myPC.M/4)) -1
        Q2=myPC.reliabilities[:T]
        if len(Q1) > len(Q2):
            Q4=Q1
        elif len(Q1) < len(Q2):
            Q4=Q2
        elif len(Q1) == len(Q2):
            Q4=Q1
        
        R_m = []
        for i in range(myPC.N):    # add elements from R not in punct_set to R_m
            if myPC.reliabilities[i] not in Q4:
                R_m.append(myPC.reliabilities[i])
        Q3 = myPC.N - myPC.K -len(Q4)  # number of frozen bits left to select
        frozen = np.array(np.append(np.array(R_m[:Q3]), Q4))   # first t bits of R_m, then append S
        return frozen