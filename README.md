# RMP Dataset Creator

## Overview

A python program that call upon the RMP API and create a dataset of prompts and answers to be used for training a llama 2 model.

## Features

- Outputs CSV file with 2 columns, one for prompts and one for answers.
- Takes in file of input prompts with structure similar to the below examples and will construct prompts from RMP data

EX)  
input:  
"Who is the best Professor for {ClassName}"  

output:  
Prompts  
"Who is the best Professor for CS 111"  
"Who is the best Professor for CS 112"  
"Who is the best Professor for CS 113"  
...  

Answers  
"The best professor for CS 111 is Jason Smith"
"The best professor for CS 112 is Bob Jones"
"The best professor for CS 113 is Jason Smith"
...




##Websscarping API Documentation:  
https://github.com/Nobelz/RateMyProfessorAPI




     
