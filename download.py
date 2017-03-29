import os
import requests

# 需要找到存放个某个用户视频和图片链接的路径
user_name = 'syz3'
image_dir = user_name + '_images/'
video_dir = user_name + '_videos/'
# 存放图片和视频的文件
image_links_file = image_dir + 'images.txt'
video_links_file = video_dir + 'videos.txt'
# 存放第一次运行时 已经下载的文件个数的文件
process_image_file_name = 'process_image.txt'
process_video_file_name = 'process_video.txt'


# 根据url和第i个，下载视频和图片
def download_video(i, url):
    video_name = str(i) + '.mp4'
    print('下载第' + str(i) + '个视频……')
    video_res = requests.get(url, stream=True)
    # 使用wb，写入二进制文件
    with open(video_dir + video_name, 'wb') as f:
        f.write(video_res.content)
    print('第' + str(i) + '个视频下载完成。')


# 比video多一个img_type，有的是jpg，有的是gif
def download_img(i, img_type, url):
    img_name = str(i) + img_type
    print('下载第' + str(i) + '张图片……')
    img_res = requests.get(url, stream=True)
    with open(image_dir + img_name, 'wb') as f:
        f.write(img_res.content)
        print('第' + str(i) + '张图片下载完成。')


# 读取已经下载了多少个文件。
# 主要是因为第一次下载时，有很多个。可能下载到一半就莫名崩溃，
# 所以每下载一个文件，就存下当前一共下载了多少文件，
# 崩溃了，再运行时，不用从头下载了。
def read_x_process(x_dir, file_name):
    if os.path.isfile(x_dir + file_name):
        with open(x_dir + file_name, 'r') as f:
            done_count = f.read()
            print('目前已经下载了' + done_count + '个。')
            return done_count
    else:
        with open(x_dir + file_name, 'w') as f:
            print('目前已经下载了0个。')
            return '0'


def read_process(type):
    if(type == 'image'):
        file_name = process_image_file_name
        return read_x_process(image_dir, file_name)
    else:
        file_name = process_video_file_name
        return read_x_process(video_dir, file_name)


def save_x_process(x_dir, file_name, i):
    with open(x_dir + file_name, 'w') as f:
        f.write(str(i))
        print("已完成" + str(i) + '个。')


def save_process(i, type):
    if type == 'image':
        file_name = process_image_file_name
        save_x_process(image_dir, file_name, i)
    else:
        file_name = process_video_file_name
        save_x_process(video_dir, file_name, i)


# 把保存的链接都下载完后，将下载的个数存在last_num.txt中
# 需要根据相应的存放链接的文件
def save_x_download_num(links_file, x_dir):
    num = 0
    with open(links_file) as f:
        for line in f.readlines():
            num = num + 1
    with open(x_dir + 'last_num.txt', 'w') as f:
        f.write(str(num))


def save_download_num(type):
    if type == 'image':
        save_x_download_num(image_links_file, image_dir)
    else:
        save_x_download_num(video_links_file, video_dir)


# 下载视频，先读取已经下载的个数（第一次运行时，又可能崩溃）。
i = int(read_process('video'))
with open(video_links_file) as f:
    # 这里就是从上一次崩溃的地方开始读取
    for line in f.readlines()[i:]:
        link = line.strip()
        print(link)
        # 根据i和url去下载
        download_video(i, link)
        i = i + 1
        # 每下载一个，就要更新已处理的文件process_video.txt
        save_process(i, 'video')
# 整个video.txt中的链接都下载完了（若是崩溃了，就不会执行后边的语句了）
# 所以save_download_num函数一定是将所有视频链接都下载了之后才会执行的
# 保存的也是第一次执行时video.txt中链接个数
save_download_num('video')


# 同上，下载图片过程和下载视频过程几乎一样，多一个img_type
j = int(read_process('image'))
with open(image_links_file) as f:
    for line in f.readlines()[j:]:
        link = line.strip()
        print(link)
        img_type = link[-4:]
        download_img(j, img_type, link)
        j = j + 1
        save_process(j, 'image')
save_download_num('image')
