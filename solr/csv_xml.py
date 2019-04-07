import argparse, os, re

# Tags
tag_start           = '<add>\n<doc>\n'
tag_id              = '<field name="doc_id">'
tag_content         = '<field name="content">'
tag_close           = '</field>\n'
tag_end             = '</doc>\n</add>'

def docs_to_xml(lines, dir_out):
    '''convert a list to len(lines) numbe of .xml documents
    in: 
        lines: list, with each instance a document
    out:
        save each instance to a separate .xml file
    '''
    if not os.path.exists(dir_out):
        os.makedirs(dir_out)
    for i in range(len(lines)):
        str_id = tag_id + str(i) + tag_close
        content = tag_content + lines[i] + tag_close
        res = tag_start + str_id + content + tag_end
        save_to_xml(res, i, dir_out)


def save_to_xml(xml, str_id, dir_out):
    '''save xml-like str to a file to dirout/str_id.csv
    in: 
        xml: xml-like str
        str_id: id for .xml file name
        dir_out: place to save .xml
    out:
        save each instance to a separate .xml file
    '''
    path_out = os.path.join(dir_out, str(str_id)+'.xml')
    with open (path_out, 'w') as f:
        f.write(xml)
        print(f'finished processing {path_out}')
        


if __name__ == '__main__':
    # convert single csv file to xml file
    # 1. construct args
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_in', default='./', type=str, help='dir of where the csv is saved')
    parser.add_argument('--dir_out', default='./xml_dir', type=str, help='dir of where the csv is saved')
    parser.add_argument('--csv', default='test', type=str, help='name of the input csv file')
    args = parser.parse_args()

    # 2. read and convert
    in_file = os.path.join(args.dir_in, args.csv+'.csv')
    with open (in_file, 'r') as f:
        lines = f.readlines()
    docs_to_xml(lines, args.dir_out)
        

    


