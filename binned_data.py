import bags_array_test as bg
import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np
from scipy import stats
import pandas as pd


# df_33_1 = bg.bags_array(r"C:\Users\misha\Desktop\data\F33\F33_20000").df_array
# df_33_2 = bg.bags_array(r"C:\Users\misha\Desktop\data\F33\F33_12000").df_array

# df_37_1 = bg.bags_array(r"C:\Users\misha\Desktop\data\F37\F37_10000_21_11_2025").df_array
# df_37_2 = bg.bags_array(r"C:\Users\misha\Desktop\data\F37\F37_15000_20_11_2025").df_array

# df_41 = bg.bags_array(r"C:\Users\misha\Desktop\data\F41\F41_10000_21_11_2025").df_array
# # df_41_1 = bg.bags_array(r"C:\Users\misha\Desktop\data\F41\F41_15000_20_11_2025").df_array

# df_45_1 =  bg.bags_array(r"C:\Users\misha\Desktop\data\F45\F45_20000_07_11_2025").df_array

# df_concat = pd.concat([df_33_1, df_37_1, df_41, df_37_2, df_33_2, df_45_1], ignore_index=True)
# df_concat = df_concat.dropna()
# df_concat.to_excel(r"C:\Users\misha\Desktop\output.xlsx")


df = pd.read_excel(r"C:\Users\misha\Desktop\output.xlsx").dropna()

# Выравнивание групп по минимальному размеру
df_min = min(df.groupby(by='wind_velocity').size())
df = df.groupby(by='wind_velocity').head(df_min)

# Список для сбора результатов биннинга
binned_data = []

for name, group in df.groupby(by='wind_velocity'):
    # Разбиваем t_average на 5 бинов
    group['bin'] = pd.cut(x=group['t_average'], bins=5)
    
    # Группируем по бинам и считаем среднее
    binned_group = group.groupby('bin', observed=False).agg({
        't_average': 'mean',      # среднее значение t_average в бине
        'velocity': 'mean'        # среднее значение velocity в бине
    }).reset_index()
    
    binned_group['wind_velocity'] = name  # добавляем метку группы
    binned_data.append(binned_group)

# Объединяем все группы
df_binned = pd.concat(binned_data, ignore_index=True)

# Выравнивание групп по минимальному размеру
df_min = min(df_binned.groupby(by='wind_velocity').size())
df_binned = df_binned.groupby(by='wind_velocity').head(df_min)

# for name, group in df_binned.groupby(by='wind_velocity'):
#     sns.scatterplot(x = group['t_average'], y = group['velocity'], label = name)
# plt.legend()
# plt.show()


for name, group in df.groupby(by='wind_velocity'):
    # Создаем бины по t_average внутри каждой группы
    group['t_bin'] = pd.cut(group['t_average'], bins=10)  # 10 бинов, можно изменить
    
    # Группируем по бинам и находим среднее velocity
    binned_means = group.groupby('t_bin')['velocity'].mean().reset_index()
    
    # Извлекаем среднее значение t_average для каждого бина (для оси X)
    binned_means['t_mid'] = binned_means['t_bin'].apply(lambda x: x.mid)
    
    # Строим график
    sns.scatterplot(x=binned_means['t_mid'], y=binned_means['velocity'], label=name)
    sns.regplot(x=group['t_average'], y=group['velocity'])

plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show()