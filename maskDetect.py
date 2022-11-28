import argparse
import torch
from sys import platform

from yolov3.models import Darknet, attempt_download
from yolov3.utils.datasets import LoadImages
from yolov3.utils.utils import *


class MaskDetector:
    def __init__(self, weights, output_folder):
        self.img_size = 416
        self.model = Darknet('yolov3/cfg/yolov3-spp.cfg', self.img_size)
        self.out = output_folder

        self.device = 'cpu'
        attempt_download(weights)
        self.model.load_state_dict(torch.load(weights, map_location=self.device)['model'])
        self.names = ['mask', 'no-mask']
        self.colors = [[30, 200, 30], [30, 30, 200]]

    def reset_output_folder(self):
        if os.path.exists(self.out):
            shutil.rmtree(self.out)  # delete output folder
        os.makedirs(self.out)  # make new output folder

    def detect_mask(self, image):
        self.model.to(self.device).eval()
        dataset = LoadImages(image, img_size=self.img_size)
        im0 = None
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(self.device)
            img = img.float()
            img /= 255.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)
                prediction = self.model(img)[0]
                prediction = non_max_suppression(prediction, 0.3, 0.6, agnostic=False)

                for i, det in enumerate(prediction):
                    p, im0 = path, im0s

                    save_path = str(Path(self.out) / Path(p).name)

                    if det is not None and len(det):
                        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                        for *xyxy, conf, cls in det:
                            label = '%s %.2f' % (self.names[int(cls)], conf)
                            plot_one_box(xyxy, im0, label=label, color=self.colors[int(cls)])

                    if dataset.mode == 'images':
                        cv2.imwrite(save_path, im0)
        return im0

