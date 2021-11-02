"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
from polarcodes import *
from polarcodes import Sim_utils
import pprint
import time
import pmt



class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self,msg_len=1,use_RM=True,rate=1,channel='ucl',snr=1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='Rate_dematcher',   # will show up in GRC
            in_sig=[np.int8],
            # in_sig=[np.float32],
            # in_sig=None,
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.msg_len=msg_len
        self.rate=rate
        self.useRM= use_RM
        self.channel=channel
        self.snr=snr

    # def forecast(self, noutput_items, ninput_items_required):
    #     #setup size of input_items[i] for work call
    #     print("---------- Forecast function --------------")
    #     n_in1 = self.N
    #     print("noutput_items : ", type(ninput_items_required))
    #     n_in2 = self.msg_len
    #     # print(n_in1,"n_in : ",  n_in2)
    #     ninput_items_required. =[1]
    #     # ninput_items_required[1]=n_in2
    #     # print("ninput_items_required[0] : ", ninput_items_required[0])
    #     # # print("noutput_items : ", noutput_items)
    def forecast(self, noutput_items, ninputs):
        """
        forecast is only called from a general block
        this is the default implementation
        """
        # print("---------- Forecast function --------------")
        # print("ooo_items : ", noutput_items)
        # ninput_items_required = [0]*ninputs
        ninput_items_required = [0]*ninputs
        ninput_items_required[0] = 10
        # time.sleep(1)
        return ninput_items_required
    

    def general_work(self, input_items, output_items):
        """example: multiply with constant"""
        time.sleep(1)
        print('2',len(input_items[0]))
        # print(len(input_items[1]))
        # print((input_items[0].dtype))
        # pprint.pprint((input_items[0]))
        # pprint.pprint((input_items[1]))
        msg_len=[self.msg_len] # information length
        # crc_n=Sim_utils.crc_selector(msg_len,'ucl') # crc polynomial generator length
        crc_n=Sim_utils.crc_selector(msg_len,self.channel) # crc polynomial generator length
        k=list(crc_n+np.array(msg_len))
        M=(np.array(msg_len)/np.array(self.rate))  #codeword E = A/R
        M=list(M.astype(int))
        self.M=M
        N = Sim_utils.mothercode(self.channel,k,M)
        if self.useRM == False:
            M=N  # no rate matching M == N
        # print(1)
        match_rate=list(np.array(k)/np.array(M)) # K/E
        # rate=list(np.array(msg_len)/np.array(M)) # A/E
        construction='5g' # construction type
        # sim_time=10000 # number of blocks
        useRM=self.useRM
        snr=self.snr
        # time.sleep(5)
        # print(2)
            

        # def get_likelihoods(y):
        #     Linear_EbNo=10**(snr/10)
        #     for i in range(len(y)):
        #         # s = np.random.normal(0, np.sqrt( (2*Linear_EbNo)), size=1)
        #         # print(s)
        #         # y[i]=2 * (y[i] - 0.5)*np.sqrt(Linear_EbNo) 
        #         # y[i]=1-(2 * y[i] * np.sqrt(Linear_EbNo) )
        #         y[i]=(1-(2 * y[i]))
        #     return y

        for i in range(0,len(msg_len)):
            # time.sleep(2)
            # print(11)
            myPC=Sim_utils.matching_scheme_selector(N[i],self.M[i],k[i],match_rate[i],useRM,snr,construction)
            # print(myPC.frozen)

            # myPC.tx = self.modulation(self.myPC.u)
            # print(myPC.punct_flag)
            # if myPC.punct_flag:
            #     # punctured bit not meant to be sent over the channel
            #     if myPC.punct_type == 'shorten':  #shortening procedure
            #         myPC.rx = input_items[0]
            #         myPC.likelihoods = np.concatenate((np.array(get_likelihoods(myPC.rx), dtype=np.float64),
            #             np.zeros(myPC.s,dtype=np.float64)))
            #         myPC.likelihoods[myPC.source_set_lookup == 0] = np.inf
            #     elif myPC.punct_type == 'punct':  #puncturing procedure
            #         myPC.rx = input_items[0]
            #         myPC.likelihoods = np.concatenate((np.zeros(myPC.s,dtype=np.float64),
            #             np.array(get_likelihoods(myPC.rx), dtype=np.float64)))
            #         myPC.likelihoods[myPC.source_set_lookup == 0] = 0
            #     elif myPC.punct_type == 'rep':   #repetition procedure
            #         myPC.rx = input_items[0]
            #         rep_remover=myPC.rx[0:myPC.N]
            #         for j in range(myPC.N,myPC.M):
            #             index = (j% myPC.N)
            #             rep_remover[index] = rep_remover[index]  + myPC.rx[j]
            #         myPC.rx=rep_remover
            #         myPC.likelihoods = np.array(get_likelihoods(myPC.rx), dtype=np.float64)
                    
            # else:
            #     myPC.rx = input_items[0]
            #     myPC.likelihoods = np.array(get_likelihoods(myPC.rx), dtype=np.float64)

            myPC.rx = input_items[0]
            AWGN(myPC, snr)


            # print(5)
            # print(msg_len,' ',len(myPC.u))
            # output_items[0] = np.ones(256,dtype=np.int0)
            output_items[0][:N[i]] = myPC.likelihoods.astype(np.float64)
            # print('6',len(output_items[0][:N[i]]))
            # print(('6',(output_items[0][:N[i]])))
            # time.sleep(5)
            self.consume(0, len(input_items[0])) #consume port 0 input
            # self.consume(1, N[i]) #consume port 1 input
            
        return len(output_items[0][:N[i]])
        # return len(input_items[0])
