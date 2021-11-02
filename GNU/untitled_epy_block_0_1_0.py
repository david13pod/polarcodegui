"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

from tkinter.constants import S
import numpy as np
from gnuradio import gr
from polarcodes import *
from polarcodes import Sim_utils
import pprint
import time
import pmt


class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self,msg_len=1,use_RM=True,rate=1,channel='ucl',snr=5):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='Noise',   # will show up in GRC
            in_sig=[np.complex64],
            # in_sig=None,
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.msg_len=msg_len
        self.rate=rate
        self.useRM= use_RM
        self.channel=channel
        self.snr=snr

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
        # print("ninput_itemsreq : ", ninput_items_required)
        # for i in range(ninputs):
        #     ninput_items_required[i] = 200
        # print("ninput_itemsreq : ", ninput_items_required)
        # time.sleep(1)
        return ninput_items_required
    
    # noutput_items=200
    # ninput_items=200
    def general_work(self, input_items, output_items):
        """example: multiply with constant"""
        # self.forecast(1,1)
        # print('1',len(output_items[0]))
        # print('tx',len(input_items[0]))
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
        snr=self.snr
        # time.sleep(5)
        # print(2)
        for i in range(0,len(msg_len)):
            # time.sleep(2)
            # print(2)
            tx_len = len(input_items[0])
            tx=input_items[0]
            Linear_EbNo=10**(-snr/10)
            noise = np.random.normal(0, np.sqrt(2*Linear_EbNo)/2, size=(tx_len,2)).view(np.complex128)
            noise= noise.flatten()
            rx=tx+noise

            output_items[0][:tx_len] = rx
            print('3',len(output_items[0][:tx_len]))
            # print('4',(output_items[0][:k[i]]))
            # time.sleep(5)
            self.consume(0, len(input_items[0])) #consume port 0 input
            # self.consume(1, N[i]) #consume port 1 input
            
        return len(output_items[0][:tx_len])
        # return len(input_items[0])
