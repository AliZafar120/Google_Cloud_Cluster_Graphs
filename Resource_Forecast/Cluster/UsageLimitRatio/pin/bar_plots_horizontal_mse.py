from matplotlib import pyplot as plt
import numpy as np
# Read CSV into pandas
barWidth = 0.25
width=barWidth
name = ["u_25","u_50","u_75","u_100","u_collective","u_all","u_cumul"]

loss_mse=[0.00019,0.00147,0.0056,0.0286,0.0197,0.0250,0.013]
#savings_pin=[1223.09,630.99,333.37,10.85,180.03,192.21,45.53]
loss_pin = [0.0006,0.0015,0.012,0.097,0.042,0.029,0.153]

ind = np.arange(len(name))
# Figure Size
fig, ax = plt.subplots(figsize=(8, 8))

# Horizontal Bar Plot
ax.barh(ind, loss_mse, barWidth, color='red', label='MSE')
ax.barh(ind + barWidth, loss_pin, barWidth, color='green', label='PIN')

ax.set_title('Loss Functions MSE Loss',
             loc='center', )
ax.set(yticks=ind + width, yticklabels=name, ylim=[2*width - 1, len(name)])
ax.legend()


plt.savefig('./output_images/cluster_usagelimitratio_mse.jpg')
plt.show()