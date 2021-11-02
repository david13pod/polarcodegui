import numpy as np
from polarcodes import *
import statistics as st
import time

# System input
msg_len=[180,180,180]
channel='ucl'  # ucl for uplink channel and dcl for downlink channel
desired_rate=[0.16, 0.3, 0.7]
use_ratematching=True #Activate rate matching
sim_time=5000 # number of blocks
List_n = 4 # list size for SCL decoder
design_SNR  = Sim_utils.snr_gen(0,28,0.2)



# myPC = PolarCode(N, M, k, shorten_params)
start_time2 = time.time()

msg_len=msg_len # information length
crc_n=Sim_utils.crc_selector(msg_len,channel) # crc polynomial generator length
k=list(crc_n+np.array(msg_len)) # crc coded information length K
rate=desired_rate # A/E desired system rate
M=(np.array(msg_len)/np.array(rate))  #codeword E = A/R
for ii in range(0,len(msg_len)):
    if k[ii] >= M[ii]:
        raise ValueError(f'crc coded information {k[ii]} can not be greater than the codeword {M[ii]} in length')
M=list(M.astype(int))
N = Sim_utils.mothercode(channel,k,M) # mothercode N
useRM=use_ratematching # Rate matching activator: True To activate rate matching False to deactivate. M == N when rate matching is not used 
if useRM == False:
    M=N  # no rate matching M == N
match_rate=list(np.array(k)/np.array(M)) # match rate K/E
design_SNR  = design_SNR # for bler plot
construction='5g' # construction type
sim_time=sim_time # number of blocks
List_n = List_n # list size for SCL decoder
BER_avged=[]
BLER_list=[]
#time_list=[]
for snr in design_SNR:
    BER=[]
    BLER=[]
    crc_usage_temp=[]
    for i in range(0,len(msg_len)):
        ber_temp = []
        bler_temp=0
        myPC=Sim_utils.matching_scheme_selector(N[i],M[i],k[i],match_rate[i],useRM,snr,construction)
        # print(myPC, "\n\n")
        #time_temp=[]
        #start_time3 = time.time()
            
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
        #time_temp.append(time.time() - start_time3)
        BER.append(float(ber_temp[0]))
        BLER.append(bler_temp/sim_time)

    BER_avged.append(BER)
    BLER_list.append(BLER)
    #time_list.append(time_temp)

print( time.time() - start_time2, "seconds")
# BLER_list

# Plot results
Sim_utils.sim_plot(BLER_list,design_SNR,msg_len,N,rate,match_rate,List_n)
