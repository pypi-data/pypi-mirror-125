from askdata.NLG import nlg
import pandas as pd

if __name__ == "__main__":
    df = pd.DataFrame()
    df = df.append({'player': 'Cristiano Ronaldo', 'goals': 10, 'team': 'Juventus'}, ignore_index=True)
    df = df.append({'player': 'Roberto Baggio', 'goals': 2, 'team': 'Milan'}, ignore_index=True)
    examples=["{{player}}[[Cristiano Ronaldo]] scored {{goals}}[[3]] goals for {{team}}[[Juventus]]"]
    example_sentences=["Crisriano Ronaldo scored 3 goals for Juventus"]
    res = nlg(df=df, examples=examples, example_sentences=example_sentences, max_tokens=64)
    print(res)
