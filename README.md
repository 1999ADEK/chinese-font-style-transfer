# Chinese Font Style Transfer

## Introduction
This project aims for transfering the style of a Chinese character with respect to an arbitray font style. The whole project is implemented based on a forked
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
 \# result img  
 Therefore, recognizability loss is added to solve the problem. One way is to match the content character and the output character in the image space.  
 \# formula  
 It ensure the character's identity, but sometimes the desired font style is lost due to the strong constraint of matching the two characters in the image space.  
 \# result img  
 Another way is to match the content character and the output character in the feature space. A pre-trained character classifier is used as a feature extractor to 
 compute the feature-matching loss of the content and the output character.  
 \# fomula  
 The identity of the character is retained.  
 \# result img   
 
 ## Train
 \# TODO
 
 ## Inference
 \# TODO
