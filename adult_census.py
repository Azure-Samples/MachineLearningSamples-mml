import pandas
import os
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve
from microsoftml import rx_fast_trees, rx_predict
from microsoftml import categorical

columns = ["age", "workclass", "fnlwgt", "education", "educationnum", "maritalstatus",
           "occupation", "relationship", "race", "sex", "capitalgain", "capitalloss", 
           "hoursperweek", "nativecountry", "Label"]

def preprocess_data(df):
    # The data contains '?' for missing values.
    # We replace them and remove them.
    # We convert every numerical features into either str or float.
    # We remove extra spaces and put every thing in lower case.
    for c in df.columns:
        df[c] = df[c].apply(lambda x: numpy.nan if x == '?' else x)
    df = df.dropna()
    for c in df.columns:
        try:
            newc = df[c].astype(float)
            print("numerical", c)
        except Exception as e:
            print("categorical", c)
            newc = df[c].astype(str).apply(lambda s: s.strip(". ").lower())
        df[c] = newc
    return df

if os.path.exists("adult.train.csv"):
    train = pandas.read_csv("adult.train.csv")
else:
    train = pandas.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
                            header=None, names=columns)
    train = preprocess_data(train)
    # We store the data on disk to avoid loading it every time
    # we execute the script.
    train.to_csv("adult.train.csv", index=False)
    
print(train.shape)
print(train.head())

if os.path.exists("adult.test.csv"):
    test = pandas.read_csv("adult.test.csv")
else:
    test = pandas.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test",
                            header=None, names=columns)
    test = preprocess_data(test)
    # We store the data on disk to avoid loading it every time
    # we execute the script.
    test.to_csv("adult.test.csv", index=False)
    
print(test.shape)
print(test.head())

train["Label"] = train["Label"] == ">50k"
test["Label"] = test["Label"] == ">50k"

trees = rx_fast_trees("Label ~ age + fnlwgt + educationnum + capitalgain + capitalloss", data=train)
y_pred = rx_predict(trees, test)

print(y_pred.head())
print(y_pred.tail())

from sklearn.metrics import confusion_matrix
conf = confusion_matrix(test["Label"], y_pred["PredictedLabel"])
print(conf)

try:
    trees2 = rx_fast_trees("Label ~ age + fnlwgt + educationnum + capitalgain + capitalloss + education", data=train)
except Exception as e:
    print(e)

trees2 = rx_fast_trees("Label ~ age + fnlwgt + educationnum + capitalgain + capitalloss + education_cat",
                       data=train,
                       ml_transforms=[categorical(cols=dict(education_cat="education"))])

y_pred2 = rx_predict(trees2, test)
conf = confusion_matrix(test["Label"], y_pred2["PredictedLabel"])
print(conf)

cats = {}
for col in ["workclass", "education", "maritalstatus", "occupation", 
            "relationship", "race", "sex", "nativecountry"]:
    cats[col + "_cat"] = col

formula = "Label ~ age + fnlwgt + educationnum + capitalgain + capitalloss +" + \
          " + ".join(sorted(cats.keys()))
          
print(cats)
print(formula)

trees3 = rx_fast_trees(formula, data=train,
                       ml_transforms=[categorical(cols=cats)])
y_pred3 = rx_predict(trees3, test)
conf = confusion_matrix(test["Label"], y_pred3["PredictedLabel"])
print(conf)

fpr, tpr, th = roc_curve(test["Label"], y_pred3["Probability"])

plt.figure()
plt.plot(fpr, tpr, label=">50k")
plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title('ROC - Adult Data Set')
plt.legend(loc="lower right")

# save ROC to outputs
plt.savefig('./outputs/roc.png')