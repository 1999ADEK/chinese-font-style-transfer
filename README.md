# Chinese Font Style Transfer

## Introduction
This project aims for transfering the style of a Chinese character with respect to an arbitrary font style. The whole project is implemented based on a forked
version of [imaginaire](https://github.com/NVlabs/imaginaire). 

## Experiment Details
- **Network Structure**  
  The structure is based on [COCO-FUNIT: Few-Shot Unsupervised Image Translation with a Content Conditioned Style Encoder](https://arxiv.org/abs/2007.07431). 
  An additional recognizability loss is added to the training loss to ensure character recognizability. See the Results section for more details.
- **Datasets**  
  The datasets consists of 30 different Chinese fonts. Each font generates the same 3494 characters 
  of size 256x256 from the [character set](https://blog.csdn.net/u011762313/article/details/47419063) of commonly used Chinese characters. 
  The source fonts are downloaded from [字体天下](http://www.fonts.net.cn/).  
  
## Results  
With the original COCO-FUNIT implementation, the output character often fails to retain the identity, that is, it fails to be recognized as the same character
as the content input.  
<p align="center">
  <img src="imgs/result_original.png" alt="result_original.png", width="200"/>
</p>
Therefore, recognizability loss is added to solve the problem. One way is to match the content character and the output character in the image space.  
<p align="center">
  <img src="https://latex.codecogs.com/png.latex?L_%7Brecog%7D%20%3D%20%7B%5ClVert%20I_%7Bcontent%7D%20-%20I_%7Boutput%7D%20%5CrVert%7D_1" alt="equation", width="200"/>
</p>
It ensures the character's identity, but sometimes the desired font style is lost due to the strong constraint of matching the two characters in the image space.  
<p align="center">
  <img src="imgs/result_image_matching.png" alt="result_image_matching.png", width="200"/>
</p>
Another way is to match the content character and the output character in the feature space. A pre-trained character classifier is used as a feature extractor to 
compute the feature-matching loss of the content and the output character.   
<p align="center">
  <img src="https://latex.codecogs.com/png.latex?L_%7Brecog%7D%20%3D%20%7B%5ClVert%20f%28I_%7Bcontent%7D%29%20-%20f%28I_%7Boutput%7D%29%20%5CrVert%7D_1" alt="equation", width="230"/>
</p>
The identity of the character is retained.  
<p align="center">
  <img src="imgs/result_feature_matching.png" alt="result_feature_matching.png", width="200"/>
</p> 

## Train 
First put any font types you like under the folder `dataset/font_train` and then modify the file `dataset/font_file_train.json` according to the font types. Use the following command to generate training dataset.
```bash
bash scripts/gen_font_train_data.sh
```  
After specifying the training setting by modifying the file `configs/config.yaml`, train your model by  
```bash
python train.py \
--config configs/config.yaml \
--logdir logs
```
 
## Inference
First put any font types you like under the folder `dataset/font_test` and then modify the file `dataset/font_file_test.json` according to the font types. Use the following command to generate testing data.
```bash
bash scripts/gen_font_test_data.sh
```  
After specifying the testing setting by modifying the file `configs/config.yaml`, test your model by  
```bash
python inference.py \
--config configs/config.yaml \
--checkpoint checkpoint.pth \
--output_dir result
```
A pretrained model can be downloaded by 
```bash
bash scripts/download_model.sh
```  
