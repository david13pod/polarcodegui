import numpy as np
from polarcodes import *
from polarcodes.Repetition import Repetition
import matplotlib.pyplot as plt  


#Auxilary functions

def data_transform(output_ber):
    ''' 
    simulation result cleaning and transformation 
    '''
    avgd_ber=[]
    counter=0
    for f in range(0,len(output_ber[0])):
        avgd_ber_temp=[]
        for s in output_ber:
            avgd_ber_temp.append(s[counter])
        avgd_ber.append(avgd_ber_temp)
        counter+=1
    return avgd_ber

def snr_gen(start_snr,snr_count,snr_intrv):
    '''
    SNR generating function
    '''
    temp_snr=[]
    for xz in range(0,snr_count):
        start_snr+=snr_intrv
        temp_snr.append(np.round(start_snr,1))
    return list(temp_snr)


def crc_selector(A,mode):
    '''
    Automatic selection of CRC polynomial 
    '''
    crcn=[]
    for k in range(len(A)):
        if (A[k] > 20) and mode =='ucl':
            crcn.append(11)
        elif (A [k]> 12 or A[k] <=19) and mode=='ucl':
            crcn.append(6)
        elif (A[k] >= 12 ) and (mode=='dcl' or mode== 'pay'):
            crcn.append(24)
    return crcn

def mothercode(channel,k,M):
    #implementation of mothercode length
    N=[]
    nmin=5
    for i in range(0,len(k)):
        n1=np.log2(M[i])
        n2=np.log2(8*k[i])
        if channel =='dcl':
            nmax=9
            n=max(min(n1,n2,nmax),nmin)
            N.append(2**int(np.ceil(n)))
        else:
            nmax=10
            n=max(min(n1,n2,nmax),nmin)
            N.append(2**int(np.ceil(n)))
    return N

def matching_scheme_selector(N,M,k,match_rate,useRM,snr,construction):
    if M==N and useRM==False: #no rate matching used
        myPC = PolarCode(N,M, k)
        myPC.construction_type = construction
        Construct(myPC, snr)
        return myPC
    elif M <= N and match_rate > (7/16) and useRM==True: #shortening
        params = ('shorten', 'fiveG_shortnening', None, None, False)
        myPC = PolarCode(N,M, k, params)
        myPC.construction_type = construction
        Shorten(myPC, snr)
        return myPC
    elif M <= N and match_rate <= (7/16) and useRM==True: #puncturing
        params = ('punct', None, None, None, False)
        myPC = PolarCode(N,M, k, params)
        myPC.construction_type = construction
        Puncture(myPC, snr)
        return myPC
    elif M > N and useRM==True: #repetition
        params = ('rep', None, None, None, False)
        myPC = PolarCode(N,M, k, params)
        myPC.construction_type = construction
        Repetition(myPC, snr)
        # Repetition(myPC, design_SNR)
        return myPC
    else:
        raise 'Check your rate matching activator, mothercode N and codeword length M '
        
def sim_plot(BLER_list,design_SNR,msg_len,N,rate,match_rate,List_n):
    blertx=data_transform(BLER_list)

    fig, ax = plt.subplots(figsize=(11,7))
    for kk in range(0,len(blertx)):
    # for kk in [0,1,3,5]:
        plt.plot(design_SNR,blertx[kk], label='rate ='+str(round(rate[kk],2))+' , '+"msg_len ="
        +str(msg_len[kk])+ ' , '+"N =" +str(N[kk])+", L =List_n")

    #plt.axis([0, 20, 0, 3.0e-1])
    plt.xscale('linear')
    plt.yscale('log')
    fig.suptitle('EbNo vs BLER ')
    plt.ylim(5e-4, 2e0)
    plt.xlim(-2, 6)
    plt.xlabel('EbNo')
    plt.ylabel('BLER')
    plt.legend(loc='best')
    plt.figtext(.51, .9, "L = "+str(List_n))
    plt.figtext(.2, .85, "rate matching scheme: Repetition: E>N, Punctuting E<N and R<0.438, Shortening E<N and R>0.438")
    #plt.figtext(.51, .9, "rates: Rep<0.273<Punct<0.378<Short, L = "+str(List_n))
    plt.grid(True,which="both")
    plt.show()
    #fig.savefig('EbNo_vs_BLER_Compx_rateL8.jpg', bbox_inches='tight')
    # fig.savefig('EbNo_vs_BLER_Comp_5g.jpg', bbox_inches='tight')