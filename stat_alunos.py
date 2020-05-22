"""
stat_2016_alunos.py
Descriptive and inferential statistics in Python.
Use numpy, scipy and matplotlib.
"""
__author__ = 'Ernesto Costa'
__date__ = 'March 2015, March 2016'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

# obtain data
def get_data(filename):
    data = np.loadtxt(filename)
    # print(data)
    return data

def get_data_MP(folder):
    """
    Load data of the algorithm Multiple populations
    """
    f1 = open(folder + "best_data.txt", "r")
    f2 = open(folder + "best2_data.txt", "r")
    data = []
    f1 = f1.readlines()
    f2 = f2.readlines()
    for i in range(len(f1) ):
        gen, avg, std = f1[i].split(" ")
        gen2, avg2, std2 = f2[i].split(" ")

        if avg > avg2:
            data.append(float(avg))
        else:
            data.append(float(avg2))
    return data

def get_data_RI(filename):
    """
    Load data of the algorithm Random Immigrants
    """
    f = open(filename, "r")
    data = []
    for line in f.readlines():
        gen, avg, std = line.split(" ")
        data.append(float(avg))
    return data

def get_data3(filename):
    f = open(filename, "r")
    data = []
    for line in f.readlines():
        gen, fitness = line.split(",")
        if int(gen) == 0:
            data.append(float(fitness))
    return data

def get_data_many(filename):
    data_raw = np.loadtxt(filename)
    data = data_raw.transpose()
    #print(data)
    return data

# describing data

def describe_data(data):
    """ data is a numpy array of values"""
    min_ = np.amin(data)
    max_ = np.amax(data)
    mean_ = np.mean(data)
    median_ = np.median(data)
    mode_ = st.mode(data)
    std_ = np.std(data)
    var_ = np.var(data)
    skew_ = st.skew(data)
    kurtosis_ = st.kurtosis(data)
    q_25, q_50, q_75 = np.percentile(data, [25,50,75])
    basic = 'Min: %s\nMax: %s\nMean: %s\nMedian: %s\nMode: %s\nVar: %s\nStd: %s'
    other = '\nSkew: %s\nKurtosis: %s\nQ25: %s\nQ50: %s\nQ75: %s'
    all_ = basic + other
    print(all_ % (min_,max_,mean_,median_,mode_,var_,std_,skew_,kurtosis_,q_25,q_50,q_75))
    return (min_,max_,mean_,median_,mode_,var_,std_,skew_,kurtosis_,q_25,q_50,q_75)

