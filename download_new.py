import os
# from download import download_video
# from download import download_img
import requests

user_name = 'syz'
image_dir = user_name + '_images/'
video_dir = user_name + '_videos/'


# 这两个下载的代码 和 上边的变量与download.py中的都一样
# 但是import download，download.py会新执行一次。
def download_video(i, url):
    video_name = str(i) + '.mp4'
    print('下载第' + str(i) + '个视频……')
    video_res = requests.get(url, stream=True)
    with open(user_name + '_videos/' + video_name, 'wb') as f:
        f.write(video_res.content)
    print('第' + str(i) + '个视频下载完成。')


def download_img(i, img_type, url):
    img_name = str(i) + img_type
    print('下载第' + str(i) + '张图片……')
    img_res = requests.get(url, stream=True)
    with open(user_name + '_images/' + img_name, 'wb') as f:
        f.write(img_res.content)
        print('第' + str(i) + '张图片下载完成。')


# 获取上一次的下载的个数
def get_last_num(x_dir):
    if os.path.isfile(x_dir + 'last_num.txt'):
        with open(x_dir + 'last_num.txt', 'r') as f:
            last_num = f.read()
            print('之前已经下载了' + last_num + '个。')
            return last_num
    else:
        with open(x_dir + 'last_num.txt', 'w') as f:
            print('之前一个也没有下载了。')
            return '0'


# 这一次又可能新下载了一些。更新已下载的个数
def update_last_num(x_dir, num):
    with open(x_dir + 'last_num.txt', 'w') as f:
        f.write(str(num))


# 下载新的连接时，要先获取上一次已经下载的个数
last_num_video = int(get_last_num(video_dir))
# 再获取这一次一共有多少链接
new_num_video = 0
with open(video_dir + 'videos.txt') as f:
    for line in f.readlines():
        new_num_video = new_num_video + 1
print('目前共有' + str(new_num_video) + '个视频。')
# 根据新旧链接的个数，判断要不要下载新的
if new_num_video > last_num_video:
    i = last_num_video + 1
    with open(video_dir + 'videos.txt') as f:
        # 新增的链接就是在 0 至 new - old之间
        for line in f.readlines()[0: new_num_video - last_num_video]:
            link = line.strip()
            print(link)
            download_video(i, link)
            i = i + 1
    update_last_num(video_dir, new_num_video)
elif new_num_video == last_num_video:
    print('没有新增的视频')
elif new_num_video < last_num_video:
    print('你是不是删掉了一些视频链接？')


# 下载图片和下载视频一样
last_num_image = int(get_last_num(image_dir))
new_num_image = 0
with open(image_dir + 'images.txt') as f:
    for line in f.readlines():
        new_num_image = new_num_image + 1
print('目前共有' + str(new_num_image) + '张图片。')

if new_num_image > last_num_image:
    j = last_num_image + 1
    with open(image_dir + 'images.txt') as f:
        for line in f.readlines()[0: new_num_image - last_num_image]:
            link = line.strip()
            print(link)
            img_type = link[-4:]
            download_img(j, img_type, link)
            j = j + 1
    update_last_num(image_dir, new_num_image)
elif new_num_image == last_num_image:
    print('没有新增的图片')
elif new_num_image < last_num_image:
    print('你是不是删掉了一些图片链接？')
