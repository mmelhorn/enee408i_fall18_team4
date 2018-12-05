#!/bin/bash
#Make executable with chmod u+x scriptname

xterm -hold -e  ~/Documents/enee408i_fall18_team4-master/ngrok http 5000 

python ~/Desktop/enee408i_fall18_team4/opencv-face-recognition/extract_embeddings.py --dataset dataset --embeddings output/embeddings.pickle --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7

python ~/Desktop/enee408i_fall18_team4/opencv-face-recognition/train_model.py --embeddings ~/Desktop/enee408i_fall18_team4/opencv-face-recognition/output/embeddings.pickle --recognizer ~/Desktop/enee408i_fall18_team4/opencv-face-recognition/output/recognizer.pickle --le ~/Desktop/enee408i_fall18_team4/opencv-face-recognition/output/le.pickle
