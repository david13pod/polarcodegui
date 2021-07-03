import numpy as np
from polarcodes.utils import *
from polarcodes.decoder_utils import *


class ListSCD:
    def __init__(self, myPC, List_n,min_sum=True):
        self.myPC = myPC
        self.L = np.full((self.myPC.N, self.myPC.n + 1,1), np.nan, dtype=np.float64)
        self.B = np.full((self.myPC.N, self.myPC.n + 1,1), 0) #Bits container
        lkelihoods_n=len(self.myPC.likelihoods)
        self.likelihoods=myPC.likelihoods.reshape(lkelihoods_n,1) #reshape likelihoods
        self.L[:, 0] = self.likelihoods #LLRS container

        self.approx_minstar=min_sum
        self.PM = np.zeros((1,1,1)) #Path metrics
        self.List_n=List_n
        self.L_prime = 1  #initial list size

    def decode(self):
        """
        A CRC aided SCL Decoder:
        Implemented by combining a SC Decoder created by into a SCL decoder anf adding the CRC functionality. 
        Using CRC SCL Decoder implementation idea from 
        https://github.com/robmaunder/polar-3gpp-matlab/blob/master/components/CA_polar_decoder.m by Rob Maunder
        """

        # decode bits in natural order
        for l in [bit_reversed(i, self.myPC.n) for i in range(self.myPC.N)]:
            # evaluate tree of LLRs for root index i
            self.update_llrs(l)

            # if frozen bits no splitting done
            if l in self.myPC.frozen:
                for i1 in range(self.B.shape[2]): #Ensure all splitted lists are worked on
                    self.B[l, self.myPC.n,i1] = 0 
                self.PM=self.phi(self.PM, self.L[None,l, None,self.myPC.n,:],0) #No splitting, calculate PM

            # if not frozen bits splitting is done
            else:
                #Double the list size, using 0-valued bits for the first half 
                #and 1-valued bits for the other half

                # Path metrics calculatio and splitting 
                self.PM=np.concatenate( (self.phi(self.PM, self.L[None,l, None,self.myPC.n,:],0),
                        self.phi(self.PM, self.L[None,l, None,self.myPC.n,:],1)), axis=2) 
                        # None added to retain dimension
                
                # Splitting llrs and bits matrices 
                self.L = np.concatenate((self.L,self.L),axis=2)
                self.B= np.concatenate((self.B,self.B),axis=2)

                # set bits to 0 on one split and 1 to the other split
                if self.L_prime == 1:
                    self.B[l,self.myPC.n,self.L_prime-1:1] = 0
                    self.B[l,self.myPC.n,self.L_prime:2] = 1
                else:
                    self.B[l,self.myPC.n,0:self.L_prime] = 0
                    self.B[l,self.myPC.n,self.L_prime:(2*self.L_prime)] = 1


                #If the list size has grown above L, then we need to find 
                # and keep only the best L entries (least path metrics) in the list
                
                self.L_prime = self.B.shape[2]  
                self.myPC.L_prime=self.L_prime   
                if self.L_prime > self.List_n:
                    max_indices = np.argsort(self.PM,2)
                    self.PM = self.PM[:,:,max_indices[0,0,0:self.List_n]]
                    self.B = self.B[:,:,max_indices[0,0,0:self.List_n]]
                    self.L = self.L[:,:,max_indices[0,0,0:self.List_n]]
                    self.L_prime = self.List_n

            # propagate the decisions just made
            self.update_bits(l)

        # Information bits extraction 
        # If the CRC doesn't pass then return bits for the least PM.
        max_indices = np.argsort(self.PM,2)
        self.myPC.mylists=[]
        for list_index in max_indices[0,0,:]:
            u_hat = self.B[:,self.myPC.n,list_index].astype(int)

            # Extract the information bits (msg and crc bits)
            decoded_msg = u_hat[self.myPC.frozen_lookup == 1]

            # CRC check
            crc_flag=self.myPC.crc_encode.detection(decoded_msg)[0]
            if crc_flag ==1:
                break
            elif crc_flag ==0 and list_index== max_indices[0,0,-1]:
                u_hat = self.B[:,self.myPC.n,max_indices[0,0,0]].astype(int)
                decoded_msg = u_hat[self.myPC.frozen_lookup == 1]
            
        return decoded_msg


    def update_llrs(self, l):
        for s in range(self.myPC.n - active_llr_level(l, self.myPC.n), self.myPC.n):
            block_size = int(2 ** (s + 1))
            branch_size = int(block_size / 2)
            for j in range(l, self.myPC.N, block_size):
                if j % block_size < branch_size:  # upper branch
                    for i3 in range(self.L.shape[2]): #Ensure all splitted lists are worked on
                        top_llr = self.L[j, s,i3]
                        btm_llr = self.L[j + branch_size, s,i3]
                        self.L[j, s + 1,i3] = upper_llr(top_llr, btm_llr)
                else:  # lower branch
                    for i3 in range(self.L.shape[2]): #Ensure all splitted lists are worked on
                        btm_llr = self.L[j, s,i3]
                        top_llr = self.L[j - branch_size, s,i3]
                        top_bit = self.B[j - branch_size, s + 1,i3]
                        self.L[j, s + 1,i3] = lower_llr(btm_llr, top_llr, top_bit)

    def update_bits(self, l):
        if l < self.myPC.N / 2:
            return

        for s in range(self.myPC.n, self.myPC.n - active_bit_level(l, self.myPC.n), -1):
            block_size = int(2 ** s)
            branch_size = int(block_size / 2)
            for j in range(l, -1, -block_size):
                if j % block_size >= branch_size:  # lower branch
                    for i4 in range(self.B.shape[2]): #Ensure all splitted lists are worked on
                        self.B[j - branch_size, s - 1,i4] = (int(self.B[j, s,i4]) + int(self.B[j - branch_size, s,i4]))%2
                        self.B[j, s - 1,i4] = self.B[j, s,i4]

    def phi(self,PM_ini,L_i,u_i):
        '''
        For Path Metrics calculation
        From Rob Maunder Implementation
        https://github.com/robmaunder/polar-3gpp-matlab/blob/master/components/phi.m
        '''
        if self.approx_minstar:
            # !!! this path metrics is less accurate but faster || to use min_sum = True 
            PM_i=PM_ini.copy()
            shape_ini=PM_i.shape[2]
            if shape_ini == 1:
                # L_i=L_i.reshape(1)
                flags = 0.5*(1-np.sign(L_i)) != u_i
                flags=flags.reshape(shape_ini)
                PM_i[flags]=PM_i[flags]+ abs(L_i)  
            else:    
                flags = 0.5*(1-np.sign(L_i)) != u_i
                for lk in range (shape_ini):
                    if flags[0,0][lk] == False:
                        PM_i=PM_i
                    else:
                        PM_i[0,0][lk]=PM_i[0,0][lk]+ abs(L_i)[0,0][lk]   

            return PM_i 
        else: # !!! this path metrics is more accurate 
            # To use min_sum = False 
            PM_i = PM_ini + np.log(1+np.exp(-(1-2*u_i)*L_i))
            return PM_i 
        
