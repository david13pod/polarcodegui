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

    def __init__(self,msg_len=1,rate=1,use_RM=True,channel='ucl'):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='Message generator',   # will show up in GRC
            # in_sig=[np.int8],
            in_sig=None,
            out_sig=[np.int8]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.msg_len=msg_len
        self.rate=rate
        self.useRM= use_RM
        self.channel=channel

    def general_work(self, input_items, output_items):
        """example: multiply with constant"""
        # print(len(input_items[0]))
        # print((input_items[0].dtype))
        # pprint.pprint((input_items[0]))
        # print(self.msg_len)

        time.sleep(5)
        msg_len=[self.msg_len] # message length

        crc_n=Sim_utils.crc_selector(msg_len,self.channel) # crc polynomial generator length
        k=list(crc_n+np.array(msg_len))
        M=(np.array(msg_len)/np.array(self.rate))  #codeword E = A/R
        self.M=list(M.astype(int))
        N = Sim_utils.mothercode(self.channel,k,M)
        if self.useRM == False:
            self.M=N  # no rate matching M == N
       

        for i in range(0,len(msg_len)):
            my_message = np.random.randint(2, size=msg_len[i],dtype=np.int8)
            zobo = np.zeros(self.M[i])
            
            with open('sim6msg.txt','a') as f:
                f.write(f'{list(my_message)},{N[i]},{self.M[i]},{self.rate}.\n')
                f.close()

            output_items[0][:self.M[i]] = zobo
            output_items[0][:msg_len[i]] = my_message.astype(np.int8)
        
        print((output_items[0][:msg_len[0]]))
        # print((self.M[0]))
        # print((output_items[0][:msg_len]))
        # self.produce(0, msg_len) #consume port 0 input
        
            
        return len(output_items[0][:self.M[0]])
        # return