# visualizing data
def histogram(data,title,xlabel,ylabel,bins=25):
    plt.hist(data,bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    
def histogram_norm(data,title,xlabel,ylabel,bins=20):
    plt.hist(data,normed=1,bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    min_,max_,mean_,median_,mode_,var_,std_,*X = describe_data(data)
    x = np.linspace(min_,max_,1000)
    pdf = st.norm.pdf(x,mean_,std_)
    plt.plot(x,pdf,'r')    
    plt.show()

def box_plot_color(data, labels):
    bp = plt.boxplot(data,labels=labels, patch_artist=True)
    i = 0
    j = 3
    colors = ['whitesmoke','lightgrey','darkgray', 'dimgrey']
    for b in bp['boxes']:
        # if i == len(colors):
        #     i = 0
        b.set_facecolor(colors[i])
        j -= 1
        if j == 0:
            i += 1
            j = 3
    plt.show()

def box_plot(data, labels):
    bp = plt.boxplot(data,labels=labels)
    plt.show()

# Parametric??
def test_normal_ks(data):
    """Kolgomorov-Smirnov"""
    norm_data = (data - np.mean(data))/(np.std(data)/np.sqrt(len(data)))
    return st.kstest(norm_data,'norm')

def test_normal_sw(data):
    """Shapiro-Wilk"""
    norm_data = (data - np.mean(data))/(np.std(data)/np.sqrt(len(data)))
    return st.shapiro(norm_data)

def levene(data):
    """Test of equal variance. H0 = same variance.
    @W: thev test statistics
    @pval: the p-value
    """
    W,pval = st.levene(*data)
    return(W,pval)

# hypothesis testing
# Parametric
def t_test_ind(data1,data2, eq_var=True):
    """
    parametric
    two samples
    independent
    """
    t,pval = st.ttest_ind(data1,data2, equal_var=eq_var)
    return (t,pval)

def t_test_dep(data1,data2):
    """
    parametric
    two samples
    dependent
    """
    t,pval = st.ttest_rel(data1,data2)
    return (t,pval)

def one_way_ind_anova(data):
    """
    parametric
    many samples
    independent
    """
    F,pval = st.f_oneway(*data)
    return (F,pval)


# Non Parametric
def mann_whitney(data1,data2):
    """
    non parametric
    two samples
    independent
    """
    return st.mannwhitneyu(data1, data2)

def wilcoxon(data1,data2):
    """
    non parametric
    two samples
    dependent
    """     
    return st.wilcoxon(data1,data2)

def kruskal_wallis(data):
    """
    non parametric
    many samples
    independent
    """     
    H,pval = st.kruskal(*data)
    return (H,pval)

def friedman_chi(data):
    """
    non parametric
    many samples
    dependent
    """     
    F, pval = st.friedmanchisquare(*data)
    return (F,pval)    
    
# Effect size
def effect_size_t(stat,df):
    r = np.sqrt(stat**2/(stat**2 + df))
    return r

def effect_size_mw(stat,n1,n2):
    """
    n1: size of the first sample
    n2: size of the second sample
    n_ob: number of observations
    """
    n_ob = n1 + n2 
    mean = n1*n2/2
    std = np.sqrt(n1*n2*(n1+n2+1)/12)
    z_score = (stat - mean)/std
    # print(z_score)
    return z_score,z_score/np.sqrt(n_ob)

def effect_size_wx(stat,n, n_ob):
    """
    n: size of effective sample (zero differences are excluded!)
    n_ob: number of observations = size sample 1 + size sample 2
    """
    mean = n*(n+1)/4
    std = np.sqrt(n*(n+1)*(2*n+1)/24)
    z_score = (stat - mean)/std
    return z_score/np.sqrt(n_ob)




def ks_test(a,b):
    for data in a:
        _, pvalue = test_normal_ks(data)
        if pvalue < 0.05:
            print("Rejeita a Hipotese Nula")
        else:
            print("O teste falha em rejeitar a Hipotese Nula")
    for data in b:
        _, pvalue = test_normal_ks(data)
        if pvalue < 0.05:
            print("Rejeita a Hipotese Nula")
        else:
            print("O teste falha em rejeitar a Hipotese Nula")

def kw_test(a,b):
    H,pvalue = (kruskal_wallis(a))
    if pvalue < 0.05:
            print("Rejeita a Hipotese Nula")
    else:
        print("O teste falha em rejeitar a Hipotese Nula")
    H,pvalue = kruskal_wallis(b)
    if pvalue < 0.05:
            print("Rejeita a Hipotese Nula")
    else:
        print("O teste falha em rejeitar a Hipotese Nula")

def mw_test(a,b):
    f = open("file2.csv","w")
    for aa in a:
        line = ""
        for bb in b:
            media_a = np.mean(aa)
            media_b = np.mean(bb)
            print("media A: %f    media B: %f" % (media_a, media_b))
            U,pvalue = mann_whitney(aa, bb)
            print("U: %.2f" % U)
            print("Pvalue: %f" % pvalue)
            # correcao bonferroni
            print("Pvalue: %f" % (pvalue/2))
            z_score, r = effect_size_mw(U, len(bb), len(aa))
            print("Effect Size: %f" % r)
            # box_plot([aa,bb], ["A","B"])
            if abs(r) <= 0.1:
                line = line + "," + "~"
            elif abs(r) > 0.1 and abs(r) <= 0.3:
                if media_a < media_b:
                    line = line + "," + "-"
                else:
                    line = line + "," + "+"
            elif abs(r) > 0.3 and abs(r) <= 0.5:
                if media_a < media_b:
                    line = line + "," + "- -"
                else:
                    line = line + "," + "+ +"
            elif abs(r) > 0.5 and abs(r) <= 1:
                if media_a < media_b:
                    line = line + "," + "- - -"
                else:
                    line = line + "," + "+ + +"
            else:
                line = line + ",err"

            # input()
            # line = line + "," + str(r) 
        line = line + "\n"
        f.write(line)
    f.close()

def main(a,b):

    ks_test(a,b)
    kw_test(a,b)
    mw_test(a,b)


if __name__ == '__main__':
    # use the function get_data_MP to load data from Multiple population algorithm
    # use the function get_data_RI to load data from Random Immigrants algorithm



    a_5_1_w = get_data_MP("save/A/dataset1/0.05_smp_worst/")
    a_5_1_b = get_data_MP("save/A/dataset1/0.05_smp_best/")
    a_5_1_r = get_data_MP("save/A/dataset1/0.05_smp_random/")
    a_5_2_w = get_data_MP("save/A/dataset1/0.05_par_worst/")
    a_5_2_b = get_data_MP("save/A/dataset1/0.05_par_best/")
    a_5_2_r = get_data_MP("save/A/dataset1/0.05_par_random/")
    a_5_5_w = get_data_MP("save/A/dataset1/0.05_5_worst/")
    a_5_5_b = get_data_MP("save/A/dataset1/0.05_5_best/")
    a_5_5_r = get_data_MP("save/A/dataset1/0.05_5_random/")
    a_5_10_w = get_data_MP("save/A/dataset1/0.05_10_worst/")
    a_5_10_b = get_data_MP("save/A/dataset1/0.05_10_best/")
    a_5_10_r = get_data_MP("save/A/dataset1/0.05_10_random/")
    a_25_1_w = get_data_MP("save/A/dataset1/0.25_smp_worst/")
    a_25_1_b = get_data_MP("save/A/dataset1/0.25_smp_best/")
    a_25_1_r = get_data_MP("save/A/dataset1/0.25_smp_random/")
    a_25_2_w = get_data_MP("save/A/dataset1/0.25_2_worst/")
    a_25_2_b = get_data_MP("save/A/dataset1/0.25_2_best/")
    a_25_2_r = get_data_MP("save/A/dataset1/0.25_2_random/")
    a_25_5_w = get_data_MP("save/A/dataset1/0.25_5_worst/")
    a_25_5_b = get_data_MP("save/A/dataset1/0.25_5_best/")
    a_25_5_r = get_data_MP("save/A/dataset1/0.25_5_random/")
    a_25_10_w = get_data_MP("save/A/dataset1/0.25_10_worst/")
    a_25_10_b = get_data_MP("save/A/dataset1/0.25_10_best/")
    a_25_10_r = get_data_MP("save/A/dataset1/0.25_10_random/")

    a = [a_5_1_w,a_5_1_b,a_5_1_r,a_5_2_w,a_5_2_b,a_5_2_r,a_5_5_w,a_5_5_b,a_5_5_r,a_5_10_w,a_5_10_b,a_5_10_r,a_25_1_w,a_25_1_b,a_25_1_r,a_25_2_w,a_25_2_b,a_25_2_r,a_25_5_w,a_25_5_b,a_25_5_r,a_25_10_w,a_25_10_b,a_25_10_r]

    b_5_1 = get_data_RI("save/B/dataset1/b_weak_0.05_smp/best_data.txt")
    b_5_2 = get_data_RI("save/B/dataset1/b_weak_0.05_par/best_data.txt")
    b_5_5 = get_data_RI("save/B/dataset1/b_weak_0.05_5/best_data.txt")
    b_5_10 = get_data_RI("save/B/dataset1/b_weak_0.05_10/best_data.txt")
    b_25_1 = get_data_RI("save/B/dataset1/b_weak_0.25_smp/best_data.txt")
    b_25_2 = get_data_RI("save/B/dataset1/b_weak_0.25_par/best_data.txt")
    b_25_5 = get_data_RI("save/B/dataset1/b_weak_0.25_5/best_data.txt")
    b_25_10 = get_data_RI("save/B/dataset1/b_weak_0.25_10/best_data.txt")
    b_75_1 = get_data_RI("save/B/dataset1/b_weak_0.75_smp/best_data.txt")
    b_75_2 = get_data_RI("save/B/dataset1/b_weak_0.75_par/best_data.txt")
    b_75_5 = get_data_RI("save/B/dataset1/b_weak_0.75_5/best_data.txt")
    b_75_10 = get_data_RI("save/B/dataset1/b_weak_0.75_10/best_data.txt")

    b = [b_5_1, b_5_2, b_5_5, b_5_10, b_25_1, b_25_2, b_25_5, b_25_10, b_75_1, b_75_2, b_75_5, b_75_10]
    
    main(a,b)
    
    # box_plot([a_5_10_w, b_75_10], ["Multiple Populations", "Random Immigrants"])
    # box_plot([b_5_1, b_25_1, b_75_1],["5%","25%","75%"])
    # box_plot([a_5_1_r,a_25_1_r],["5%","25%"])

    # box_plot([b_5_1,b_5_2,b_5_5,b_5_10],["1","2","5","10"])

    # box_plot([a_5_1_w,a_5_1_b,a_5_1_r],["worst","best","random"])
    # box_plot([a_25_2_w,a_25_2_b,a_25_2_r],["worst","best","random"])
    # box_plot([a_5_1_r, b_5_1],["Multi-populations","Random Immigrants"])
    # box_plot_color([b_5_1,b_5_2,b_5_5, b_5_10, b_25_1,b_25_2,b_25_5, b_25_10,  b_75_1,b_75_2,b_75_5, b_75_10],["5% 1","5% 2","5% 5","5% 10","25% 1","25% 2","25% 5","25% 10","75% 1","75% 2","75% 5","75% 10"])
    # box_plot_color([a_25_1_w,a_25_1_b,a_25_1_r,a_25_2_w,a_25_2_b,a_25_2_r,a_25_5_w,a_25_5_b,a_25_5_r,a_25_10_w,a_25_10_b,a_25_10_r],["1 w","1 b","1 r","2 w","2 b","2 r","5 w","5 b","5 r","10 w","10 b","10 r"])
    # box_plot_color([a_5_1_w,a_5_1_b,a_5_1_r,a_5_2_w,a_5_2_b,a_5_2_r,a_5_5_w,a_5_5_b,a_5_5_r,a_5_10_w,a_5_10_b,a_5_10_r],["1 w","1 b","1 r","2 w","2 b","2 r","5 w","5 b","5 r","10 w","10 b","10 r"])
