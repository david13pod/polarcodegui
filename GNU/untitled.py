#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.9.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import untitled_epy_block_0 as epy_block_0  # embedded python block
import untitled_epy_block_0_0 as epy_block_0_0  # embedded python block
import untitled_epy_block_0_1 as epy_block_0_1  # embedded python block
import untitled_epy_block_0_1_0 as epy_block_0_1_0  # embedded python block
import untitled_epy_block_0_2 as epy_block_0_2  # embedded python block
import untitled_epy_block_0_2_0 as epy_block_0_2_0  # embedded python block
import untitled_epy_block_0_3 as epy_block_0_3  # embedded python block



from gnuradio import qtgui

class untitled(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "untitled")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.snr = snr = 4
        self.samp_rate = samp_rate = 32000
        self.rate = rate = 0.3
        self.qpsk = qpsk = digital.constellation_bpsk().base()
        self.msg_len = msg_len = 30
        self.channel = channel = 'ucl'
        self.activate_RM = activate_RM = True
        self.List_n = List_n = 4

        ##################################################
        # Blocks
        ##################################################
        self._snr_range = Range(0, 20, 0.5, 4, 200)
        self._snr_win = RangeWidget(self._snr_range, self.set_snr, 'EbNo_dB', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._snr_win)
        self.qtgui_time_sink_x_0_1 = qtgui.time_sink_f(
            msg_len, #size
            50, #samp_rate
            'Polar codes Decoded message', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1.enable_tags(False)
        self.qtgui_time_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1.enable_grid(True)
        self.qtgui_time_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1.enable_stem_plot(False)


        labels = ['decoded msg', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['red', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_1_win)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            msg_len, #size
            50, #samp_rate
            'Input message', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.050)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(False)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Input msg', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.epy_block_0_3 = epy_block_0_3.blk(msg_len=msg_len, use_RM=activate_RM, rate=rate, channel=channel)
        self.epy_block_0_2_0 = epy_block_0_2_0.blk(msg_len=msg_len, use_RM=activate_RM, rate=rate, channel=channel, list_n=List_n, snr=snr)
        self.epy_block_0_2 = epy_block_0_2.blk(msg_len=msg_len, use_RM=activate_RM, rate=rate, channel=channel, snr=snr)
        self.epy_block_0_1_0 = epy_block_0_1_0.blk(msg_len=msg_len, use_RM=activate_RM, rate=rate, channel=channel, snr=snr)
        self.epy_block_0_1 = epy_block_0_1.blk(msg_len=msg_len, use_RM=activate_RM, rate=rate, channel=channel)
        self.epy_block_0_0 = epy_block_0_0.blk(msg_len=msg_len, rate=rate, use_RM=activate_RM, channel=channel)
        self.epy_block_0 = epy_block_0.blk(msg_len=msg_len, use_RM=activate_RM, rate=rate, channel=channel)
        self.digital_constellation_encoder_bc_1 = digital.constellation_encoder_bc(qpsk)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(qpsk)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_float*1, 1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, 2)
        self.blocks_char_to_float_0_1 = blocks.char_to_float(1, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_char_to_float_0_1, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.qtgui_time_sink_x_0_1, 0))
        self.connect((self.blocks_throttle_0, 0), (self.epy_block_0_1_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.epy_block_0_2, 0))
        self.connect((self.digital_constellation_encoder_bc_1, 0), (self.blocks_throttle_0, 0))
        self.connect((self.epy_block_0, 0), (self.epy_block_0_3, 0))
        self.connect((self.epy_block_0_0, 0), (self.blocks_char_to_float_0_1, 0))
        self.connect((self.epy_block_0_0, 0), (self.epy_block_0_1, 0))
        self.connect((self.epy_block_0_1, 0), (self.epy_block_0, 0))
        self.connect((self.epy_block_0_1_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.epy_block_0_2, 0), (self.epy_block_0_2_0, 0))
        self.connect((self.epy_block_0_2_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.epy_block_0_3, 0), (self.digital_constellation_encoder_bc_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "untitled")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        self.epy_block_0_1_0.snr = self.snr
        self.epy_block_0_2.snr = self.snr
        self.epy_block_0_2_0.snr = self.snr

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate
        self.epy_block_0.rate = self.rate
        self.epy_block_0_0.rate = self.rate
        self.epy_block_0_1.rate = self.rate
        self.epy_block_0_1_0.rate = self.rate
        self.epy_block_0_2.rate = self.rate
        self.epy_block_0_2_0.rate = self.rate
        self.epy_block_0_3.rate = self.rate

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_msg_len(self):
        return self.msg_len

    def set_msg_len(self, msg_len):
        self.msg_len = msg_len
        self.epy_block_0.msg_len = self.msg_len
        self.epy_block_0_0.msg_len = self.msg_len
        self.epy_block_0_1.msg_len = self.msg_len
        self.epy_block_0_1_0.msg_len = self.msg_len
        self.epy_block_0_2.msg_len = self.msg_len
        self.epy_block_0_2_0.msg_len = self.msg_len
        self.epy_block_0_3.msg_len = self.msg_len

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        self.epy_block_0.channel = self.channel
        self.epy_block_0_0.channel = self.channel
        self.epy_block_0_1.channel = self.channel
        self.epy_block_0_1_0.channel = self.channel
        self.epy_block_0_2.channel = self.channel
        self.epy_block_0_2_0.channel = self.channel
        self.epy_block_0_3.channel = self.channel

    def get_activate_RM(self):
        return self.activate_RM

    def set_activate_RM(self, activate_RM):
        self.activate_RM = activate_RM

    def get_List_n(self):
        return self.List_n

    def set_List_n(self, List_n):
        self.List_n = List_n
        self.epy_block_0_2_0.list_n = self.List_n




def main(top_block_cls=untitled, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
