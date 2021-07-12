#!/usr/bin/env python

"""
This class simulates an AWGN channel by adding gaussian noise with double-sided noise power.
It updates ``likelihoods`` in `PolarCode` with randomly generated log-likelihood ratios
for ``u`` in `PolarCode`. For puncturing, the likelihoods for the punctured bits given by
``source_set_lookup`` in `PolarCode` will be set to zero. For shortening,
these likelihoods will be set to infinity. Currently only BPSK modulation is supported.
"""

import matplotlib.pyplot as plt
import numpy as np


class AWGN:
    def __init__(self, myPC, Eb_No, plot_noise=False):
        """
        Parameters
        ----------
        myPC: `PolarCode`
            a polar code object created using the `PolarCode` class
        Eb_No: float
            the design SNR in decibels
        plot_noise: bool
            a flag to view the modeled noise

        """

        self.myPC = myPC
        self.Eb_No_dB = Eb_No
        self.coderate = myPC.message.size/myPC.M
        self.Es = myPC.get_normalised_SNR(Eb_No)
        self.No = 1
        self.plot_noise = plot_noise

        self.myPC.tx = self.modulation(self.myPC.u)

        if self.myPC.punct_flag:
            # punctured bit not meant to be sent over the channel
            if self.myPC.punct_type == 'shorten':  #shortening procedure
                self.myPC.rx = self.myPC.tx[0:self.myPC.M] + self.noise(self.myPC.M)
                self.myPC.likelihoods = np.concatenate((np.array(
                    self.get_likelihoods(self.myPC.rx), dtype=np.float64),
                    np.zeros(self.myPC.s,dtype=np.float64)))
                self.myPC.likelihoods[self.myPC.source_set_lookup == 0] = np.inf
            elif self.myPC.punct_type == 'punct':  #puncturing procedure
                self.myPC.rx = self.myPC.tx[self.myPC.s:self.myPC.N] + self.noise(self.myPC.M)
                self.myPC.likelihoods = np.concatenate((np.zeros(self.myPC.s,dtype=np.float64),
                    np.array(self.get_likelihoods(self.myPC.rx), dtype=np.float64)))
                self.myPC.likelihoods[self.myPC.source_set_lookup == 0] = 0
            elif self.myPC.punct_type == 'rep':   #repetition procedure
                match_position= np.array(range(0,self.myPC.M))% self.myPC.N 
                self.myPC.tx=self.myPC.tx[match_position]
                self.myPC.rx = self.myPC.tx + self.noise(self.myPC.M)
                rep_remover=self.myPC.rx[0:self.myPC.N]
                for j in range(self.myPC.N,self.myPC.M):
                    index = (j% self.myPC.N)
                    rep_remover[index] = rep_remover[index]  + self.myPC.rx[j]
                self.myPC.rx=rep_remover
                self.myPC.likelihoods = np.array(
                    self.get_likelihoods(self.myPC.rx), dtype=np.float64)
                
        else:
            self.myPC.rx = self.myPC.tx + self.noise(self.myPC.N)
            self.myPC.likelihoods = np.array(
                self.get_likelihoods(self.myPC.rx), dtype=np.float64)

    def LLR(self, y):
        """
        > Finds the log-likelihood ratio of a received signal.
        LLR = Pr(y=0)/Pr(y=1).

        Parameters
        ----------
        y: float
            a received signal from a gaussian-distributed channel

        Returns
        ----------
        float
            log-likelihood ratio for the input signal ``y``

        """
        
        Linear_EbNo=10**(self.Eb_No_dB/10)
        return -2 * y * np.sqrt(Linear_EbNo) / self.No
       

    def get_likelihoods(self, y):
        """
        Finds the log-likelihood ratio of an ensemble of received signals using :func:`LLR`.

        Parameters
        ----------
        y: ndarray<float>
            an ensemble of received signals

        Returns
        ----------
        ndarray<float>
            log-likelihood ratios for the input signals ``y``

        """
        return [self.LLR(y[i]) for i in range(len(y))]

    def modulation(self, x):
        """
        BPSK modulation for a bit field.
        "1" maps to +sqrt(E_s) and "0" maps to -sqrt(E_s).

        Parameters
        ----------
        x: ndarray<int>
            an ensemble of information to send

        Returns
        ----------
        ndarray<float>
            modulated signal with the information from ``x``

        """

        Linear_EbNo=10**(self.Eb_No_dB/10)
        return 2 * (x - 0.5)*np.sqrt(Linear_EbNo) 

    def noise(self, N):
        """
        Generate gaussian noise with a specified noise power.
        For a noise power N_o, the double-side noise power is N_o/2.

        Parameters
        ----------
        N: float
            the noise power

        Returns
        ----------
        ndarray<float>
            white gaussian noise vector

        """
        #Eb_No
        Linear_EbNo=10**(-self.Eb_No_dB/10)
        s = np.random.normal(0, np.sqrt( (2*Linear_EbNo)), size=N)

        # SNR
        # Linear_EbNo=10**(-self.Eb_No_dB/10)
        # s = np.random.normal(0, np.sqrt((2*Linear_EbNo*self.coderate)), size=N)

        # eliminate channel effect
        # s=np.zeros(N)

        # original noise
        # s = np.random.normal(0, np.sqrt(self.No / 2), size=N)


        # display RNG values with ideal gaussian pdf
        if self.plot_noise:
            num_bins = 1000
            count, bins, ignored = plt.hist(s, num_bins, density=True)
            plt.plot(bins, 1 / (np.sqrt(np.pi * self.No)) * np.exp(- (bins) ** 2 / self.No),
                     linewidth=2, color='r')
            plt.title('AWGN')
            plt.xlabel('Noise, n')
            plt.ylabel('Density')
            plt.legend(['Theoretical', 'RNG'])
            plt.draw()
        return s

    def show_noise(self):
        """
        Trigger showing the gaussian noise. Only works if ``plot_noise`` is True.
        """
        plt.show()
