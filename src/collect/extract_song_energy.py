import os
import librosa
import numpy as np
import soundfile as sf
from multiprocessing import Pool
from functools import partial

def calculate_energy(file_path, segment_duration=30):
    # 讀取音訊檔案
    y, sr = librosa.load(file_path, sr=None)
    
    # 計算短時能量，使用框架大小為一秒（sr個樣本），這樣計算出每秒的能量
    frame_length = sr
    hop_length = frame_length
    
    # 短時能量的簡單計算：每一幀的平方和
    energy = np.square(y)
    
    # 使用滑動窗口，計算每秒的總能量
    energy_per_frame = [np.sum(energy[i:i + frame_length]) for i in range(0, len(energy), hop_length)]
    
    # 找到能量最高的幾個幀
    max_energy_idx = np.argmax(energy_per_frame)
    start_sample = max_energy_idx * hop_length
    end_sample = start_sample + segment_duration * sr  # 30秒長度
    
    # 返回開始和結束時間點
    return start_sample, end_sample

def process_file(file_info, segment_duration=30):
    input_dir, output_dir, filename = file_info
    file_path = os.path.join(input_dir, filename)
    
    # 使用簡單的能量計算找到最強的片段
    start_sample, end_sample = calculate_energy(file_path, segment_duration)
    
    # 使用librosa從音訊文件讀取高能量區段
    y, sr = librosa.load(file_path, sr=None)
    high_energy_segment = y[start_sample:end_sample]
    
    # 使用soundfile儲存高能量片段
    output_filename = os.path.join(output_dir, filename)
    sf.write(output_filename, high_energy_segment, sr)
    
    print(f"Processed and saved high-energy segment for {filename}")
    return filename

def process_high_energy_segments_parallel(input_dir, output_dir, num_workers=6):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 準備每個MP3檔案的處理資訊
    file_infos = [(input_dir, output_dir, filename) for filename in os.listdir(input_dir) if filename.endswith(".mp3")]
    
    # 使用multiprocessing的imap進行並行處理
    with Pool(num_workers) as pool:
        for _ in pool.imap(partial(process_file, segment_duration=30), file_infos):
            pass


if __name__ == '__main__':
    # Paths
    input_dir = "../../data/raw_mp3"       # Directory containing original MP3 files
    output_dir = "../../data/processed_mp3"   # Directory to save processed 30s high-energy MP3s

    # Run the parallel processing function
    process_high_energy_segments_parallel(input_dir, output_dir, num_workers=6)
