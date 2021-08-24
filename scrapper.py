from datetime import datetime
import lxml.html as html
import requests
import os

errors = 0
HOME_URL = 'https://www.larepublica.co/'

# la etiqueta h2 fue reemplazada por text-fill ya que python no la reconoce como h2
# solo la reconoce como 
XPATH_LINKS = '//text-fill/a[contains(@href, "https://www.larepublica.co")]/@href'
XPATH_TITLE = '//div[@class = "mb-auto"]/text-fill/span/text()'
XPATH_DATE = '//div/span[@class="date"]/text()'
XPATH_SUMMARY = '//div[@class = "lead"]/p/text()'
XPATH_AUTHOR = '//div[@class = "autorArticle"]/p/text()'
XPATH_CONTENT_NEW = '//div[@class = "html-content"]/p[not(@class)]/text()'


def parse_new(link:str, route:str):
    global errors
    try:
        response = requests.get(link)

        if response.status_code == 200:
            new = response.content.decode('utf-8')
            parsed = html.fromstring(new)

            title_new = parsed.xpath(XPATH_TITLE)[0]
            title_new = title_new.replace('\"', '')
            author_new = parsed.xpath(XPATH_AUTHOR)[0]
            date_new = parsed.xpath(XPATH_DATE)[0]
            summary_new = parsed.xpath(XPATH_SUMMARY)[0]
            # No se toma el primer elemento debido a que es una lista de parrafos
            content_new = parsed.xpath(XPATH_CONTENT_NEW)

            with open(f'{route}/{title_new}.txt', 'w', encoding='utf-8') as file:
                file.write(title_new)
                file.write('\n')
                file.write(author_new)
                file.write(date_new)
                file.write('\n\n')
                file.write(summary_new)
                file.write('\n\n')
                for p in content_new:
                    file.write(p)
                    file.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)

    except IndexError:
        print('Ha ocurrido un error leyendo la noticia')
        errors += 1


def write_txt(route:str, text:str):
    try:
        with open(route, "w") as file:
            file.write(text)
    except:
        print('Ha ocurrido un error al escribir el archivo')


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            # content devuelve el html de la respuesta
            home = response.content.decode('utf-8')
            # write_txt("page.txt", home)
            # se transfroma a un documento especial para hacer xpath
            parsed = html.fromstring(home)
            links_to_news = parsed.xpath(XPATH_LINKS)

            today = datetime.today().strftime('%d-%m-%Y')
            if not os.path.isdir(f"news/{today}"):
                os.mkdir(f"news/{today}")
            
            for link in links_to_news:
                print(link)
                parse_new(link, f'news/{today}')

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)

    global errors
    print(f'No se han podido leer {errors} noticias')
    


def main():
    parse_home()


if __name__ == "__main__":
    main()
