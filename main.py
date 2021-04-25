from flask import *
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired
from finder import search1, search2, search3
import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
adr = ''  # создаю глобальные переменные адреса и параметра поиска
srch = ''


class Start(FlaskForm):
    search = SelectField("Выбирите параметр поиска", validators=None, choices=[(1, 'Найти приют рядом с вашим домом (введите свой адрес)'),
                                                                            (2, "Найти приют по адресу (введите требуемый адрес)"),
                                                                            (3, "Найти приют по названию (введите название приюта)")])
    # выбор параметра поиска
    address = StringField('Введите адрес или название приюта:', validators=[InputRequired('адрес')]) # поле для ввода адреса или названия приюта
    submit = SubmitField('Искать')


@app.route('/', methods=['GET', 'POST'])
def start():  # стартовое окно
    global adr, srch
    form = Start()
    if form.validate_on_submit():  # если поля заполнены, запоминаем адрес и параметр в глобальные переменные
        adr = form.address.data
        srch = form.search.data
        return redirect('/results')  # переход к результатам
    return render_template('start.html', title='Поиск приюта для животных', form=form)


@app.route('/results', methods=['GET', 'POST'])
def results():  # результаты поиска
    print(adr, srch)
    a = {}
    if srch == '1':  # если выбран первый параметр поиска
        result = search1(adr)  # получаешь json словарь с информацией о приютах
        print(result['features'][0])
        for i in range(len(result['features'])):
            # находим адрес
            a[result['features'][i]['properties']['name']] = [i + 1, result['features'][i]['properties']['description']]
            if 'url' in result['features'][i]['properties']['CompanyMetaData'].keys():
                # если есть сайт добавляем в словарь
                a[result['features'][i]['properties']['name']].append(
                        result['features'][i]['properties']['CompanyMetaData']['url'])
            else:
                # если нет сайта добавляем 0
                a[result['features'][i]['properties']['name']].append(0)
            if 'Phones' in result['features'][i]['properties']['CompanyMetaData'].keys():
                b = []
                # если есть телефоны, добавляем
                for j in range(len(result['features'][i]['properties']['CompanyMetaData']['Phones'])):
                    b.append(result['features'][i]['properties']['CompanyMetaData']['Phones'][j]['formatted'])
                a[result['features'][i]['properties']['name']].append(b)
            else:
                # если нет телефонов добавляем 0
                a[result['features'][i]['properties']['name']].append(0)
    elif srch == '2':  # аналогично 1ому
        result, S = search2(adr)
        S = round(S, 1)
        for i in range(1):
            a[result['features'][i]['properties']['name']] = [i + 1, result['features'][i]['properties']['description']]
            if 'url' in result['features'][i]['properties']['CompanyMetaData'].keys():
                a[result['features'][i]['properties']['name']].append(
                        result['features'][i]['properties']['CompanyMetaData']['url'])
            else:
                a[result['features'][i]['properties']['name']].append(0)
            if 'Phones' in result['features'][i]['properties']['CompanyMetaData'].keys():
                b = []
                for j in range(len(result['features'][i]['properties']['CompanyMetaData']['Phones'])):
                    b.append(result['features'][i]['properties']['CompanyMetaData']['Phones'][j]['formatted'])
                a[result['features'][i]['properties']['name']].append(b)
            else:
                a[result['features'][i]['properties']['name']].append(0)
        a[result['features'][0]['properties']['name']].append(S)
    elif srch == '3':
        result = search3(adr)
        for i in range(1):
            a[result['features'][i]['properties']['name']] = [i + 1, result['features'][i]['properties']['description']]
            if 'url' in result['features'][i]['properties']['CompanyMetaData'].keys():
                a[result['features'][i]['properties']['name']].append(
                        result['features'][i]['properties']['CompanyMetaData']['url'])
            else:
                a[result['features'][i]['properties']['name']].append(0)
            if 'Phones' in result['features'][i]['properties']['CompanyMetaData'].keys():
                b = []
                for j in range(len(result['features'][i]['properties']['CompanyMetaData']['Phones'])):
                    b.append(result['features'][i]['properties']['CompanyMetaData']['Phones'][j]['formatted'])
                a[result['features'][i]['properties']['name']].append(b)
            else:
                a[result['features'][i]['properties']['name']].append(0)
        print(a)
    return render_template('search.html', x=srch, spisok=a)


@app.route('/review', methods=['GET', 'POST'])
def review():  # оставить отзыв
    return render_template('review.html')


@app.route('/thanks')
def thanks():  # благодарность за отзыв
    return render_template('Thanks.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

# Пример адреса: Москва, ул. Ак. Королева, 12
# Пример названия приюта: Муниципальный приют «Бирюлево»
