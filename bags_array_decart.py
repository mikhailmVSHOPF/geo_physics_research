import re
import os
import numpy as np
from scipy.optimize import minimize
import pandas as pd


class bags_array(object):

    ###################################### ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ

    def circle_residuals(self, params, x, y):
        x0, y0, R = params
        distances = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)
        return np.sum(abs((distances - R)))

    def appr_circle(self, x_data, y_data):
        x0_guess = np.mean(x_data)
        y0_guess = np.mean(y_data)
        R_guess = np.mean(np.sqrt((x_data - x0_guess) ** 2 + (y_data - y0_guess) ** 2))
        initial_guess = [x0_guess, y0_guess, R_guess]
        result = minimize(self.circle_residuals, initial_guess, args=(x_data, y_data))
        return result

    ###################################### ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ЗАКОНЧИЛИСЬ

    ###################################### ЧТЕНИЕ ФАЙЛОВ
    def points_of_gap(self, path):
        regex_r = re.compile(r'.+r(\d+)\t(\d+)\t(\d+,\d+)\t(\d+,\d+)')
        t_r_list = [];
        x_r_list = [];
        y_r_list = [];
        frame_list = [];
        df = pd.DataFrame(columns=['x_r', 'y_r', 't_r', 'frame', 'pixel_x_r', 'pixel_y_r']);
        with open(self.folder_path + "/" + path) as file:
            for line in file:
                if re.search(regex_r, line):
                    data = re.findall(regex_r, line)[0]
                    t_r = float(data[1]) * (1 / self.fps) - self.t_p
                    frame = int(data[1])
                    x_r = float(data[2].replace(',', '.')) * self.dx
                    y_r = float(data[3].replace(',', '.')) * self.dx
                    x_r_list.append(x_r);
                    y_r_list.append(y_r);
                    t_r_list.append(t_r)
                    frame_list.append(frame)
        df['x_r'] = x_r_list;
        df['y_r'] = y_r_list;
        df['t_r'] = t_r_list;
        df['frame'] = frame_list;


        x_r_array = [];
        y_r_array = [];
        R_r_array = [];
        frame_r_array = [];
        t_array = []
        for name, group in df.groupby(by='t_r'):
            x = group['x_r'].values
            y = group['y_r'].values
            frame = (group['frame'].values)[0]
            result = self.appr_circle(x, y)
            x_r, y_r, R = result.x
            x_r_array.append(x_r)
            y_r_array.append(y_r)
            R_r_array.append(R)
            frame_r_array.append(frame)
            t_array.append(name)

        self.df_point_of_gap = pd.DataFrame({'x_r': x_r_array, 
                                             'y_r': y_r_array,
                                             'R_r': R_r_array,
                                             'frame': frame_r_array,
                                             't': t_array,
                                             'source_path': str(self.folder_path + "/" + path),
                                             'dx': float(self.dx), 
                                             'fps':int(self.fps)
        })
        return self.df_point_of_gap;

    def point_canopy(self, path):
        regex_point = re.compile(r'^(point)\t\t(\d+)\t(\d+,\d+)\t(\d+,\d+)')
        canopy_x = []
        canopy_y = []
        canopy_t = []
        with open(self.folder_path + "/" + path) as file:
            for line in file:
                if re.search(regex_point, line):
                    data = re.findall(regex_point, line)[0]
                    t = float(data[1]) * (1 / self.fps) - self.t_p
                    x = float(data[2].replace(',', '.')) * self.dx - self.x_p
                    y = float(data[3].replace(',', '.')) * self.dx - self.x_p
                    canopy_t.append(t)
                    canopy_x.append(x)
                    canopy_y.append(y)
        df = pd.DataFrame(columns=['x', 'y', 't'])
        df['x'] = canopy_x;
        df['y'] = canopy_y;
        df['t'] = canopy_t;

        xc_array = [];
        yc_array = [];
        R_array = [];
        time_array = []

        for time, group in df.groupby('t'):
            x = group['x'].values
            y = group['y'].values

            result = self.appr_circle(x, y)
            xc, yc, R = result.x
            xc_array.append(xc)
            yc_array.append(yc)
            R_array.append(R)
            time_array.append(time)

        self.df_canopy = pd.DataFrame(columns=['xc', 'yc', 'R', 't'])
        self.df_canopy['xc'] = xc_array;
        self.df_canopy['yc'] = yc_array;
        self.df_canopy['R'] = R_array;
        self.df_canopy['t'] = time_array
        return self.df_canopy

    def line_points(self, path):
        self.df_line_points = pd.DataFrame(columns=['x_s', 'x_e', 'y_s', 'y_e', 't_s', 't_e'])
        regex_line = re.compile(
            r'^.+\t(\d+)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)')

        # Создаем списки для DataFrame
        y_s_list = []
        y_e_list = []
        x_s_list = []
        x_e_list = []
        t_s_list = []
        t_e_list = []

        with open(self.folder_path + "/" + path) as file:
            for line in file:
                if re.search(regex_line, line):
                    data = re.findall(regex_line, line)[0]
                    name = str(data[0])
                    t_s = float(data[1]) * (1 / self.fps) - self.t_p
                    t_e = float(data[2]) * (1 / self.fps) - self.t_p
                    x_s = float(data[3].replace(',', '.')) * self.dx - self.x_p
                    y_s = float(data[4].replace(',', '.')) * self.dx - self.y_p
                    x_e = float(data[5].replace(',', '.')) * self.dx - self.x_p
                    y_e = float(data[6].replace(',', '.')) * self.dx - self.y_p

                    y_s_list.append(y_s)
                    y_e_list.append(y_e)
                    x_s_list.append(x_s)
                    x_e_list.append(x_e)
                    t_s_list.append(t_s)
                    t_e_list.append(t_e)

        # Заполняем DataFrame
        self.df_line_points['x_s'] = x_s_list
        self.df_line_points['x_e'] = x_e_list
        self.df_line_points['y_s'] = y_s_list
        self.df_line_points['y_e'] = y_e_list
        self.df_line_points['t_s'] = t_s_list
        self.df_line_points['t_e'] = t_e_list

        return self.df_line_points



    def point_of_diametr(self, path):
        regex_d = re.compile(r'point\td\t(\d+)\t(-*\d+,*\d+)\t(-*\d+,*\d+)')
        diametr_x_list = [];
        diametr_y_list = [];
        t_list = []
        with open(self.folder_path + "/" + path) as file:
            for line in file:
                if re.search(regex_d, line):
                    data = re.findall(regex_d, line)[0]
                    t = float(data[0]) * (1 / self.fps)
                    x = float(data[1].replace(',', '.')) * self.dx
                    y = float(data[2].replace(',', '.')) * self.dx
                    diametr_x_list.append(x);
                    diametr_y_list.append(y);
                    t_list.append(t)
            unique, counts = np.unique(np.array(t_list), return_counts=True)
            duplicate_values = unique[counts > 1]
            mask = np.isin(t_list, duplicate_values)
            diametr_x_list = np.array(diametr_x_list)[mask];
            diametr_y_list = np.array(diametr_y_list)[mask]
        try:
            self.diametr = ((diametr_x_list[0] - diametr_x_list[1]) ** 2 + (
                        diametr_y_list[0] - diametr_y_list[1]) ** 2) ** (1 / 2)
        except:
            self.diametr = None

    def point_finder(self, path):
        regex_point = re.compile(r'^(point)\tcenter\t(\d+)\t(\d+,\d+)\t(\d+,\d+)')
        with open(self.folder_path + "/" + path) as file:
            for line in file:
                if re.search(regex_point, line):
                    data = re.findall(regex_point, line)[0]
                    self.t_p = float(data[1]) * (1 / self.fps)
                    self.x_p = float(data[2].replace(',', '.')) * self.dx
                    self.y_p = float(data[3].replace(',', '.')) * self.dx
                    break;

    ###################################### ЧТЕНИЕ ФАЙЛОВ ЗАКОНЧИЛОСЬ

    ##################################### КОНФИГ И ДРУГАЯ ЧЕПУХА
    def find_paths_to_files(self):
        regex_config_file = re.compile(r'config_file')
        regex_file = re.compile(r'.*F\d+.*\.dat')
        files_path = os.listdir(str(self.folder_path))
        files_path_np = np.array(files_path)
        files_config_mask = np.array([bool(re.match(regex_config_file, path)) for path in files_path])
        self.сonfig_file_path = str(list(files_path_np[files_config_mask])[0])
        files_path_mask = np.array([bool(re.match(regex_file, path)) for path in files_path])
        self.files_path = list(files_path_np[files_path_mask])

    def read_config_file(self):
        try:
            with open(self.folder_path + '/' + self.сonfig_file_path) as file:
                regex_config_file_info = re.compile(r'^(\w+)=(\d+.*\d*|\w+)')
                data = [re.findall(regex_config_file_info, line) for line in file]
                print(data)
                self.dx = float(data[0][0][1]) / 100  # м/кол-во пикселей
                self.fps = float(data[1][0][1])  # кадров/секунду
                self.type = str(data[2][0][1])
                self.rho = float(data[4][0][1])
                self.sigma = float(data[3][0][1])
                self.F = float(data[5][0][1])
        except Exception as e:
            print(e)

    ###################################### ФУНКЦИИ ДЛЯ РАСЧЕТОВ

    def __init__(self, folder_path):
        self.df = pd.DataFrame(
            columns=['times', 'thicknesses', 'Weber', 'velocities_x', 'velocities_y', 'velocities', 'diametr', 'sigma'])
        self.result = []
        self.x_p = None;
        self.y_p = None
        self.folder_path = folder_path
        self.find_paths_to_files()
        self.read_config_file()

        wind_velocities = [9.733314375061918, 11.516166220297418, 13.245244087133667, 14.945746089594333,
                           16.556265562066415, 18.08798016685125, 19.317571271139833, 20.626973582256667]
        name = [21, 25, 29, 33, 37, 41, 45, 49]
        velocity_by_F = dict(zip(name, wind_velocities))

        df = []

        for file in self.files_path:
            self.point_finder(file)  ##ищет центр первоначальный
            print(file)
            self.wind_velocity = velocity_by_F.get(int(self.F))
            df_points_of_gap = self.points_of_gap(file)  ##точки разрыва для последующей аппроксимации
            df_line_points =self.line_points(file)  ##достает траектории разрыва
            df_point_of_diametr = self.point_of_diametr(file)  ## характеристический размер бэга

            df_line_points['x_s'] = df_line_points['x_s'] - np.interp(df_line_points['t_s'], df_points_of_gap['t'], df_points_of_gap['x_r'])
            df_line_points['y_s'] = df_line_points['y_s'] - np.interp(df_line_points['t_s'], df_points_of_gap['t'], df_points_of_gap['y_r'])

            df_line_points['x_e'] = df_line_points['x_e'] - np.interp(df_line_points['t_s'], df_points_of_gap['t'], df_points_of_gap['x_r'])
            df_line_points['y_e'] = df_line_points['y_e'] - np.interp(df_line_points['t_s'], df_points_of_gap['t'], df_points_of_gap['y_r'])

            df_line_points['v_x'] = (df_line_points['x_e'] - df_line_points['x_s'])/(df_line_points['t_e'] - df_line_points['t_s'])
            df_line_points['v_y'] = (df_line_points['y_e'] - df_line_points['y_s'])/(df_line_points['t_e'] - df_line_points['t_s'])

            df_line_points['velocity'] = np.sqrt(df_line_points['v_x']**2 + df_line_points['v_y']**2)

            df_line_points['wind_velocity'] = self.wind_velocity
            
            df_line_points['t_average'] = (df_line_points['t_e'] + df_line_points['t_s'])/2
            df.append(df_line_points)

        self.df_array = pd.concat(df, ignore_index=True)