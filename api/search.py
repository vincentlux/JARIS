import pysolr, requests, argparse
from utils import add_quote

def search(keyword, test=False):
    if test: # show mode
        solr = pysolr.Solr("http://104.248.61.45:8983/solr/jaris/")
    else:
        raise NotImplementedError
    query = 'content:' + add_quote(keyword)
    print(query)
    results = solr.search(q=query, rows=10000)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--keyword', type=str, default='thermal',
            help='keyword you want to search and test.')
    parser.add_argument('--test', action='store_true', help='If present, test mode and show results directly.')
    args = parser.parse_args()

    # pass args to search
    results = search(args.keyword, test=args.test)
    print(f"Saw {len(results)} result(s).")
    for result in results:
        try:
            print(f"id: {result['doc_id'][0]}.")
            print(f"content: {result['content'][0]}.")
        except Exception as e:
            print(e)
