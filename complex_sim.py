import numpy as np
from polarcodes import *
from polarcodes import Sim_utils
import statistics as st
import time


start_time2 = time.time()

msg_len=[30] # information length
crc_n=Sim_utils.crc_selector(msg_len,'ucl') # crc polynomial generator length
k=list(crc_n+np.array(msg_len)) # crc coded information length K
N=[128] # mothercode N
M=[100] #codeword E
match_rate=list(np.array(k)/np.array(M)) # K/E
rate=list(np.array(msg_len)/np.array(M)) # A/E
design_SNR  = Sim_utils.snr_gen(-0.2,30,.2)
construction='5g' # construction type
sim_time=10 # number of blocks
useRM=1 # Rate matching activator: 1 To activate rate matching zero to deactivate. M == N when rate matching is not used 
List_n = 4 # list size for SCL decoder
BER_avged=[]
BLER_list=[]
for snr in design_SNR:
    BER=[]
    BLER=[]
    crc_usage_temp=[]
    for i in range(0,len(msg_len)):
        ber_temp = []
        bler_temp=0
        myPC=Sim_utils.matching_scheme_selector(N[i],M[i],k[i],match_rate[i],useRM,snr,construction)
        # print(myPC, "\n\n")
            
        for blk in range(0,sim_time):

            # set message
            my_message = np.random.randint(2, size=msg_len[i])
            myPC.set_message(my_message,crc_n[i])
            # print("The message is:", my_message)

            # encode message
            Encode(myPC)
            # print("The coded message is:", myPC.get_codeword())

            # transmit the codeword and get likelihoods
            AWGN(myPC, snr)
            # print("The log-likelihoods are:", myPC.likelihoods)

            # decode the received codeword
            # decoders: 'scd' and 'SCL'
            # Decode(myPC) #to use scd decoder
            Decode(myPC, list=List_n, decoder_name ='SCL')
            # print("The decoded message is:", myPC.message_received)

            errors=len([w for w in range(len(myPC.message_received))  #sum errors per block
                if myPC.message_received[w] != myPC.message[w] ])
            ber_temp.append(errors / msg_len[i])
            ber_temp=[st.mean(ber_temp)]
            if errors > 0: # cal bler
                bler_temp+=1
        BER.append(float(ber_temp[0]))
        BLER.append(bler_temp/sim_time)

    BER_avged.append(BER)
    BLER_list.append(BLER)

print( time.time() - start_time2, "seconds")
# BLER_list

Sim_utils.sim_plot(BLER_list,design_SNR,msg_len,N,rate,match_rate,List_n)