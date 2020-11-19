import os
import time
from pathlib import Path
from src.downloader import Downloader, compose_local_file
from src.vmaf import VMAFHelper


def read_comparison_to_do(comparison_file_name='comparing_files.csv'):
    comparison_file = open(comparison_file_name)
    lines = comparison_file.readlines()[1:]  # skip heading
    comparisons = []
    for line in lines:
        try:
            comparisons.append(FileComparison(line))
        except TypeError as e:
            print("Type error when reading one line of the file")
            continue
    return comparisons


class FileComparison:
    def __init__(self, comparing_file_line):
        if not comparing_file_line or comparing_file_line == "":
            raise TypeError("Error: Comparing Line was empty")
        line_split = comparing_file_line.split(',')
        if len(line_split) < 4:
            raise TypeError(
                "Error: Comparing line is missing fields. Four fields necessary: id,path, source_file, encoded_file")
        self.id = line_split[0]
        self.source_file_s3_path = line_split[1].strip() + "/" + line_split[2].strip()
        self.encoded_file_s3_path = line_split[1].strip() + "/" + line_split[3].strip()


class VMAFFileResults:
    def __init__(self):
        self.filename = Path('./tmp/vmaf_result.csv')
        if self.filename.exists():
            os.renames('./tmp/vmaf_result.csv', './tmp/vmaf_result-' + str(time.time()) + '.csv')
        self.file = open('./tmp/vmaf_result.csv', 'w+')
        self.file.write('s3_source_file,s3_encoded_file,vmaf_average,vmaf_stdev,vmaf_min,vmaf_max')


    def append_line(self, line):
        self.file.write(line+'\n')


    def make_line(self, comparison, vmaf_data_point):
        return comparison.source_file_s3_path + ',' + comparison.encoded_file_s3_path \
               + ',' + str(vmaf_data_point.average) + ',' + str(vmaf_data_point.stdev) \
               + ',' + str(vmaf_data_point.min) + ',' + str(vmaf_data_point.max)


if __name__ == '__main__':
    comparisons = read_comparison_to_do()
    Downloader(comparisons).download_video_files()
    file_results = VMAFFileResults()
    for comparison in comparisons:
        source_file = compose_local_file(comparison.source_file_s3_path)
        encoded_file = compose_local_file(comparison.encoded_file_s3_path)
        vmaf_helper = VMAFHelper(source_file, encoded_file)
        vmaf_data_point = vmaf_helper.run_vmaf()
        result_line = file_results.make_line(comparison, vmaf_data_point)
        file_results.append_line(result_line)


