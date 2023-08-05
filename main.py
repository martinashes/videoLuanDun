import os
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip


def compose_viedo(background_image, video_file, head_image, filename):
    # Step 1: 获取video1.mp4的时长
    video_duration = VideoFileClip(video_file).duration

    # Step 2: 新建一个1080*1920的视频，并设置背景为background1.jpg
    video_size = (1080, 1920)
    background_clip = ImageClip(background_image).set_duration(video_duration).resize(video_size)

    # Step 3: 导入video1.mp4，裁剪并放置在（0，650）的位置
    video_clip = VideoFileClip(video_file).crop(x1=0, y1=650, x2=1080, y2=1250).set_position((0, 650))

    # Step 4: 导入head1.png放置于（0，160）的位置
    head_clip = ImageClip(head_image).set_duration(video_duration).set_position((0, 60))

    # Step 5: 导入video1.mp4，裁剪并放置在（0，650）的位置
    video_clip2 = VideoFileClip(video_file).crop(x1=0, y1=1410, x2=1080, y2=1510).set_position((0, 1410))

    # 创建合成视频
    final_clip = CompositeVideoClip([background_clip, video_clip, head_clip, video_clip2])

    # 确保输出文件夹存在
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # 生成视频文件
    output_path = os.path.join(output_folder, filename)
    final_clip.write_videofile(output_path, fps=30, codec='libx264', preset='ultrafast', threads=10,
                               ffmpeg_params=['-threads', '12'])


def main():
    video_file_pack = get_files_with_extension('./viedo', 'mp4')
    head_pack = get_files_with_extension('./head', 'png')
    background_img_pack = get_files_with_extension('./background', 'jpg')
    j = 1

    for video_file in video_file_pack:
        for background_image in background_img_pack:
            i = video_file_pack.index(video_file)
            head_image = head_pack[i]
            filename = 'video00' + str(j) + '.mp4'
            compose_viedo(background_image, video_file, head_image, filename)
            j = j + 1


def get_files_with_extension(directory, extension):
    """
    Get a list of file names in the specified directory with the given extension.

    Parameters:
        directory (str): The path to the directory to search for files.
        extension (str): The file extension to filter the files (e.g., '.txt', '.jpg').

    Returns:
        List[str]: A list of file names with the specified extension.
    """
    file_names = []
    for file in os.listdir(directory):
        if file.endswith(extension):
            file_names.append(file)
    return file_names
