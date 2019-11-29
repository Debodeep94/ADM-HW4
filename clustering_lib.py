#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import random
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:



def kmeans(data):
    
    data = data.sample(frac=1).reset_index(drop=True)
    

    data['cluster'] = None
    data.iloc[0,-1]=1
    data.iloc[1,-1]=2
    data.iloc[2,-1]=3

    mean_cluster1 = list(data[data['cluster']==1].iloc[:,1:-1].mean(axis=0))
    mean_cluster2 = list(data[data['cluster']==2].iloc[:,1:-1].mean(axis=0))
    mean_cluster3 = list(data[data['cluster']==3].iloc[:,1:-1].mean(axis=0))

    distance_metric1=1000
    distance_metric2=0
    iter_count = 1
    abs_diff=1000
    
    while abs_diff>0.001:
        distance_metric2=distance_metric1
        distance_metric1=0
        for i in range(data.shape[0]):
            this_point = list(data.iloc[i,1:-1])
            euc_dist_clust1 = math.sqrt(sum([(a - b) ** 2 for a, b in zip(this_point, mean_cluster1)]))
            euc_dist_clust2 = math.sqrt(sum([(a - b) ** 2 for a, b in zip(this_point, mean_cluster2)]))
            euc_dist_clust3 = math.sqrt(sum([(a - b) ** 2 for a, b in zip(this_point, mean_cluster3)]))
            min_dist = min(euc_dist_clust1, euc_dist_clust2, euc_dist_clust3)
            if min_dist == euc_dist_clust1:
                x = 1
            elif min_dist == euc_dist_clust2:
                x = 2
            else:
                x = 3
            if data.iloc[i,-1] != x:
               
                data.iloc[i,-1] = x
            mean_cluster1 = list(data[data['cluster']==1].iloc[:,1:-1].mean(axis=0))
            mean_cluster2 = list(data[data['cluster']==2].iloc[:,1:-1].mean(axis=0))
            mean_cluster3 = list(data[data['cluster']==3].iloc[:,1:-1].mean(axis=0))
            distance_metric1 = distance_metric1+min_dist
        
        abs_diff = abs(distance_metric1-distance_metric2)
        iter_count += 1
        if (abs_diff==0):
            break
    return(data)

