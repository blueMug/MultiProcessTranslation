
使用google翻译文本，python多进程处理，需要安装 [py-googletrans](https://github.com/ssut/py-googletrans)

由于 py-googletrans 提供的翻译在连续翻译一部分文本后会十分卡顿，出现翻译失败，但是重启后又能比较正常的进行翻译，这里不去
深究内部的原因，采用多进程的方式绕过这种限制，将所有的翻译任务交由多个进程去翻译，每个进程只翻译相对短的任务，翻译结束后
直接死去，通过一个for循环遍历所有的文本，不断产生进程。

相关参数如下：
- srclg: src language, [en, zh-cn, ...]           源语言缩写
- trglg: target language, [en, zh-cn, ...]        目标语言缩写
- input: input file, each sentence a line         输入文件，一行一个句子
- output: input file, each sentence a line        输出文件，一行一个句子
- pbatch: batch size for translation loop         一次翻译任务提交的句对数
- process_num: num of process                     进程数
- tbatch: batch for one google translate request  一次google翻译提交的句对数
- max_try: maximum try for google translate       google翻译出错时最大的尝试次数
