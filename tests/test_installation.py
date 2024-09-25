

def test():
    try:
        import inplace_abn
        assert bool(inplace_abn)
    except:
        assert False
    
    try:
        from inplace_abn import ABN
        assert bool(ABN)
    except:
        assert False
