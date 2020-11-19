import time
import os
import numpy as np
from ffmpeg_quality_metrics.__main__ import calc_vmaf, get_brewed_model_path, calculate_global_stats


class VMAFDataPoint:
    def __init__(self, vmaf_data_dict):
        self.average = vmaf_data_dict['average']
        self.stdev = vmaf_data_dict['stdev']
        self.min = vmaf_data_dict['min']
        self.max = vmaf_data_dict['max']


def extract_vmaf_global_info(vmaf_data_dict):
    data_point = VMAFDataPoint(vmaf_data_dict)
    return data_point


def calculate_global(data):
    values = [float(entry['vmaf']) for entry in data]
    global_stats = {
        "average": np.average(values),
        "stdev": np.std(values),
        "min": np.min(values),
        "max": np.max(values),
    }

    return global_stats


class VMAFHelper:
    def __init__(self, source_file_path, encoded_file_path):
        self.source_file_path = source_file_path
        self.encoded_file_path = encoded_file_path

    def run_vmaf(self):
        print('Start VMF calculation for :' + self.source_file_path + ' and ' + self.encoded_file_path)
        start_time = time.time()
        model_path = os.path.join(get_brewed_model_path(), "vmaf_v0.6.1.pkl")
        framerate = 60
        vmaf_data = calc_vmaf(self.encoded_file_path, self.source_file_path, model_path, "bicubic", False, framerate)
        vmaf_data_global = calculate_global(vmaf_data)
        total_time = time.time() - start_time
        print('Total time: ' + str(total_time))
        return extract_vmaf_global_info(vmaf_data_global)
