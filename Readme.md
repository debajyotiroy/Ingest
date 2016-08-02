Delete unwanted files from Staging using (example for pdf):
`find . -name \*.pdf -print0| xargs -0 rm`

Install: 
Python 2.7.12  and Anaconda 4.1.1
`pip install --upgrade html5lib==1.0b8`

Run: 
`python tu.py`
`python tu_find.py "rent roll"`
