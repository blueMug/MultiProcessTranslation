from translate import Translate
import utils.file_util as futil
import time
import multiprocessing
import argparse
import os


parser = argparse.ArgumentParser(description="Multi-process translation using Google",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--srclg', type=str, default='en',
                    help='src language')
parser.add_argument('--trglg', type=str, default='zh-cn',
                    help='target language')
parser.add_argument('--input', type=str, required=True,
                    help='input file, each sentence a line')
parser.add_argument('--output', type=str, default='./output',
                    help='output file, each sentence a line')
parser.add_argument('--pbatch', type=int, default=100,
                    help='batch size for translation loop')
parser.add_argument('--process_num', type=int, default=5,
                    help='num of process')
parser.add_argument('--tbatch', type=int, default=5,
                    help='batch for one google translate request')
parser.add_argument('--max_try', type=int, default=3,
                    help='maximum try for google translate')


class MultiProcessTranslation:
    def __init__(self, client_url, src='en', target='zh-cn'):
        self.translator = Translate(client_url, src, target)

    def _translate(self, sentences, index, tbatch, max_try):
        output_list = []
        all_len = len(sentences)
        for i in range(0, all_len, tbatch):
            output_list.extend(self.translator.translate_batch(sentences[i: i + tbatch], max_try))
        return output_list, index

    def trans_all_processes(self, sentences, process_num, tbatch, max_try) -> list:
        """
        :param sentences:
        :param process_num:
        :param tbatch:  google 翻译，一次提交的数量
        :param max_try:  最大尝试次数
        :return:
        """
        processes = []
        pool = multiprocessing.Pool(process_num)
        step = int(len(sentences) / process_num)
        if step == 0:  # 总的翻译句子数小于进程数，则一个进程处理全部翻译
            step = len(sentences)
        for i in range(0, len(sentences), step):
            processes.append(pool.apply_async(func=self._translate, args=(sentences[i:i + step], i, tbatch, max_try)))
        pool.close()
        pool.join()
        result = []
        for p in processes:
            output_list, index = p.get()
            result.append([output_list.copy(), index])
        result.sort(key=lambda x: x[1])
        output_list = []
        for r in result:
            output_list.extend(r[0])

        return output_list

    def trans_all(self, sentences,
                  output_file,
                  index_file,
                  begin=0,
                  pbatch=100,
                  process_num=5,
                  tbatch=5,
                  max_try=3):
        """
        :param sentences:
        :param output_file: 如果不为空，则将翻译的内容写入该文件，以append方式
        :param index_file: 用来存储翻译的位置，只有output_file不为空才有意义
        :param begin: 待翻译文件中需要翻译的起始序列
        :param pbatch:  提交给所有进程总的数据量， 如果pbatch不为空，则每隔pbatch写入一次文件
        :param process_num:  进程数
        :param tbatch:  google 翻译，一次提交的数量
        :param max_try:  最大尝试次数
        :return:
        """
        translations = []
        all_len = len(sentences)
        for i in range(0, all_len, pbatch):
            translate_start = time.time()
            batch_translations = self.trans_all_processes(sentences[i: i + pbatch], process_num=process_num,
                                                          tbatch=tbatch, max_try=max_try)
            translate_end = time.time()
            print('翻译用时 %d, %d -> %s' % ((translate_end-translate_start), begin + i, batch_translations[:1]))
            if output_file:
                futil.add_to_txt(output_file, batch_translations)
                futil.save_to_txt(index_file, str(begin+len(batch_translations)))
            else:
                translations.extend(batch_translations)
        return translations


if __name__ == '__main__':
    args = parser.parse_args()
    url_client_file = 'client.config'
    client_url = []
    if os.path.exists(url_client_file):
        client_url = futil.read_txt(url_client_file)
    if len(client_url) == 0:
        client_url = ['translate.google.cn']
    mpt = MultiProcessTranslation(client_url, src=args.srclg, target=args.trglg)
    index_file = args.input+'.index'
    if os.path.exists(index_file):
        index = int(futil.read_txt(index_file)[0])
    else:
        index = 0
    sentences = futil.read_txt(args.input, begin=index)
    mpt.trans_all(sentences, output_file=args.output, index_file=index_file, begin=index,
                  pbatch=args.pbatch, process_num=args.process_num, tbatch=args.tbatch, max_try=args.max_try)
