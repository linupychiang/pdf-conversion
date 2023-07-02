from PyPDF2 import PdfReader, PdfWriter
import os.path
import os


def pdf_add_page(path_source, page_insert, path_insert):
    page_insert -= 1

    pdf_source = PdfReader(open(path_source, 'rb'))  # 原PDF文件
    count_source = len(pdf_source.pages)  # 原文件页数
    pdf_insert = PdfReader(open(path_insert, 'rb'))  # 原PDF文件
    count_insert = len(pdf_insert.pages)  # 原文件页数

    if page_insert >= count_source:
        page_insert = count_source - 1
        print(f'最大插入页码为:{count_source}')

    pdf_writer = PdfWriter()
    path_dest = 'new/add/' + path_source.rpartition('/')[2]

    for page in range(count_source):
        if page != page_insert:
            pdf_writer.add_page(pdf_source.pages[page])  # 原文件页
        else:
            pdf_writer.add_page(pdf_source.pages[page])  # 原文件页
            for p in range(count_insert):
                pdf_writer.add_page(pdf_insert.pages[p])  # 插入文件页

    # pdf_insert 追加末尾
    for p in range(count_insert):
        pdf_writer.add_page(pdf_insert.pages[p])

    with open(path_dest, 'wb') as out:
        pdf_writer.write(out)
        print('add_page成功生成:{}'.format(path_dest))


def pdf_replace_page(path_source, page_replace, path_insert):
    page_replace -= 1

    pdf_source = PdfReader(open(path_source, 'rb'))  # 原PDF文件
    count_source = len(pdf_source.pages)  # 原文件页数
    pdf_insert = PdfReader(open(path_insert, 'rb'))  # 原PDF文件
    count_insert = len(pdf_insert.pages)  # 原文件页数

    if page_replace > count_source:
        print(f'超出原文件最大页码：{count_source}')
        return

    pdf_writer = PdfWriter()
    path_dest = 'new/replace/' + path_source.rpartition('/')[2]

    for page in range(count_source):
        if page != page_replace:
            pdf_writer.add_page(pdf_source.pages[page])  # 原文件页
        else:
            for p in range(count_insert):
                pdf_writer.add_page(pdf_insert.pages[p])  # 插入文件页

    # pdf_insert 追加末尾
    for p in range(count_insert):
        pdf_writer.add_page(pdf_insert.pages[p])

    with open(path_dest, 'wb') as out:
        pdf_writer.write(out)
        print('add_page成功生成:{}'.format(path_dest))


def pdf_delete_page(path_source, page_delete, path_insert):
    page_delete -= 1

    pdf_source = PdfReader(open(path_source, 'rb'))  # 原PDF文件
    count_source = len(pdf_source.pages)  # 原文件页数

    if page_delete > count_source:
        print(f'超出原文件最大页码：{count_source}')
        return

    pdf_writer = PdfWriter()
    path_dest = 'new/delete/' + path_source.rpartition('/')[2]

    for page in range(count_source):
        if page != page_delete:
            pdf_writer.add_page(pdf_source.pages[page])  # 原文件页

    with open(path_dest, 'wb') as out:
        pdf_writer.write(out)
        print('delete_page成功生成:{}'.format(path_dest))


def main():
    print('本程序分为3个功能：增加（1）、替换（2）、删除（3）。参数之间以一个空格间隔。')
    print('举例：')
    print('=' * 10)
    print('1 source 2 one.pdf')
    print('遍历source目录下所有pdf文件，从第2页开始，将one.pdf中的内容插入到pdf中')
    print('=' * 10)
    print('2 source 2 one.pdf')
    print('遍历source目录下所有pdf文件，将pdf的第2页，替换为one.pdf的内容')
    print('=' * 10)
    print('3 source 2')
    print('遍历source目录下所有pdf文件，删除pdf中第2页的内容')
    print('=' * 10)
    print('')
    print('注：目录及文件名称中不能包含空格！')
    print('注：第一个参数分别对应增加，替换，删除功能。')
    print('注：增加、替换功能，同时会把one.pdf的内容追加到source下pdf文件内容末尾')
    print('')
    print('输入exit退出程序...')
    print('')

    while True:
        data = input('请输入参数：')
        if data == 'exit':
            return

        datas = data.split(' ')

        if not os.path.exists('new/add'):
            os.makedirs('new/add')
        if not os.path.exists('new/replace'):
            os.makedirs('new/replace')
        if not os.path.exists('new/delete'):
            os.makedirs('new/delete')

        action_type = int(data[0])
        path_source = datas[1]
        page_action = int(datas[2])
        try:
            path_insert = datas[3]
        except Exception as e:
            print(e)
            path_insert = ''

        try:
            pdf_files = os.listdir(path_source)
        except Exception as e:
            print(e)
            pdf_files = []
            print(f'{path_source}目录不正确')

        if action_type == 1:
            for pdf_file in pdf_files:
                pdf_add_page(path_source + '/' + pdf_file, page_action,
                             path_insert)
        elif action_type == 2:
            for pdf_file in pdf_files:
                pdf_replace_page(path_source + '/' + pdf_file, page_action,
                                 path_insert)
        elif action_type == 3:
            for pdf_file in pdf_files:
                pdf_delete_page(path_source + '/' + pdf_file, page_action,
                                path_insert)
        else:
            print('输入不正确，请重新输入!!!')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('参数错误, e:' + e)
