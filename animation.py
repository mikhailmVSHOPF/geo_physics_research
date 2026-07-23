import bags_array_test_2 as bg_2
import bags_array_test as bg
import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np
import pandas as pd
from PIL import Image 
import os 
from celluloid import Camera  # ✅ Уже импортировано

result = bg.bags_array("C:/Users/misha/Desktop/experiment_with_canopy/test")
result_temp = result.df_point_of_gap
phi = np.linspace(0, 2*np.pi, 100)
path = str(result_temp['source_path'][0][:-4])
image_name = os.listdir(path)

fig = plt.figure(figsize=(10, 8))
camera = Camera(fig)

for name, group in result_temp.groupby(by='frame'):
    dx = group['dx'].values[0] if 'dx' in group else 1.0  # Если dx есть в данных

    ##разрыв
    x_center = group['x_r'].values
    y_center = group['y_r'].values
    R = group['R_r'].values

    x_pixels = np.round((x_center + R[:, np.newaxis] * np.cos(phi)) / dx)
    y_pixels = np.round((y_center + R[:, np.newaxis] * np.sin(phi)) / dx)

    ##купол
    if 'x_c' in result_temp:
        x_center_c = group['x_c'].values
        y_center_c = group['y_c'].values
        R_c = group['R'].values

        x_pixels_c = np.round((x_center_c + R_c[:, np.newaxis] * np.cos(phi)) / dx)
        y_pixels_c = np.round((y_center_c + R_c[:, np.newaxis] * np.sin(phi)) / dx)
        plt.scatter(x=x_pixels_c, y=y_pixels_c, s=1, color='green')



    full_path = os.path.join(path, image_name[name])
    img = np.array(Image.open(full_path))
    plt.imshow(img)
    plt.scatter(x=x_pixels, y=y_pixels, s=1, color='red')
    plt.title(f'Frame: {name}')
    plt.axis('off')
    camera.snap()

animation = camera.animate(interval=500, repeat=True, repeat_delay=1000)

plt.show()

animation.save('C:/Users/misha/Desktop/animation.gif', writer='pillow', fps=2)
print("Анимация сохранена как animation.gif")