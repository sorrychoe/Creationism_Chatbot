# 한동대학교 창조와 진화 질의응답 Chatbot With LLM

```bash
├── Makefile
├── README.md
├── api
│   └── __init__.py
├── data
│   └── __init__.py
├── db
│   └── __init__.py
├── model
│   ├── __init__.py
│   └── doc.py
├── requirements.txt
├── crawler.py
├── main.py
└── vector_store.py
```

## How to Run?

1. 초기 설정은 다음 코드를 터미널에 입력을 통해 진행할 수 있습니다.
## Installation

해당 프로그램은 Makefile을 통해 간편하게 설치할 수 있습니다.

```bash
  make init
```

Make가 없는 경우(Especially Window), 별도로 설치가 필요합니다.
- [Make.exe install](https://gnuwin32.sourceforge.net/packages/make.htm)

또한, OPENAI API를 보유하고 있어야 합니다. OPENAI API는 api 디렉토리에서 tokens.py라는 파일을 만든 후에, 해당 폴더에 입력해주세요.

tokens.py의 안에는 다음과 같이 코드를 작성해주세요. 그리고 `{OPENAI API}`라고 적힌 칸에 API Key를 기입해주세요.

```python
import os

os.environ['OPENAI_API_KEY']="{OPENAI API}"
```


2. 그 후 다음 코드를 통해 데이터를 수집 및 전처리를 진행해주세요. 시간이 다소 소요되니, 그동안 기다려주세요.

```bash
make crawling
```

3. 마지막으로, 터미널에 다음과 같이 입력해주세요. 그러면 최종적인 결과를 확인할 수 있습니다.

```bash
make run
```

## you have some issue?

사용하다 문제 발생 시, github 상단 이슈란에 등록해주세요.

## Authors

- [@sorrychoe](https://www.github.com/sorrychoe)
