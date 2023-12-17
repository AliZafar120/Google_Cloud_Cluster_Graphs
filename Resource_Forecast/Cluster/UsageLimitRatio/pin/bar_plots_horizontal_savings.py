from matplotlib import pyplot as plt
import numpy as np
# Read CSV into pandas
barWidth = 0.25
width=barWidth
name = ["u_25","u_50","u_75","u_100","u_collective","u_all","u_cumul"]
#violations = [0.34,0.56,0.59,0.55,.78,0.74,0.68]
savings_mse=[0.87,0.738,0.575,0.082,0.256,0.271,0.231]
#mse=[]
savings_pin=[0.79,0.59,0.24,0.0048,0.095,0.118,0.0077]


ind = np.arange(len(name))
# Figure Size
fig, ax = plt.subplots(figsize=(8, 8))

# Horizontal Bar Plot
ax.barh(ind, savings_mse, barWidth, color='red', label='MSE')
ax.barh(ind + barWidth, savings_pin, barWidth, color='green', label='PIN')

ax.set_title('Savings',
             loc='center', )
ax.set(yticks=ind + width, yticklabels=name, ylim=[2*width - 1, len(name)])
ax.legend()


plt.savefig('./output_images/cluster_usagelimitratio_savings.jpg')
plt.show()