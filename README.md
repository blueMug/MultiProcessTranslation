
使用google翻译文本，python多进程处理（建议python3），需要安装 [py-googletrans](https://github.com/ssut/py-googletrans)

## 说明
由于 py-googletrans 提供的翻译在连续翻译一部分文本后会十分卡顿，出现翻译失败，但是重启后又能比较正常的进行翻译，这里不去
深究内部的原因，采用多进程的方式绕过这种限制，将所有的翻译任务交由多个进程去翻译，每个进程只翻译相对短的任务，翻译结束后
直接死去，通过一个for循环遍历所有的文本，不断产生进程。

## 应用
- 本程序适合大批量句子的翻译，提供了断点功能，可灵活设置进程数以及单个任务的句子数
- 在client.config中可以修改翻译请求的链接，若多个则每行一个url，如空则使用 "translate.google.cn"
- 翻译程序启动后默认在根目录下生成一个.index的文件，用来记录当前翻译的位置

## 样例
``python multi_process_translate.py --srclg en --trglg zh-cn --input test --output test.trans``


## 相关参数如下：
- srclg: src language, [en, zh-cn, ...]           源语言缩写
- trglg: target language, [en, zh-cn, ...]        目标语言缩写
- input: input file, each sentence a line         输入文件，一行一个句子
- output: input file, each sentence a line        输出文件，一行一个句子
- pbatch: batch size for translation loop         一次翻译任务提交的句对数
- process_num: num of process                     进程数
- tbatch: batch for one google translate request  一次google翻译提交的句对数
- max_try: maximum try for google translate       google翻译出错时最大的尝试次数

## Tips
- 在网络情况比较好的时候，可以适当加大单个进程翻译的句子量，通过 pbatch 和 process_num 组合控制
- 当翻译的量太大时，可以考虑按行拆分输入文件，在不同的服务器分别运行，需要控制好 .index 的内容

