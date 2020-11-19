
The goal of this script is calculating the VMAF score for a given video pair.
VMAF score is an indicator of the visual quality of an encoded video. 

It helps to measure the encoding templates, and therefore have a baseline to
drive encoding changes.

The script expects the videos, original and encoded version,  to be in an s3 bucket.

## Usage

1) Create a file named `comparing_files.csv` at the root of the project.
   The file follows below format:
   
   ```
    id,path, source_file, encoded_file
    1, 394/ip_instance,video_394_source.mp4,video_394_360p.mp4
    2, 394/ip_instance,video_394_source.mp4,video_394_480p.mp4

   ```
   
2) Open the `downloader.py` file and enter the s3 bucket that contains the videos, aws region, and a pair access key and secret access key with permissions to access the bucket. 

    Lines to replace:
    
    ```
   RECORDINGS_BUCKET_NAME = '<REPLACE WITH S3 BUCKET>'
   ```
   
   ```
   os.environ["AWS_DEFAULT_REGION"] = '<REPLACE_WITH_REGION>'
   os.environ["AWS_ACCESS_KEY_ID"] = '<REPLACE WITH ACCESS_KEY_ID THAT HAS ACCESS TO THE ABOVE BUCKET>'
   os.environ["AWS_SECRET_ACCESS_KEY"] = '<<REPLACE WITH SECRET_ACCESS_KEY>'
   ```

3) Run the script as follows:
    
    Requirements: 
     * Python 3
     * Virtualenv (Install it executing the following: `pip3 install virtualenv`)
        
   3.1) Create the virtual environment:
        `python3 -m venv venv`
        
   3.2) Activate the virtual environment:
        `source venv/bin/activate`
   
   3.3) Install python dependencies:
        `pip -r install requirements.txt`
        
   3.4) Run the main script:
        `python main.py`
        
4) The script will download the video files from s3 and save them in 
    a `./tmp` folder. Also within the `./tmp` folder, it will create a file named `vmaf_result.csv` containing the VMAF results. The file follows the below format:
     
     | s3_source_file | s3_encoded_file | vmaf_average | vmaf_stdev | vmaf_min | vmaf_max |
     |----------------|-----------------|--------------|------------|----------|----------|
     |s3_path/video_394_source.mp4|s3_path/video_394_360p.mp4|0.5934425942700652|0.4905720658824808|0.0|2.7422|
     |s3-path/video_394_source.mp4|s3_path/video_394_480p.mp4|0.6660551232357278|0.5191834959062602|0.0|2.8167|

    
    
