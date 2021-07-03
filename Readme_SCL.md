<strong>Repo cloned from https://github.com/mcba1n/polar-codes</strong>

Project focuses on implementing CRC aiaded SCL decoder and Rate Matching schemes.

README.md instructions still applies for most part of the project.

<br>
Added modeules to the project:

<li>ListSCD.py</li>
<li>Repetition.py</li>
<li>complex_sim.py</li>
<li>Sim_utils.py</li>

<br><br>
Added Methods to the project:

<li>get_polar_5g_positions Method in Construct Class</li>
<li>__init__ Method in ListSCD Class</li>
<li>decode Method in ListSCD Class</li>
<li>phi Method in ListSCD Class</li>
<li>puncture_pattern Method in Puncture Class</li>
<li>frozen_pattern_5g Method in Puncture Class</li>
<li>repeat_pattern Method in Puncture Class</li>
<li>frozen_pattern_5g Method in Puncture Class</li>
<li>fiveG_shortnening Method in Shorten Class</li>
<li>frozen_pattern_5g Method in Shorten Class</li>
<li>__init__ Method in CRC Class</li>
<li>data_transform function in Sim_utils</li>
<li>snr_gen function in Sim_utils</li>
<li>crc_selector function in Sim_utils</li>
<li>matching_scheme_selector function in Sim_utils</li>
<li>sim_plot function in Sim_utils</li>

<br><br>
Existing Methods edited in the project:

<li>AWGN: __init__ method</li>
<li>AWGN: noise method</li>
<li>Construct: update_mpcc</li>
<li>Decode: __init__ method</li>
<li>PolarCode: __init__ method</li>
<li>PolarCode: initialise_code method</li>
<li>PolarCode: set_message method</li>
<li>Puncture: update_spcc method</li>
<li>Repetition: update_spcc method</li>
<li>Shorten: update_spcc method</li>

<br><br>
To simulate, edit and run the <strong>complex_sim.py</strong> file or <strong>complex_sim.ipynb</strong> file for interactive simulation