from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
import argparse


def main():
    path = 'beverages.xlsx'
    parser = argparse.ArgumentParser(description='Укажите, при необходимости, путь к excel-файлу с напитками')
    parser.add_argument('--path', help='Путь к файлу')
    args = parser.parse_args()
    if args.path != None: path = args.path

    excel_data_df = pandas.read_excel(
        path,
        sheet_name='Лист1',
        na_values=' ',
        keep_default_na=False,
    )
    wines = excel_data_df.to_dict(orient='records')
    age = datetime.now().year - 1920

    grouped_wines = defaultdict(list)
    for wine in wines:
        grouped_wines[wine['Категория']].append(wine)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        sorted_wines=grouped_wines,
        age=age
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()

