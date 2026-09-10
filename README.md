# LFP-instances
Instances for the Line Feed Problem

# Structure of randomly generated instances:

<n_items> <n_periods> <n_bins>

n_items lines :
<hold_cost>  <demand_1> ... <demand_{n_periods}>  <stock0>  <price_item>

<capacity_bin_1> ... <capacity_bin_{n_bins}>

n_items lines, n_bins values each :
<quantity_of_item_in_bin_1> ... <quantity_of_item_in_bin_{n_bins}>

n_items lines, n_bins values each :
<hand_cost_1> ... <hand_cost_{n_bins}>

# Structure of benchmark real-life instances:

<I: number of items> <T: number of periods> <K: number of containers>

<c_i: holding cost of item i * 100> <d_it: demand of i in period t> <s_i0: initial stock of i>
line 1: c_1*100 d_{1,1} d_{1,2} d_{1,3} d_{1,4} d_{1,5} d_{1,6} d_{1,7} s_{1,0}
.
.
.
line 191: c_191 d_{191,1} d_{191,2} d_{191,3} d_{191,4} d_{191,5} d_{191,6} d_{191,7} s_{191,0}

<b_k: handling cost of k * 100> <l_k: number of containers k available>
line 1: b_1*100 l_1
line 2: b_2*100 l_2
line 3: b_3*100 l_3

<q_ik: quantity of item i that goes into container k>
line 1: q_{1,1} q_{1,2} q_{1,3}
.
.
.
line 191: q_{191,1} q_{191,2} q_{191,3}
