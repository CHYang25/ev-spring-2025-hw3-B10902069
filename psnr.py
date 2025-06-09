from PIL import Image
import numpy as np
import os
import click
import matplotlib.pyplot as plt 


def psnr(img1: np.ndarray, img2: np.ndarray):
    mse = np.mean((img1 - img2)**2)
    if mse == 0:
        return float('inf')
    else:
        return 20 * np.log10(255/np.sqrt(mse))
    
@click.command()
@click.option('-v1', '--video1', type=str, required=True)
@click.option('-v2', '--video2', type=str, required=True)
@click.option('-p', '--plot', type=str, required=True)
def main(video1, video2, plot):
    
    assert os.path.isdir(video1) and os.path.isdir(video2), "Video path not exists"

    frames1 = sorted(os.listdir(video1))
    frames2 = sorted(os.listdir(video2))
    psnrs = []

    for img1, img2 in zip(frames1, frames2):

        if 'mp4' in img1 or 'mp4' in img2:
            continue

        arr1 = np.array(Image.open(os.path.join(video1, img1)))
        arr2 = np.array(Image.open(os.path.join(video2, img2)))
        psnrs.append(psnr(arr1, arr2))

    plt.figure(figsize=(10, 5))
    plt.plot(list(range(len(frames1)-1)), psnrs, marker='o')
    plt.title("PSNR between Frames")
    plt.xlabel("Frame Index")
    plt.ylabel("PSNR (dB)")
    plt.grid(True)
    plt.tight_layout()
    assert plot[-4:] == '.png', "You shall include the extension png."
    plt.savefig(os.path.join('./plots', plot))

if __name__ == '__main__':
    main()