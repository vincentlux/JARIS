def add_quote(inp):
    try:
        return int(inp)
    except:
        return '"' + inp + '"'
