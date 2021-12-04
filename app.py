from flask import Flask,render_template,request,jsonify
import numpy as np
import pickle

app = Flask(__name__)
model = pickle.load(open('veg_rule_mining.pkl','rb'))

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/getdet',methods=['POST'])
def getdet():
    import pandas as pd
    import warnings
    warnings.filterwarnings("ignore")
    from mlxtend.frequent_patterns import apriori
    from mlxtend.frequent_patterns import association_rules

    df = pd.read_excel(r"veg.xlsx")
    df['kname'] = df['kname'].str.strip()
    df_basket = pd.pivot_table(data=df, index='billno', columns='kname', values='qty', aggfunc='sum', fill_value=0)

    ### wether that product is bought or not is important so lets chane these value to binary
    def convert_into_binary(x):
        if x > 0:
            return 1
        else:
            return 0

    basket_sets = df_basket.applymap(convert_into_binary)

    frequent_itemsets = apriori(basket_sets, min_support=0.01, use_colnames=True)
    frequent_itemsets

    rules_mlxtend = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    rules_mlxtend

    rules_mlxtend.sort_values(by=['lift'], ascending=False).head(20)

    import pickle
    file = open('veg_rule_mining.pkl', 'wb')
    pickle.dump(rules_mlxtend, file)

    output=rules_mlxtend
    return render_template('index.html',tables=[rules_mlxtend.to_html(classes='data')], titles=rules_mlxtend.columns.values)


if __name__=="__main__":
    app.run(port=5001,debug=True)