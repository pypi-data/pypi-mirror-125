#### Installing

-----

Install with **pip**

```shell
pip install nest-dfa==1.1.2
```


#### Usage

------

- DFAFilter用法

  > :explain: 敏感词过滤
  >
  > :syntax: DFAFilter(sensitive_words: str) -> None
  >
  > :syntax: filter(self, message: str, repl: str="*") -> str
  >
  > :param: sensitive_words， 敏感词文本文件地址
  >
  > :param: message  需要检测敏感词的字符串
  >
  > :param: repl  敏感词需要替换的标识，默认为 *
  >
  > :return: 过滤后的字符串
  
  ```python
  >>> from pydfa.dfa import DFAFilter
  >>> dfa = DFAFilter(sensitive_words="/mnt/d/sensitive_words.txt")
  >>> message = "大家足球投注哈麻醉"
  >>> print(dfa.filter(message))
  >>> "大家****哈**"
  ```

