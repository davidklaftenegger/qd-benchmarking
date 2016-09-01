#!/usr/bin/python2

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

try:
	Format = FORMAT
except NameError:
	Format = 'pdf'

from itertools import cycle
mystyles = ['o', 'x', 's', 'D', '^', 'v', '<', '>'] #etc
mycolors = ['b', 'g', 'r', 'c', 'm', 'y', '#6699FF', 'k', '#660000', '#99FF66', '#FF6699'] #etc

def read_dat_file(the_file):
    with open(the_file, 'r') as f:
        lines = f.readlines()
        x = []
        y = []
        for line in lines:
            p = line.split()
            x.append(float(p[0]))
            y.append(float(p[2])/float(p[1]))
        return (x, y)

def set_up_figure(title):
    ax_marker = cycle( mystyles )
    colors = cycle( mycolors )
    plt.figure(figsize=(8,4.75))
    plt.autoscale(enable=True, tight=False)
    plt.xlabel('Local Work')
    plt.ylabel('Operations / Microsecond') 
    plt.figtext(0.5, 0.915, title, horizontalalignment='center', verticalalignment='center')
#    plt.title(title)
    return (ax_marker, colors)


def plot_file(the_file, title, ax_marker, line_color, force_color_and_marker = None):
    (x_list, y_list) = read_dat_file(the_file)
    mapped = [(a, [b for (comp_a, b) in zip(x_list, y_list) if a == comp_a]) for a in x_list]
    mapped.sort()
    x,y_vals = zip(*mapped)
    y = map(lambda v : sum(v) / float(len(v)), y_vals)
    emin = map(lambda (v, avg) : avg - min(v), zip(y_vals, y))
    emax = map(lambda (v, avg) : max(v) - avg, zip(y_vals, y))
    if (force_color_and_marker != None):
            color, marker = force_color_and_marker
    else:
            color = line_color.next()
            marker = ax_marker.next()
    plt.errorbar(x, y, [emin, emax], label=title, linewidth=2, elinewidth=1, marker=marker, color=color)
    #plt.plot(x, y, label=title, linewidth=2)


def complete_figure(save_file_name, ymax=12):
    plt.axis(xmin=6)
    plt.axis(ymin=0)
    plt.axis(ymax=ymax)
    plt.tight_layout()
    plt.xscale('log')
    plt.legend(loc='best', ncol=1, fontsize=12)
    plt.savefig(save_file_name + '.' + Format, bbox_inches='tight')
    print save_file_name + '.' + Format


(m,c) = set_up_figure("Priority Queue (64 Threads)")
plot_file("pairing_heap_bench_qdlock#data_sandy#qdlock/xncw_no_64_0.5_2_1_0.dat", "QD lock", m, c)
plot_file("pairing_heap_bench_qdlock_futex#data_sandy#qdlock_futex/xncw_no_64_0.5_2_1_0.dat", "QD (futex)", m, c)
plot_file("pairing_heap_bench_hqdlock#data_sandy#hqdlock/xncw_no_64_0.5_2_1_0.dat", "HQD lock", m, c)
plot_file("pairing_heap_bench_flatcomb#data_sandy#flatcomb/xncw_no_64_0.5_2_1_0.dat", "FC", m, c)
plot_file("pairing_heap_bench_ccsynch#data_sandy#ccsynch/xncw_no_64_0.5_2_1_0.dat", "CC-Synch", m, c)
plot_file("pairing_heap_bench_hsynch#data_sandy#hsynch/xncw_no_64_0.5_2_1_0.dat", "H-Synch", m, c)
#plot_file("pairing_heap_bench_cohortlock#data_sandy#cohortlock/xncw_no_64_0.5_2_1_0.dat", "Cohort", m, c)
#plot_file("pairing_heap_bench_oyama#data_sandy#oyama/xncw_no_64_0.5_2_1_0.dat", "Oyama", m, c)
plot_file("pairing_heap_bench_oyamaopt#data_sandy#oyamaopt/xncw_no_64_0.5_2_1_0.dat", "DetachExec", m, c)
#plot_file("pairing_heap_bench_lf#data_sandy#lf/xncw_no_64_0.5_2_1_0.dat", "Lock-free", m, c)
complete_figure("pairingheap_lwperformance_all")

(m,c) = set_up_figure("Priority Queue (64 Threads)")
plot_file("pairing_heap_bench_hqdlock#data_sandy#hqdlock/xncw_no_64_0.5_2_1_0.dat", "HQD", m, c)
plot_file("pairing_heap_bench_hqdlock_nostarve#data_sandy#hqdlock_nostarve/xncw_no_64_0.5_2_1_0.dat", "HQD (nostarve)", m, c)
#m.next();
#c.next();
plot_file("pairing_heap_bench_cashqdlock#data_sandy#cashqdlock/xncw_no_64_0.5_2_1_0.dat", "HQD (CAS)", m, c)
plot_file("pairing_heap_bench_nodhqdlock#data_sandy#nodhqdlock/xncw_no_64_0.5_2_1_0.dat", "HQD (nodetach)", m, c)
#plot_file("pairing_heap_bench_padhqdlock#data_sandy#padhqdlock/xncw_no_64_0.5_2_1_0.dat", "HQD (padded)", m, c)
#plot_file("pairing_heap_bench_padnodhqdlock#data_sandy#padnodhqdlock/xncw_no_64_0.5_2_1_0.dat", "HQD (nodet/pad)", m, c)
complete_figure("pairingheap_lwperformance_hqd")

(m,c) = set_up_figure("Priority Queue (64 Threads)")
plot_file("pairing_heap_bench_qdlock#data_sandy#qdlock/xncw_no_64_0.5_2_1_0.dat", "QD", m, c)
plot_file("pairing_heap_bench_qdlock_futex#data_sandy#qdlock_futex/xncw_no_64_0.5_2_1_0.dat", "QD (futex)", m, c)
plot_file("pairing_heap_bench_qdlock_nostarve#data_sandy#qdlock_nostarve/xncw_no_64_0.5_2_1_0.dat", "QD (nostarve)", m, c)
#for i in range(1, 5):
#        m.next()
#        c.next()
plot_file("pairing_heap_bench_casqdlock#data_sandy#casqdlock/xncw_no_64_0.5_2_1_0.dat", "QD (CAS)", m, c)
plot_file("pairing_heap_bench_nodqdlock#data_sandy#nodqdlock/xncw_no_64_0.5_2_1_0.dat", "QD (nodetach)", m, c)
#plot_file("pairing_heap_bench_padqdlock#data_sandy#padqdlock/xncw_no_64_0.5_2_1_0.dat", "QD (padded)", m, c)
#plot_file("pairing_heap_bench_padnodqdlock#data_sandy#padnodqdlock/xncw_no_64_0.5_2_1_0.dat", "QD (nodet/pad)", m, c)
complete_figure("pairingheap_lwperformance_qd", ymax=12)
