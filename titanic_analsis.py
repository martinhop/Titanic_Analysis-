'''

Objectives:

1.) Who were the passengers on the Titanic? (Ages,Gender,Class,..etc)
2.) What deck were the passengers on and how does that relate to their class?
3.) Where did the passengers come from?
4.) Who was alone and who was with family?
5.) What factors helped someone survive the sinking?


'''

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

#Define dataset

titanic_df = pd.read_csv('train.csv')
titanic_df.head()

print ("1.) Who were the passengers on the Titanic? (Ages,Gender,Class,..etc)")

#1) who were the passengers on the titanic

#Spilt of male, female passengers on titanic across all classes

sns.catplot('Sex',data=titanic_df, kind='count')

#Spilt of male, female (inc. children) in each class

sns.catplot('Sex', data= titanic_df, hue= 'Pclass', kind= 'count')

#Spilt of male, female (inc. children) in each class

sns.catplot('Pclass', data= titanic_df, hue= 'Sex', kind= 'count')

#Function to determine if each passenger is a male, female of child

def male_female_child(passenger):
    age,sex = passenger

    if age < 16:
        return 'child'
    else:
        return sex

#adding a person column to data set using function male_female_child

titanic_df['Person'] = titanic_df[['Age', 'Sex']].apply(male_female_child, axis=1)
titanic_df.head(10)

#Spilt of male, female and children in each class on the titanic

sns.catplot('Pclass', data= titanic_df, hue= 'Person', kind = 'count')

#Histagram showing spread of ages on the titanic

titanic_df['Age'].hist(bins = 70)

#Average age of all passengers on the titanic

round(titanic_df['Age'].mean(), 0)

#Passengers split between male, female and children

titanic_df['Person'].value_counts()

#kde plot showing the ages of male, female (inc. children) passengers on the titanic.

fig = sns.FacetGrid(titanic_df, hue = 'Sex', aspect = 4)
fig.map(sns.kdeplot, 'Age', shade = True)

oldest = titanic_df['Age'].max()

fig.set(xlim = (0, oldest))

fig.add_legend()

#kde plot showing the ages of male, female and children passengers on the titanic.

fig = sns.FacetGrid(titanic_df, hue = 'Person', aspect = 4)
fig.map(sns.kdeplot, 'Age', shade = True)

oldest = titanic_df['Age'].max()

fig.set(xlim = (0, oldest))

fig.add_legend()

#kde plot showing the ages of male, female by class on the titanic.

fig = sns.FacetGrid(titanic_df, hue = 'Pclass', aspect = 4)
fig.map(sns.kdeplot, 'Age', shade = True)

oldest = titanic_df['Age'].max()

fig.set(xlim = (0, oldest))

fig.add_legend()

#2 What deck were the passengers on and how does that relate to their class?

titanic_df.head()

deck = titanic_df['Cabin'].dropna()
deck.head()

#Passengers per deck

levels = []

for level in deck:
    levels.append(level[0])

cabin_df = DataFrame(levels)
cabin_df.columns = ['Cabin']
cabin_df = cabin_df[cabin_df.Cabin != 'T']
sns.catplot('Cabin', data = cabin_df, palette = 'summer', kind='count')

#3) Where did the passengers come from?

titanic_df.head()

#Passenger numbers by embarked city and class

sns.catplot(x='Embarked',hue='Pclass', data = titanic_df, kind='count')

#4.) Who was alone and who was with family?

titanic_df.head()

titanic_df['Alone'] = titanic_df.SibSp + titanic_df.Parch
titanic_df['Alone']

#add column to dataset to determine if passenger alone based on
#if they had any SibSp or Parch

titanic_df['Alone'].loc[titanic_df['Alone'] > 0] = 'With Family'
titanic_df['Alone'].loc[titanic_df['Alone'] == 0] = 'Alone'

titanic_df.head()

#Passengers traveling alone / with family

sns.catplot('Alone', data = titanic_df, palette = 'Blues', kind = 'count')

#5) What factors helped someone survive the sinking?

#add a column to the dataset to show if a passenger survived

titanic_df['Survivor'] = titanic_df.Survived.map({0: 'no', 1: 'yes'})
titanic_df.head()

#passengers that survived vs # NOTE:
sns.catplot('Survivor', data = titanic_df, palette = 'Set2', kind = 'count')

#Survivors base on male / female / children

sns.catplot('Pclass', 'Survived', hue= 'Person', data= titanic_df, kind= 'point')

#suvivors based on ages

sns.lmplot('Age', 'Survived', data = titanic_df)

#suvivors based on ages and class all ages:

sns.lmplot('Age', 'Survived', hue= 'Pclass', data = titanic_df, palette = 'winter')

#suvivors based on age groups and class:

generations = [10, 20, 30, 40, 60, 80]

sns.lmplot("Age", 'Survived', hue='Pclass', data= titanic_df, palette = 'winter', x_bins = generations)

#suvivors based on sex:

sns.lmplot("Age", 'Survived', hue='Sex', data = titanic_df, palette = 'winter', x_bins=generations)
