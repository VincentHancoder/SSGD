import json
import argparse
# import funcy
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, StratifiedKFold
import os
import numpy as np
from pathlib import Path
from tqdm import tqdm


def save_coco(file, images, annotations, categories):
    with open(file, 'wt', encoding='UTF-8') as coco:
        json.dump({'images': images, 'annotations': annotations, 'categories': categories}, coco, indent=2)

def read_json(json_file):
    with open(json_file, 'r') as r:
        data = json.load(r)
    return data

def split_data(file_name, k=3):
    data = read_json(file_name)
    image_infos = data['images']
    ann_infos = data['annotations']
    category_info = data['categories']
    
    # make hashing tree {image_id: [ann]}
    hashing_ann = dict()
    for ann_info in ann_infos:
        img_id = ann_info['image_id']
        if hashing_ann.get(img_id, None) is None:
            hashing_ann[img_id] = []
        hashing_ann[img_id].append(ann_info)
    
    # single class ; X = image_infos, Y = class
    img_index = []
    target = []
    for img_info in image_infos:
        img_id = img_info['id']
        img_index.append(img_id)
        if hashing_ann.get(img_id, None) is None:
            target.append(0)
        else:
            category = hashing_ann[img_id][0]['category_id']
            target.append(category)
    
    # split
    img_index = np.array(img_index)
    skf = StratifiedKFold(n_splits=5, random_state=0, shuffle=True)
    n = 1
    for train_index, test_index in tqdm(skf.split(img_index, target)):
        train_img_info = obtain(image_infos, train_index)
        train_img_ann = get_ann_from_having_ann(train_img_info, hashing_ann)
        train_save_file = os.path.join(Path(file_name).parent, 'train'+str(n)+'.json')
        save_coco(file=train_save_file, images=train_img_info, annotations=train_img_ann, categories=category_info)
        test_img_info = obtain(image_infos, test_index)
        test_img_ann = get_ann_from_having_ann(test_img_info, hashing_ann)
        test_save_file = os.path.join(Path(file_name).parent, 'val'+str(n)+'.json')
        save_coco(file=test_save_file, images=test_img_info, annotations=test_img_ann, categories=category_info)        
        n += 1
    
    return None

def obtain(data, index_list):
    output = [data[x-1] for x in index_list]
    return output

def get_ann_from_having_ann(img_infos, hashing_ann):
    output = []
    for x in img_infos:
        if hashing_ann.get(x['id'], None) is None:
            continue
        # print(x['id'])
        # print(hashing_ann[x['id']])
        output += hashing_ann[x['id']]
    return output

if __name__ == "__main__":
    split_data('/home/yr2/project/mmdetection_2_25_0/data/defect_screen/annotations/lb201/lb201.json')
    print('Done!')
