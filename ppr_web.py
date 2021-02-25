from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import pandas as pd
import numpy as np
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MH14BV1935//'
Bootstrap(app)


class InputForm(FlaskForm):
    address_ = StringField('Address', validators=[DataRequired()])
    date = DateField('Date', validators=[InputRequired()], format='%Y-%m-%d')

# df = pd.read_csv('tableTest.csv')


data = pd.read_csv('PPR-ALL.csv', engine='python')
data['Date of Sale (dd/mm/yyyy)'] = pd.to_datetime(data['Date of Sale (dd/mm/yyyy)'], dayfirst=True)

data_add = data.Address

# get the closest top 5 dates to the input date
def nearest_date_idx(r_list, g_date):
    diff_idx = np.abs(r_list - pd.to_datetime(g_date, dayfirst=True)).nsmallest(7).index
    return diff_idx

def main_process(input_address, data_add, data, date):
    layer_1 = process.extract(input_address, data_add, scorer=fuzz.token_set_ratio, limit=20)
    layer_2 = [y for y in layer_1 if y[1] > 60]
    #     layer_2
    layer_3_idx = [z[2] for z in layer_2]
    #     layer_3
    results = nearest_date_idx(data.loc[layer_3_idx]['Date of Sale (dd/mm/yyyy)'], date)
    if len(results) <= 0:
        print('No Results')
    else:
        return data.loc[results]


# def main_process_nodate(input_address, data_add, data):
#     layer_1 = process.extract(input_address, data_add, scorer=fuzz.token_set_ratio, limit=20)
#     layer_2 = [y for y in layer_1 if y[1] > 60]
#     #     layer_2
#     layer_3_idx = [z[2] for z in layer_2]
#     #     layer_3
#     results = nearest_date_idx(data.loc[layer_3_idx]['Date of Sale (dd/mm/yyyy)'], date)
#     if len(results) <= 0:
#         print('No Results')
#     else:
#         return data.loc[results]


@app.route('/', methods=['GET','POST'])
def home():
    form = InputForm()
    # if request.method == 'POST':
    #     results = request.form
    #     address = results.get('address')
    #     date = results.get('date')

    if form.validate_on_submit():
        # if address == " " or date == " ":
        address = form.address_.data
        date = form.date.data
        df = main_process(address, data_add, data, date)
        print(address, date)

        return render_template('results.html', df=df, address=address, date=date, form=form)

    return render_template('test.html', form=form)



if __name__=='__main__':
    app.run(debug='True')