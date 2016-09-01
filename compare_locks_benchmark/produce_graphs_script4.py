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

def read_dat_file(the_file):
    with open(the_file, 'r') as f:
        lines = f.readlines()
        x = []
        y = []
        for line in lines:
            p = line.split()
	    if(int(p[0]) != 24):
                x.append(float(p[0]))
                y.append(float(p[2])/float(p[1]))
        return (x, y)

def set_up_figure(title):
    ax_marker = cycle( mystyles )

    plt.figure(figsize=(8,4.75))
    plt.autoscale(enable=True, tight=False)
    plt.xlabel('Number of Threads')
    plt.ylabel('Operations / Microsecond') 
    plt.figtext(0.5, 0.915, title, horizontalalignment='center', verticalalignment='center')
#    plt.title(title)
    return ax_marker


def plot_file(the_file, title, ax_marker):
    (x_list, y_list) = read_dat_file(the_file)
    mapped = [(a, [b for (comp_a, b) in zip(x_list, y_list) if a == comp_a]) for a in x_list]
    mapped.sort()
    x,y_vals = zip(*mapped)
    y = map(lambda v : sum(v) / float(len(v)), y_vals)
    emin = map(lambda (v, avg) : avg - min(v), zip(y_vals, y))
    emax = map(lambda (v, avg) : max(v) - avg, zip(y_vals, y))
    plt.errorbar(x, y, [emin, emax], label=title, linewidth=2, elinewidth=1, marker=ax_marker.next())
    #plt.plot(x, y, label=title, linewidth=2)


def complete_figure(save_file_name):
    plt.axis(xmin=0)
    plt.axis(ymin=0)
    plt.tight_layout()
    plt.legend(loc='best', ncol=1, fontsize=12)
    plt.savefig(save_file_name + '.' + Format, bbox_inches='tight')
    print save_file_name + '.' + Format


m = set_up_figure("90% reads, Local Work=128")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.9_2_4_4_128.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.9_2_4_4_128.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.9_2_4_4_128.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.9_2_4_4_128.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.9_2_4_4_128.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.9_2_4_4_128.dat", "WPRW-Cohort", m)
complete_figure("b_no_09_2_4_4_128")

m = set_up_figure("0% reads, Local Work=0")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.0_2_4_4_0.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.0_2_4_4_0.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.0_2_4_4_0.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.0_2_4_4_0.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.0_2_4_4_0.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.0_2_4_4_0.dat", "WPRW-Cohort", m)
complete_figure("b_no_00_2_4_4_0")

m = set_up_figure("50% reads, Local Work=32")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.5_2_4_4_32.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.5_2_4_4_32.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.5_2_4_4_32.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.5_2_4_4_32.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.5_2_4_4_32.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.5_2_4_4_32.dat", "WPRW-Cohort", m)
complete_figure("b_no_05_2_4_4_32")

m = set_up_figure("99% reads, Local Work=32")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.99_2_4_4_32.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.99_2_4_4_32.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.99_2_4_4_32.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.99_2_4_4_32.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.99_2_4_4_32.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.99_2_4_4_32.dat", "WPRW-Cohort", m)
complete_figure("b_no_099_2_4_4_32")

m = set_up_figure("99% reads, Local Work=0")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.99_2_4_4_0.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.99_2_4_4_0.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.99_2_4_4_0.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.99_2_4_4_0.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.99_2_4_4_0.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.99_2_4_4_0.dat", "WPRW-Cohort", m)
complete_figure("b_no_099_2_4_4_0")

m = set_up_figure("90% reads, Local Work=32")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.9_2_4_4_32.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.9_2_4_4_32.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.9_2_4_4_32.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.9_2_4_4_32.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.9_2_4_4_32.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.9_2_4_4_32.dat", "WPRW-Cohort", m)
complete_figure("b_no_09_2_4_4_32")

m = set_up_figure("0% reads, Local Work=128")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.0_2_4_4_128.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.0_2_4_4_128.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.0_2_4_4_128.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.0_2_4_4_128.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.0_2_4_4_128.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.0_2_4_4_128.dat", "WPRW-Cohort", m)
complete_figure("b_no_00_2_4_4_128")

m = set_up_figure("90% reads, Local Work=0")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.9_2_4_4_0.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.9_2_4_4_0.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.9_2_4_4_0.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.9_2_4_4_0.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.9_2_4_4_0.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.9_2_4_4_0.dat", "WPRW-Cohort", m)
complete_figure("b_no_09_2_4_4_0")

m = set_up_figure("80% reads, Local Work=32")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.8_2_4_4_32.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.8_2_4_4_32.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.8_2_4_4_32.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.8_2_4_4_32.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.8_2_4_4_32.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.8_2_4_4_32.dat", "WPRW-Cohort", m)
complete_figure("b_no_08_2_4_4_32")

