# Data folder policy

- `raw/`: original public data files, immutable once downloaded.
- `derived/`: standardised/public derivatives and FinanceOps synthetic workbooks.
- `gold/`: hidden evaluation answers, reference scripts and corruption master key. Never index or include this directory in model context.
- `questions_dev.jsonl`: exactly 20 development question-workbook tasks.
- `questions_test.jsonl`: exactly 80 frozen held-out tasks.

Person 1 must source the full Sample Superstore dataset and original UCI Online Retail.xlsx, record the exact URL, retrieval date, licence notice, SHA-256, and verified row count in `data_manifest.json`.

Required sample sources:
- Sample Superstore: https://gist.github.com/SharmaAshwini/8bd642f6c46792a9c40c8ccad60391e9
- UCI Online Retail: https://archive.ics.uci.edu/dataset/352/online+retail

Online Retail has invoice/cancellation data but no profit or cost fields. Do not create profit gold answers for it.
