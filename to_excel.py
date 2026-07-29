import bags_array_sphere as bg 
import pandas as pd 
import numpy as np 



F33_20000 = bg.bags_array(r"C:\Users\misha\Desktop\science_code\data\clear_water\F33\F33_20000").df_result
F33_12000 = bg.bags_array(r"C:\Users\misha\Desktop\science_code\data\clear_water\F33\F33_12000").df_result

F37_15000_20_11_2025 = bg.bags_array(r"C:\Users\misha\Desktop\science_code\data\clear_water\F37\F37_15000_20_11_2025").df_result
F37_10000_21_11_2025 = bg.bags_array(r"C:\Users\misha\Desktop\science_code\data\clear_water\F37\F37_10000_21_11_2025").df_result

F41_15000_20_11_2025 = bg.bags_array(r"C:\Users\misha\Desktop\science_code\data\clear_water\F41\F41_15000_20_11_2025").df_result
F41_10000_21_11_2025 = bg.bags_array(r"C:\Users\misha\Desktop\science_code\data\clear_water\F41\F41_10000_21_11_2025").df_result
F41_20000 = bg.bags_array(r"C:\Users\misha\Desktop\science_code\data\clear_water\F41\F41_20000").df_result
F41_20000_14_11_2025 = bg.bags_array(r"C:\Users\misha\Desktop\science_code\data\clear_water\F41\F41_20000_14_11_2025").df_result


F45_20000_07_11_2025 = bg.bags_array(r"C:\Users\misha\Desktop\science_code\data\clear_water\F45\F45_20000_07_11_2025").df_result
F45_20000_14_11_2025 = bg.bags_array(r"C:\Users\misha\Desktop\science_code\data\clear_water\F45\F45_20000_14_11_2025").df_result

all_data = [
    (F33_20000, 'F33_20000'),
    (F33_12000, 'F33_12000'),
    (F37_15000_20_11_2025, 'F37_15000_20_11_2025'),
    (F37_10000_21_11_2025, 'F37_10000_21_11_2025'),
    (F41_15000_20_11_2025, 'F41_15000_20_11_2025'),
    (F41_10000_21_11_2025, 'F41_10000_21_11_2025'),
    (F41_20000, 'F41_20000'),
    (F41_20000_14_11_2025, 'F41_20000_14_11_2025'),
    (F45_20000_07_11_2025, 'F45_20000_07_11_2025'),
    (F45_20000_14_11_2025, 'F45_20000_14_11_2025')
]

# Объединение всех DataFrame
combined_df = pd.concat([df for df, _ in all_data], ignore_index=True)

combined_df.to_excel('new_output_2.xlsx', index=False)