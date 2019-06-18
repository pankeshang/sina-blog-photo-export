import os
import time
import requests
import lxml
import traceback
from lxml import etree

def analyze_blog(element, counter):
    name = element.tag.split('_')[1]
    dir_name = '{}_{}'.format(counter, name)
    os.makedirs(dir_name, exist_ok=True)
    counter = 0
    for x in element.iterchildren():
        print('x.tag={}'.format(x.tag))
        print('x.text={}'.format(x.text))
        image_name = x.tag
        image_url = x.text

        try:
            print('getting {} - {}...'.format(name, image_url))

            resp = requests.get(image_url)
            content_type = resp.headers.get('Content-Type', '/')
            extension = content_type.split('/')[1]
            target_filename = '{}/{}.{}'.format(dir_name, image_name, extension)
            print('target_filename = {}'.format(target_filename))

            with open(target_filename, 'wb') as f:
                f.write(resp.content)
            time.sleep(0.5)
        except KeyboardInterrupt:
            break
        except:
            traceback.print_exc()


def main(file_name, start_number):
    el = etree.parse(file_name)
    root = el.getroot()
    blogs = [i for i in root.iterchildren()]

    for counter, blog in enumerate(blogs[start_number:]):
        counter += start_number + 1
        analyze_blog(blog, counter)
        




if __name__ == '__main__':
    file_name = input('新浪相册链接XML文件路径：')
    start_number = input('起始数值：')
    if not start_number.isdigit():
        start_number = 0
    else:
        start_number = int(start_number)
    main(file_name, start_number)