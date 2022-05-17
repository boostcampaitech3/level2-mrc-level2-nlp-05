# Boostcamp AI Tech 3기: NLP-05-외않되조

---

# Project: Open-Domain Question Answering

- Wrap-up Report : [NLP_5조_ODQA_wrap-up_report.pdf](https://github.com/boostcampaitech3/level2-mrc-level2-nlp-05/files/8709416/NLP_5._ODQA_wrap-up_report.pdf)

## Members

| 이름    | Github Profile | 역할 |
| ---    | --- | --- |
| 공통   |  | EDA, git, baseline code debugging |
| 강나경 | [angieKang](https://github.com/angieKang) | ideas, title+context, ensemble |
| 김산   | [mounKim](https://github.com/mounKim) | data augmentation, back translation |
| 김현지 | [TB2715](https://github.com/TB2715) | 환경설정, top-k 수정, back translation |
| 정민지 | [minji2744](https://github.com/minji2744) | dense passage retrieval, bm25, data 추가해서 훈련 |
| 최지연 | [jeeyeon51](https://github.com/jeeyeon51) | top-k 수정, retriever doc score + reader score 방식 시도 |

## 문제 개요
<img width="1980" alt="문제 정의" src="https://user-images.githubusercontent.com/59854630/168844994-1a226d63-e75e-47c6-b1ac-475d2eff8e69.png">

본 프로젝트에서는 궁금한 것이 생겼을 때 구글링으로 답을 찾는 것과 유사한 시스템을 만들어보고자, Open Domain Question Answering(ODQA) 태스크를 수행했습니다.   
QA는 질문에 대한 답을 내는 인공지능 모델을 만드는 연구 분야입니다. 여기에 지문이 주어지고 답을 찾는 것이 아니라, 사전에 구축해 둔 지식 데이터베이스에서 질문과 관련이 있는 문서를 찾고 답을 아웃풋하는 것이 ODQA 태스크입니다.     
ODQA를 수행하기 위해서 retriever-reader 구조를 가지는 two-stage 모델 구조를 사용했습니다. retriever는 질문과 관련된 문서들을 찾아오는 단계이며, 다음으로는 찾아온 문서들을 읽고 질문에 대한 답을 찾거나 만드는 reader 단계입니다. 두 단계의 모델을 구성하고 훈련한 후 두 단계를 연결하고 통합하는 과정을 통해 태스크 수행이 가능합니다. 

## 프로젝트 수행 절차 및 방법

<img width="1590" alt="프로젝트수행" src="https://user-images.githubusercontent.com/59854630/168845131-0c9f0a98-b179-4568-a3b6-7fc7b4491a7a.png">

### MODELS
- Retriever
    - Sparse retrieval: tf-idf, bm25
    - Dense passage retrieval
    - Passage: title + context
- Linking MRC and retrieval
    - Doc score
- Reader
    - klue/bert-base
    - klue/roberta-large

## 데이터셋 구조

- `id`: 질문의 고유 id
- `question`: 질문
- `answers`: 답변에 대한 정보. 하나의 질문에 하나의 답변만 존재함
  - `answer_start`: 답변의 시작 위치
  - `text`: 답변의 텍스트
- `context`: 답변이 포함된 문서
- `title`: 문서의 제목
- `document_id`: 문서의 고유 id
    

## 실험 결과

### 리더보드 (대회 진행)

<img width="1075" alt="대회 진행" src="https://user-images.githubusercontent.com/59854630/168845985-22c4aa3a-f0f0-4a2b-910c-2083f090e8b4.png">

- EM: 55.8300
- F1: 66.5900

### 리더보드 (최종)

<img width="1074" alt="최종" src="https://user-images.githubusercontent.com/59854630/168846029-c1841110-1553-40ae-ab79-551a6c8867fb.png">

- EM: 50.0000
- F1: 61.3300

## Requirements

> Confirmed that it runs on Ubuntu 18.04.5, Python  3.8, and pytorch 1.10.2
> 

필요한 패키지들은 `/code/install/install_requirements.sh` 에서 확인하실 수 있습니다.



## Getting Started

### 1. 코드 구조
- **retrieval.py** : retreiver 모듈
- **arguments.py** : 실행되는 모든 argument가 dataclass의 형태로 저장됨
- **trainer_qa.py** : MRC 모델 학습시 필요한 trainer 제공
- **utils_qa.py** : 기타 유틸 함수 제공
- **train.py** : MRC, Retrieval 모델 학습 및 평가
- **inference.py** : ODQA 모델 평가

### 2. 코드 실행 방법
1. 학습 방법   
  arguments에 대한 세팅은 `arguments.py`에서 진행합니다.       
  `python train.py --output_dir ./models/train_dataset --do_train`
2. 평가 방법    
   - 훈련과 평가를 동시에 진행: `python train.py --output_dir ./models/train_dataset --do_train --do_eval`     
   - MRC 모델의 평가: `python train.py --output_dir ./outputs/train_dataset --model_name_or_path ./models/train_dataset/ --do_eval `
3. 추론 방법   
  `python inference.py --output_dir ./outputs/test_dataset/ --dataset_name ../data/test_dataset/ --model_name_or_path ./models/train_dataset/ --do_predict`
