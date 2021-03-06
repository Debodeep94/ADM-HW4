{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Since this kind of clustering is based on the distribution of data and we choose our initial centroids by considering the range of data, the way in which data are distributed would affect the centroids.\n",
    "\n",
    "1-If the data does not normalize the range of picking the initial centroids which are randomly selected from the range of data. The initial centroids are needed to be updated several times to be an appropriate cluster and be close to remain data. K-means algorithm which makes use of sum of squares of deviations from cluster centroids is vulnerable to outliers. In some cases, there is the possibility that the outlier data with a low density be considered as a separated cluster\n",
    "\n",
    "2-In addition, in the case data aggregation place in far distances from each other, the initial centroids will lie on the aggregated sides. Then it would take more time and steps to reach the optimum clusters for all data. \n",
    "\n",
    "3- In k-means clustering, it is assumed that all clusters have the same radius from their centroids. So, when the distribution radius of data in a cluster is more than others, it could fail.\n",
    "\n",
    "4-When density in a cluster is more than others, the k-means clustering will fail due to its assumption that the number of points in each cluster are roughly equal."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
