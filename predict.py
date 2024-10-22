import os
import argparse
from glob import glob
from model import R2RNet
import torch,thop
import numpy as np
import torch.nn as nn
from IQA_pytorch import SSIM, MS_SSIM
# from utils import PSNR, validation, LossNetwork
parser = argparse.ArgumentParser(description='')
device = torch.device('cuda:0')
parser.add_argument('--gpu_id', dest='gpu_id',
                    default="0",
                    help='GPU ID (-1 for CPU)')
parser.add_argument('--data_dir', dest='data_dir',
                    default='./data/test/low',
                    # default='D:/lunwen2/SCI-main/SCI-main/data/medium',
                    #     default='D:/lunwen2/testdatasets/dicm',  #gai
                    help='directory storing the test data')
parser.add_argument('--ckpt_dir', dest='ckpt_dir',
                    default='./ckpts',
                    help='directory for checkpoints')
parser.add_argument('--res_dir1', dest='res_dir1',
                    default='./results/test/low/',
                    # default='./output/illu',
                    help='directory for saving the results')
parser.add_argument('--res_dir2', dest='res_dir2',
                    default='./results/test/low/',
                    # default='./output/deno',
                    help='directory for saving the results')
args = parser.parse_args()

class PSNR(nn.Module):
    def __init__(self, max_val=0):
        super().__init__()

        base10 = torch.log(torch.tensor(10.0))
        max_val = torch.tensor(max_val).float()

        self.register_buffer('base10', base10)
        self.register_buffer('max_val', 20 * torch.log(max_val) / base10)

    def __call__(self, a, b):
        mse = torch.mean((a.float() - b.float()) ** 2)

        if mse == 0:
            return 0

        return 10 * torch.log10((1.0 / mse))


def predict(model):

    test_low_data_names  = glob(args.data_dir + '/' + '*.*')
    test_low_data_names.sort()
    print(test_low_data_names)
    print('Number of evaluation images: %d' % len(test_low_data_names))


    model.predict(test_low_data_names,
                res_dir1=args.res_dir1,
                res_dir2=args.res_dir2,
                ckpt_dir=args.ckpt_dir,
    # eval_high_data_names=glob('D:/lunwen2/testdatasets/VV/*.jpg'))
    #               eval_high_data_names=glob('D:/lunwen2/testdatasets/MEF/*.png'))
    # eval_high_data_names=glob('D:/lunwen2/testdatasets/NPE/*.jpg'))#gai
    # eval_high_data_names=glob('D:/lunwen2/testdatasets/LIME/*bmp'))#gai
    # eval_high_data_names = glob('D:/lunwen2/testdatasets/dicm/*jpg'))  # gai
    #               eval_high_data_names=glob('D:/lunwen2/SCI-main/SCI-main/data/medium/*.jpg')+glob('D:/lunwen2/SCI-main/SCI-main/data/medium/*.png')+glob('D:/lunwen2/SCI-main/SCI-main/data/medium/*.bmp'))
                  eval_high_data_names = glob('./data/eval15/high/*.png'))
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # model = R2RNet().to(device)
    # inputs = torch.randn(1, 3, 256, 256)  ####(360,640)
    # inputs = inputs.to(device)
    # macs, params = thop.profile(model, inputs=(inputs,))  ##verbose=False
    # # summary = 'macs: %s -->' % (macs / 1e9) + '\n'
    #
    # # summary += '[%s] paramters: %s -->' % (k, human_format(param_num)) + '\n'
    # print('The number of MACs is %s' % (macs / 1e9))
    # print('The number of params is %s' % (params / 1e6))
    # summary = 'macs: %s -->' % (macs / 1e9) + '\n'

    # ssim_value = ssim(enhanced_img, high_img, as_loss=False).item()
    # psnr_value = psnr(enhanced_img, high_img).item()
    #




# with torch.no_grad():
#     for i, imgs in tqdm(enumerate(val_loader)):
#         #print(i)
#         low_img, high_img, name = imgs[0].cuda(), imgs[1].cuda(), str(imgs[2][0])
#         print(name)
#         # print(low_img)#[0.0863, 0.1176, 0.1216,  ..., 0.1137, 0.1176, 0.1098],
#         mul, add ,enhanced_img = model(low_img)
#         # print(mul)#[[[0.2916, 0.3582, 0.3714,  ..., 0.3485, 0.3422, 0.3108]
#         # print(add)#[0.5985, 0.6922, 0.6927,  ..., 0.6569, 0.6393, 0.5453]
#         # print(enhanced_img)#[0.4845, 0.5685, 0.5709,  ..., 0.5412, 0.5286, 0.4509],
#         if config.save:
#             torchvision.utils.save_image(enhanced_img, result_path + str(name) + '.png')
#
#         ssim_value = ssim(enhanced_img, high_img, as_loss=False).item()
#         psnr_value = psnr(enhanced_img, high_img).item()
#
#         ssim_list.append(ssim_value)
#         psnr_list.append(psnr_value)

if __name__ == '__main__':
    if args.gpu_id != "-1":
        # Create directories for saving the results
        if not os.path.exists(args.res_dir1):
            os.makedirs(args.res_dir1)
        if not os.path.exists(args.res_dir2):
            os.makedirs(args.res_dir2)
        # Setup the CUDA env
        os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_id
        # Create the model
        with torch.no_grad():
            model = R2RNet().to(device)
            # Test the model
            predict(model)
    else:
        # CPU mode not supported at the moment!
        raise NotImplementedError