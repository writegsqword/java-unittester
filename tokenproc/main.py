import cfg
import regex as re
import copy


def parse_func_name(src_line : str) -> str:
    rmatch = re.findall(r'// Test\(s\) for (.*)', src_line)[0]
    return rmatch



def extract_utest_lines(src_lines : list) -> dict:
    cur_fn = None
    res = {}
    cur_reslist = []
    for l in src_lines:
        if cur_fn != None:
            if cfg.DELIMIT_TOKEN in l or cfg.END_TEST_TOKEN in l:
                res[cur_fn] = cur_reslist
                if cfg.END_TEST_TOKEN in l:
                    return res
                cur_reslist = []
                cur_fn = parse_func_name(l)
                cur_reslist.append(l)
                
                continue
                
            cur_reslist.append(l)
        
        if cfg.DELIMIT_TOKEN in l:
            cur_fn = parse_func_name(l)
            cur_reslist.append(l)
    return res



def process_var_token(token : str) -> str:
    return token[:-1] + cfg.VARDECL_WILDCARD_TOKEN

def parse_utest(utest_lines : list) -> list:
    utest_parsed = []
    var_tokens = {}
    for l in utest_lines:
        if cfg.COMMENT_TOKEN in l:
            continue
        tokens = l.split(" ")
        tokens = list(filter(lambda x : x != "", tokens))

        
        #need to figure out smarter dets
        for i in range(len(tokens)):
            v = tokens[i]
            if(v != "="):
                continue
            vdecltok = tokens[i - 1]
            vdeftok = tokens[i + 1]
            var_tokens[vdecltok] = process_var_token(vdecltok)
            #skip function calls
            if("(" in vdeftok):
                continue
            var_tokens[vdeftok] = cfg.VARDEF_WILDCARD_TOKEN + ";\n"
    
    utest_parsed = copy.deepcopy(utest_lines)
    for k,v in var_tokens.items():
        for i, l in enumerate(utest_parsed):
            utest_parsed[i] = l.replace(k, v)

    #last pass, sub all prompt tokens
    for i, l in enumerate(utest_parsed):
        if cfg.COMMENT_TOKEN in l:
            continue
        utest_parsed[i] = l.replace("1", cfg.VARDECL_WILDCARD_TOKEN)

    return utest_parsed

#args follow the order of unit test def
def gen_utest(utest_parsed : list, idx : int, args : list) -> str:
    args = copy.deepcopy(args)
    res = ""
    idxs = str(idx)
    for l in utest_parsed:
        if cfg.COMMENT_TOKEN in l:
            res += l
            continue
        lr = l
        lr = lr.replace(cfg.VARDECL_WILDCARD_TOKEN, idxs)
        if cfg.VARDEF_WILDCARD_TOKEN in lr and len(args) > 0:
            lr = lr.replace(cfg.VARDEF_WILDCARD_TOKEN, args.pop(0))
        res += lr
    return res

        

def main():
    src_lines = []
    with open("in/Selections.java", "r") as f:
        src_lines = f.readlines()
    utests = extract_utest_lines(src_lines)
    utests_parsed = {}
    for k, v  in utests.items():
        utests_parsed[k] = parse_utest(v)
    print(utests_parsed["calculateYearlyBonus"])
    tests = ["1200", "2", "true", "false", "1375.0"]
    print(gen_utest(utests_parsed["calculateYearlyBonus"], 1, tests))

    for i in range(1, 4):
        print(gen_utest(utests_parsed["calculateYearlyBonus"], i, tests))
        pass

        


main()