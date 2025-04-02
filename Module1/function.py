# -------------------------------------------
# импортирование библиотек
import librosa
import numpy as np


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

# TODO
# анализ данных:
# --------------------------------
# длина фраз, частота слов, анализ длительности, анализ шума, 
# фонетическое распределение - какие звуки чаще встречаются
# --------------------------------