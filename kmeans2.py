# This program organizes data points into clusters
# using the k-means algorithm. It asks the user to input
# the amount of clusters and the amount of k-means iterations
# to implement. After running, it plots out the data points
# with each cluster showing in a different color on a matplotlib
# figure.

import csv
import matplotlib.pyplot as plt
import numpy as np
import random
from statistics import mean


# Convert data file to 2d list of strings.
def fileToList(f):
    dataList = []
    listRow = []

    with open(f) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                listRow.append(row[0])
                listRow.append(row[1])
                listRow.append(row[2])
                dataList.append(listRow)
                listRow = []

    return dataList


# Convert x and y columns from list of strings to list of floats.
def getDataPoints(dataList):
    birth_rate = []
    life_expectancy = []
    xs_and_ys = []

    for i in range(0, len(dataList)):
        float_birth_rate = float(dataList[i][1])
        birth_rate.append(float_birth_rate)
        float_life_expectancy = float(dataList[i][2])
        life_expectancy.append(float_life_expectancy)
    xs_and_ys.append(birth_rate)
    xs_and_ys.append(life_expectancy)

    return xs_and_ys


# Initialize clusters.
def initClusters(floatList, numClusters):
    x = floatList[0]
    y = floatList[1]
    clustersX = []
    clustersY = []
    clusters = []

    for i in range(0, numClusters):
        clustersX.append(random.choice(x))
        clustersY.append(random.choice(y))
    clusters.append(clustersX)
    clusters.append(clustersY)

    return clusters


# Function for calculating mean.
def calcMean(xs, ys):
    meanXs = mean(xs)
    meanYs = mean(ys)
    return meanXs, meanYs


# K means function that returns better fitting clusters.
def kMeansAlg(points, centroids, iterations):
    # Outer loop for iterating from one
    # K-means re-centering to the next.
    for h in range(0, iterations):

        # Structures for storing data as we shift cluster centers.
        distances = []
        clusters = []

        # 3D List for storing clusters.
        for i in range(0, len(centroids[0])):
            row = []
            clusters.append(row)
            for j in range(2):
                column = []
                row.append(column)

        # Inner loops for comparing distance of data points to centroids.
        for i in range(0, len(points[0])):
            for j in range(0, len(centroids[0])):
                distance = np.sqrt((points[0][i] - centroids[0][j]) ** 2 +
                                   (points[1][i] - centroids[1][j]) ** 2)
                distances.append(distance)

            # Get distance of closest centroid to given data point.
            min_distance = min(distances)
            index_of_min = distances.index(min_distance)

            for b in range(0, len(distances)):
                # Add that given data point to its nearest cluster.
                if index_of_min == b:
                    clusters[b][0].append(points[0][i])
                    clusters[b][1].append(points[1][i])
            distances = []

        # Build a data structure for storing new centroids.
        centroids = []
        for i in range(0, 2):
            row = []
            centroids.append(row)

        # Get the mean of each cluster to find a new center
        # and add it to centroids data structure.
        for k in range(0, len(clusters)):
            means_x = []
            means_y = []
            if clusters[k][0]:
                means_x, means_y = calcMean(clusters[k][0], clusters[k][1])
                centroids[0].append(means_x)
                centroids[1].append(means_y)

    return clusters


# Get list of country names corresponding to points in a cluster.
def getCountries(cluster, dataList):
    countryList = []

    for i in range(0, len(cluster[0])):
        for j in range(0, len(dataList)):
            x = float(dataList[j][1])
            y = float(dataList[j][2])
            if cluster[0][i] == x:
                if cluster[1][i] == y:
                    countryList.append(dataList[j][0])

    return countryList


# Convert list of countries to string of countries.
def countriesToString(countryList):
    countryString = ""

    for i in range(0, len(countryList)):
        countryString += countryList[i] + "\n"

    return countryString


# Get user to input cluster amount and k-means iteration amount.
cluster_amount = int(input("Input cluster amount: "))
k_means_iterations = int(input("Input k-means iteration amount: "))
file = input("Input data file: data1953.csv OR data2008.csv OR dataBoth.csv ")
# Convert data file into a list of x and y data points.

dataList = fileToList(file)
xs_and_ys = getDataPoints(dataList)

# Initialize centroids and run the k-means algorithm.
centroids = initClusters(xs_and_ys, cluster_amount)
clusters = kMeansAlg(xs_and_ys, centroids, k_means_iterations)

# Lists for storing countries in clusters
# and mean values for life expectancy and birth rates.
all_countries = []
all_means = []

# Populate lists with countries and mean values
for i in range(0, cluster_amount):
    country_cluster = []
    country_cluster = getCountries(clusters[i], dataList)
    all_countries.append(country_cluster)
    all_means.append(calcMean(clusters[i][0], clusters[i][1]))

# Display statistics for clusters to user.
for i in range(0, cluster_amount):
    print(f'''Cluster {i + 1} countries:
Number of countries:  {len(all_countries[i])}
Mean Birth Rate: {all_means[i][0]}
Mean Life Expectancy: {all_means[i][1]}
{countriesToString(all_countries[i])}''', "\n")

# List of colors to plot clusters in.
color_maps = ["Blue", "Green", "Purple", "Pink", "Red", "Orange", "Brown", "Black", "Yellow", "Grey"]

# Plot the clusters and show the figure.
for i in range(0, cluster_amount):
    plt.scatter(clusters[i][0], clusters[i][1], c=color_maps[i])

plt.show()
