
# 
# # Predict wine quality with 'revoscalepy'
# 
# 
# 'revoscalepy' is a library provided by Microsoft to support high-performance algorithms for Python. This sample will showcase how to 'revoscalepy" algos for predictive analytics.
# 
# This sample will use [wine quality data set](https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv)
# from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets.html).  
# The dataset contains quality ratings (labels) for a 1599 red wine samples. 
# The features are the wines' physical and chemical properties (11 predictors). 
# This sample will use these properties to predict the quality of the wine. 
# The experiment is shown below and can be found in the 
# [Cortana Intelligence Gallery](https://gallery.cortanaintelligence.com/Experiment/Predict-Wine-Quality-Classification-10>)
# 
# *Sources:* 
# 
# - [Predicting Wine Quality with Azure ML and R](http://blog.revolutionanalytics.com/2016/04/predicting-wine-quality.html>)
# - [Predicting Wine
#   Quality with revoscaler](https://github.com/shaheeng/ClassificationModelEvaluation/blob/master/PredictWineQuality_RevBlog3/Predicting%20Wine%20Quality%20-%20Shaheen.ipynb>)
# 
# Processing the data
# ===================
# 
# Let's start with collecting and preparing the data.
# We save the data in a single file in order to avoid downloading them
# many times.
# 
# 

# In[21]:

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas
import os

if not os.path.exists("wines_backup.csv"):
    # if not exist, we create wines.csv which combines red and white wines into a single file
    columns = ["facidity", "vacidity", "citric", "sugar", "chlorides", "fsulfur", 
               "tsulfur", "density", "pH", "sulphates", "alcohol", "quality"]
    red = pandas.read_csv("http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
                         names=columns, sep=";", skiprows=1)
    white = pandas.read_csv("http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv",
                         names=columns, sep=";", skiprows=1)
    red["color"] = "red"
    white["color"] = "white"
    wines = pandas.concat([white, red])
    wines.to_csv("wines_backup.csv", sep="\t", index=False)
else:
    wines = pandas.read_csv("wines_backup.csv", sep="\t")
    
print(wines.head(n=5))


# The goal is to predict the quality of the wines.
# Let's see how this variable is distributed.
# 
# 

# In[22]:


fig, ax = plt.subplots(1, 1)
wines["quality"].hist(bins=7, ax=ax)
ax.set_xlabel("quality")
ax.set_ylabel("# wines")
#plt.show()


# Is there any differance between red and white wines?
# 
# 

# In[23]:


red = wines[wines.color=="red"]["quality"]
white = wines[wines.color=="white"]["quality"]

fig, ax = plt.subplots(1, 1)
ax.hist([red, white], label=["red", "white"], alpha=0.5,
        histtype='bar', bins=7, color=["red", "green"])
ax.legend()
ax.set_xlabel("quality")
ax.set_ylabel("# wines")
#plt.show()


# There are more white wines and more high quality white wines.
# Let's see if the quality is correlated to the alcohol degree?
# 
# 

# In[24]:


fig, ax = plt.subplots(1, 1)
ax.scatter(x=wines.alcohol, y=wines.quality)
ax.set_xlabel("alcohol")
ax.set_ylabel("quality")
#plt.show()


# Quite difficult to see don't you think?
# 
# 

# In[25]:


fig, ax = plt.subplots(1, 1)
wines.plot.hexbin(x='alcohol', y='quality', ax=ax, gridsize=25)
#plt.show()


# The alcohol does not explain the quality all by itself.
# 
# Training
# ===============================
# 
# The quality is a mark between 1 and 9.
# We use a revoscalepy decision tree algorithm to predict it.
# But before anything starts, we need to split the dataset
# into train and test.
# 
# 

# In[26]:


try:
    from sklearn.model_selection import train_test_split
except ImportError:
    from sklearn.cross_validation import train_test_split
wines_train, wines_test = train_test_split(wines)


# And we train. We drop the color which is a non numerical
# features.
# 
# 

# In[27]:


from revoscalepy import rx_dtree
cols = wines.columns.drop(["quality", "color"])
model = rx_dtree("quality ~" + "+".join(cols), data=wines_train, 
                 method="anova",allow_disk_write = False)


# Now let's evaluate the model accuracy.
# 
# 

# In[28]:


from revoscalepy import rx_predict_rx_dtree
pred = rx_predict_rx_dtree(model, wines_test, extra_vars_to_write=["quality"])
print(pred.head())


# The column 'quality_Pred' is the prediction.
# We estimate its quality with the metric [R2](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html)
# and we plot them.
# 
# 

# In[29]:


from sklearn.metrics import r2_score
r2 = r2_score(pred.quality, pred.quality_Pred)
print("R2=", r2)

fig, ax = plt.subplots(1, 1)
ax.scatter(x=pred.quality, y=pred.quality_Pred)
ax.set_xlabel("quality")
ax.set_ylabel("prediction")
#plt.show()


# It is not easy to read.
# 
# 

# In[30]:


fig, ax = plt.subplots(1, 1)
pred.plot.hexbin(x='quality', y='quality_Pred', ax=ax, gridsize=25)
#plt.show()
plt.savefig('./outputs/predict.png')


# It seems to be doing a relatively good job to predict
# marks 5, 6, 7. 
# 
