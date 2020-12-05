import pandas
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

df1 = pandas.read_csv('configurations_3000_750.csv')
df2 = pandas.read_csv('configurations_6000_750.csv')

df1 = df1.sort_values('recall')
df2 = df2.sort_values('recall')
df1 = df1[df1['recall'] < 0.45]
df2 = df2[df2['recall']!=0]


fig = plt.figure()

x1 = df1['recall']
y1 = df1['precision']
x2 = df2['recall']
y2 = df2['precision']

plt.plot(x1,y1, ".-")
plt.plot(x2, y2, ".-")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve")

blue_patch = mpatches.Patch(color='blue', label='3300 negatives')
orange_patch = mpatches.Patch(color='orange', label='6600 negatives')
plt.legend(handles=[blue_patch, orange_patch])

plt.show()

fig.savefig("./precision-recall_curve_compare")