import bags_array_test_2 as bg
import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np
import pandas as pd
import os 

# df_33_1 = bg.bags_array(r"C:\Users\misha\Desktop\data\F33\F33_20000").df_array
# df_33_2 = bg.bags_array(r"C:\Users\misha\Desktop\data\F33\F33_12000").df_array

# df_37_1 = bg.bags_array(r"C:\Users\misha\Desktop\data\F37\F37_10000_21_11_2025").df_array
# df_37_2 = bg.bags_array(r"C:\Users\misha\Desktop\data\F37\F37_15000_20_11_2025").df_array

# df_41 = bg.bags_array(r"C:\Users\misha\Desktop\data\F41\F41_10000_21_11_2025").df_array
# df_41_1 = bg.bags_array(r"C:\Users\misha\Desktop\data\F41\F41_15000_20_11_2025").df_array

# df_45_1 =  bg.bags_array(r"C:\Users\misha\Desktop\data\F45\F45_20000_07_11_2025").df_array

# df_concat = pd.concat([df_33_1, df_37_1, df_41, df_37_2, df_33_2, df_45_1], ignore_index=True)
# df_concat = df_concat.dropna()
# df_concat.to_excel(r"C:\Users\misha\Desktop\output2.xlsx")


df = pd.read_excel(r"C:\Users\misha\Desktop\output.xlsx").dropna()

# Выравнивание групп по минимальному размеру
df_min = min(df.groupby(by='wind_velocity').size())
df = df.groupby(by='wind_velocity').head(df_min)


df = df[df['t_average'] < 0.0004]

sns.histplot(x = df['velocity'])
plt.show()