m = set_up_figure("50% reads, Local Work=128")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.5_2_4_4_128.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.5_2_4_4_128.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.5_2_4_4_128.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.5_2_4_4_128.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.5_2_4_4_128.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.5_2_4_4_128.dat", "WPRW-Cohort", m)
complete_figure("b_no_05_2_4_4_128")

m = set_up_figure("100% reads, Local Work=0")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_1.0_2_4_4_0.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_1.0_2_4_4_0.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_1.0_2_4_4_0.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_1.0_2_4_4_0.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_1.0_2_4_4_0.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_1.0_2_4_4_0.dat", "WPRW-Cohort", m)
complete_figure("b_no_10_2_4_4_0")

m = set_up_figure("0% reads, Local Work=32")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.0_2_4_4_32.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.0_2_4_4_32.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.0_2_4_4_32.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.0_2_4_4_32.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.0_2_4_4_32.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.0_2_4_4_32.dat", "WPRW-Cohort", m)
complete_figure("b_no_00_2_4_4_32")

m = set_up_figure("50% reads, Local Work=0")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.5_2_4_4_0.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.5_2_4_4_0.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.5_2_4_4_0.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.5_2_4_4_0.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.5_2_4_4_0.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.5_2_4_4_0.dat", "WPRW-Cohort", m)
complete_figure("b_no_05_2_4_4_0")

m = set_up_figure("99% reads, Local Work=128")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.99_2_4_4_128.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.99_2_4_4_128.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.99_2_4_4_128.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.99_2_4_4_128.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.99_2_4_4_128.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.99_2_4_4_128.dat", "WPRW-Cohort", m)
complete_figure("b_no_099_2_4_4_128")

m = set_up_figure("80% reads, Local Work=0")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.8_2_4_4_0.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.8_2_4_4_0.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.8_2_4_4_0.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.8_2_4_4_0.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.8_2_4_4_0.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.8_2_4_4_0.dat", "WPRW-Cohort", m)
complete_figure("b_no_08_2_4_4_0")

m = set_up_figure("100% reads, Local Work=32")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_1.0_2_4_4_32.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_1.0_2_4_4_32.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_1.0_2_4_4_32.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_1.0_2_4_4_32.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_1.0_2_4_4_32.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_1.0_2_4_4_32.dat", "WPRW-Cohort", m)
complete_figure("b_no_10_2_4_4_32")

m = set_up_figure("95% reads, Local Work=0")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.95_2_4_4_0.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.95_2_4_4_0.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.95_2_4_4_0.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.95_2_4_4_0.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.95_2_4_4_0.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.95_2_4_4_0.dat", "WPRW-Cohort", m)
complete_figure("b_no_095_2_4_4_0")

m = set_up_figure("95% reads, Local Work=32")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.95_2_4_4_32.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.95_2_4_4_32.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.95_2_4_4_32.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.95_2_4_4_32.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.95_2_4_4_32.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.95_2_4_4_32.dat", "WPRW-Cohort", m)
complete_figure("b_no_095_2_4_4_32")

m = set_up_figure("95% reads, Local Work=128")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.95_2_4_4_128.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.95_2_4_4_128.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.95_2_4_4_128.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.95_2_4_4_128.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.95_2_4_4_128.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.95_2_4_4_128.dat", "WPRW-Cohort", m)
complete_figure("b_no_095_2_4_4_128")

m = set_up_figure("100% reads, Local Work=128")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_1.0_2_4_4_128.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_1.0_2_4_4_128.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_1.0_2_4_4_128.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_1.0_2_4_4_128.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_1.0_2_4_4_128.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_1.0_2_4_4_128.dat", "WPRW-Cohort", m)
complete_figure("b_no_10_2_4_4_128")

m = set_up_figure("80% reads, Local Work=128")
plot_file("rw_bench_clone_cohort#data_sandy#cohort/b_no_0.8_2_4_4_128.dat", "Cohort", m)
plot_file("rw_bench_clone_drmcs_rgnzi#data_sandy#drmcs_rgnzi/b_no_0.8_2_4_4_128.dat", "DR-MCS", m)
plot_file("rw_bench_clone_rhqdlock_rgnzi#data_sandy#rhqdlock_rgnzi/b_no_0.8_2_4_4_128.dat", "MR-HQD lock", m)
#plot_file("rw_bench_clone_tatasdx#data_sandy#tatasdx/b_no_0.8_2_4_4_128.dat", "QD lock", m)
plot_file("rw_bench_clone_tatasrdx_rgnzi#data_sandy#tatasrdx_rgnzi/b_no_0.8_2_4_4_128.dat", "MR-QD lock", m)
plot_file("rw_bench_clone_wprwcohort_rgnzi#data_sandy#wprwcohort_rgnzi/b_no_0.8_2_4_4_128.dat", "WPRW-Cohort", m)
complete_figure("b_no_08_2_4_4_128")

