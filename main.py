from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas


def main():
    excel_data_df = pandas.read_excel(
        'beverages.xlsx',
        sheet_name='Лист1',
        na_values=' ',
        keep_default_na=False,
    )
    wines = excel_data_df.to_dict(orient='records')
    age = datetime.now().year - 1920

    sorted_wines = defaultdict(list)
    for wine in wines:
        sorted_wines[wine['Категория']].append(wine)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        sorted_wines=sorted_wines,
        age=age
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()

