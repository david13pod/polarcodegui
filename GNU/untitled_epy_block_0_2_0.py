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

    def __init__(self,msg_len=1,use_RM=True,rate=1,channel='ucl',list_n=4,snr=1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='Polar Decoder',   # will show up in GRC
            in_sig=[np.float32],
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
        self.list_n=list_n
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
        # print('7',len(input_items[0]))
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
        for i in range(0,len(msg_len)):
            # time.sleep(2)
            # print(np.inf-np.inf)
            myPC=Sim_utils.matching_scheme_selector(N[i],self.M[i],k[i],match_rate[i],useRM,snr,construction)
            # print(myPC.frozen)

            # initiate crc decoder parameters
            dummy=np.random.randint(2, size=msg_len,dtype=np.int8)
            myPC.crc_encode=CRC(dummy,crc_n[i])

            # get decoder input
            myPC.likelihoods=input_items[0]
            myPC.likelihoods=np.array(myPC.likelihoods,dtype=np.float64)
            # pprint.pprint(myPC.likelihoods)

            # Decode
            # Decode(myPC) #to use scd decoder
            Decode(myPC, list=self.list_n, decoder_name ='SCL')
            
            message_received=np.array(myPC.message_received,dtype=np.float32)
            rx_msg=np.array(myPC.message_received,dtype=np.int8)
            with open('sim6dcdmdg.txt','a') as f:
                f.write(f'{snr},{list(rx_msg)}\n')
                f.close()

            print('msg ',message_received)
            
            
            # print(msg_len,' ',len(myPC.u))
            # output_items[0] = np.ones(256,dtype=np.int0)
            output_items[0][:msg_len[i]] = message_received
            # print('8',(output_items[0][:msg_len[i]]))
            # print('7',(output_items[0][:N[i]]))
            # time.sleep(5)
            self.consume(0, len(input_items[0])) #consume port 0 input
            # self.consume(1, N[i]) #consume port 1 input
            
        return len(output_items[0][:msg_len[i]])
        # return len(input_items[0])
