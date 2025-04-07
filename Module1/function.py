# -------------------------------------------
# импортирование библиотек
import librosa
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------------------
# реализация функций

# функция для передискретизации данных
def resample_audio(sample, 
                   array_col: str = 'array', 
                   sr_col: str = 'sampling_rate',
                   target_sr: int = 16000
                   ):
    # получаем временной ряд звука 
    # и изначальную частоту дискретизации
    array, orig_sr = sample[array_col], sample[sr_col]
    # проверяем, надо ли менять частоту выборки
    if orig_sr != target_sr:
        # меняем частоту выборки у записи
        array = librosa.resample(np.array(array), orig_sr=orig_sr, target_sr=target_sr)
    # возвращаем новые значения
    return {'array': array, 'sampling_rate': target_sr}

# функция для создания 2х графиков по признаку
def wave_hist_plot(main_title, df, col, title1, x_label1, y_label1, title2, x_label2, y_label2):    
    # создаем фигуру с двумя subplots 
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # график 1
    df[col].plot(ax=ax1)                           # график   
    ax1.set_title(title1)                          # название
    ax1.set_xlabel(x_label1)                       # ось х
    ax1.set_ylabel(y_label1)                       # ось у

    # график 2
    sns.histplot(df[col], bins=50, kde=True, ax=ax2)        # график
    ax2.set_title(title2)                                   # название
    ax2.set_xlabel(x_label2)                                # ось х
    ax2.set_ylabel(y_label2)                               # ось у

    # заголовок
    plt.suptitle(main_title, fontsize=16)

    # отображение графика
    plt.tight_layout()
    plt.show()

# функция для вычисления SNR (Signal-to-Noise-Ratio)
def calculate_snr(y, silence_threshold=0.01):
    # находим тихие участки (шум)
    silent_regions = np.where(np.abs(y) < silence_threshold)[0]
    
    if len(silent_regions) == 0:
        return np.nan  # если нет тихих учаcтков
    
    # мощность шума (по тихим участкам)
    P_noise = np.mean(y[silent_regions]**2)
    # если мощность шума почти 0
    if P_noise < 1e-10:
        return np.nan
    
    # мощность всего сигнала
    P_signal = np.mean(y**2)
    
    return 10 * np.log10(P_signal / P_noise)


# функция для передискретизации данных
def resample_audio(row, target_sr=16000):
    '''
    Передискретизирует аудиомассив из row['array'] 
    с исходной частотой row['sampling_rate'] на target_sr
    '''
    # если частота уже целевая - возвращаем как есть
    if row['sampling_rate'] == target_sr:
        return row['array']
    
    # передискретизация
    resampled = librosa.resample(
        y=row['array'],
        orig_sr=row['sampling_rate'],
        target_sr=target_sr
    )
    
    # для сохранения типа данных как в исходном массиве
    return resampled.astype(row['array'].dtype)

# функция для извлечения mel-спектрограмм
def extract_mel(sample):
    pass

# TODO
# анализ данных:
# --------------------------------
# длина фраз, частота слов, анализ длительности, анализ шума, 
# фонетическое распределение - какие звуки чаще встречаются
# --------------------------------