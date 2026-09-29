import requests,time,csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
url='https://scrapifydatalabs.com/playground/ecommerce/'
list1=[]
while True:
    try:
             r=requests.get(url,timeout=10)
             r.raise_for_status()
    except requests.exceptions.RequestException as e:
             print('Request Failed!',e)
             break
    soup=BeautifulSoup(r.text,'html.parser')
    products=soup.find_all('div',class_='sf-result')
    for product in products:
        
        name=product.find('h2',class_='sf-result-title')
        if name:
             name=name.text.strip()
        else:
             name=''
        price=product.find('div',class_='sf-price')
        if price:
             price=price.text.strip()
        else:
             price=''
        rating=product.find('div',class_='sf-stars')
        if rating:
              rating=rating.find(string=True, recursive=False).strip()
        else:
             rating=''
        fastShip_status=product.find('span',class_='sf-badge-fast')
        if fastShip_status:
             fastShip_status=fastShip_status.text.strip()
        else:
             fastShip_status=''
        link=product.find('h2', class_='sf-result-title')

        if link:
          product_link=link.find('a', href=True)
        else:
          product_link=None

        if product_link:
          product_URL=urljoin(url, product_link.get('href'))
        else:
           product_URL=''
        review_count=product.find('a',class_='reviews')
        if review_count:
             review_count=review_count.text.strip()
        else:
             review_count=''
        dictionary={
            'name':name,
            'price':price,
            'rating':rating,
            'fastShip_status':fastShip_status,
            'review_count':review_count,
            'product_URL':product_URL
        }
        list1.append(dictionary)
    next_url=soup.find('a',rel='next')
    if next_url:
         next_url=next_url.get('href')
         url=urljoin(url,next_url)
         time.sleep(2)
    else:
         break
with open('products.csv','w',newline='',encoding='utf-8') as file:
     writer=csv.DictWriter(file,fieldnames=['name','price','rating','fastShip_status','review_count','product_URL'])
     writer.writeheader()
     writer.writerows(list1)
detail_list=[]
with open('products.csv','r',encoding='utf-8') as file:
     reader=csv.DictReader(file)
     for row in reader:
          product_URL=row['product_URL']
          attempts=0
          r=None
          while attempts<4:
           try:
               
               r=requests.get(product_URL,timeout=10)
               
               r.raise_for_status()
               break
           except requests.exceptions.RequestException as e:
               attempts+=1
               print('Request Failed!',e)
               if attempts<4:
                    time.sleep(2)
          if r is None:
               print('Skipping product after 4 attempts:', product_URL)
               continue    
              
          soup = BeautifulSoup(r.text, 'html.parser')
          sku_tag=soup.find('th',string='SKU')
          if sku_tag:
               sku=sku_tag.find_next('td')
          else:
               sku=''
          if sku:
               sku=sku.text.strip()
          else:
               sku=''
          brand_tag=soup.find('th',string='Brand Name')
          if brand_tag:
               brand_name=brand_tag.find_next('td')
          else:
               brand_name=''
          if brand_name:
               brand_name=brand_name.text.strip()
          else:
               brand_name=''
          color_tag=soup.find('div',id='variation_color_name')
          if color_tag:
             color=color_tag.find('div',class_='sf-variant-row')
          else:
               color=''
          if color:
               color=color.text.strip()
          else:
               color=''
          style_tag=soup.find('div',id='variation_size_name')
          if style_tag:
            style=style_tag.find('div',class_='sf-variant-row')
          else:
               style=''
          if style:
               style=style.text.strip()
          else:
               style=''
          bullets_tag=soup.find('div',id='feature-bullets')
          if bullets_tag:
            bullets=bullets_tag.find('ul',class_='sf-bullets')
          else:
               bullets=''
          if bullets:
               bullets=bullets.text.strip()
          else:
               bullets=''
          description=soup.find('div',class_='sf-a-plus')
          if description:
               description=description.text.strip()
          else:
               description=''
          availability=soup.find('div',id='availability')
          if availability:
               availability=availability.text.strip()
          else:
               availability=''
          rows=soup.find('table',class_='sf-specs')
          technical_specs=[]
          if rows:
            for row in rows.find_all('tr'):
             key=row.find('th')
             value=row.find('td')
             if key and value:
               column=f"{key.get_text(strip=True)}:{value.get_text(strip=True)}"
               technical_specs.append(column)
          else:
               technical_specs=[]
          technical_specs='|'.join(technical_specs)
          dictionary2={
               'product_URL':product_URL,
               'sku':sku,
               'brand_name':brand_name,
               'color':color,
               'style':style,
               'bullets':bullets,
               'availability':availability,
               'description':description,
               'technical_specs':technical_specs
          }
          detail_list.append(dictionary2)
           
with open('detail.csv','w',newline='',encoding='utf-8') as file:
     writer=csv.DictWriter(file,fieldnames=['product_URL','sku','brand_name','color','style','bullets','availability','description','technical_specs'])
     writer.writeheader()
     writer.writerows(detail_list)
detail_data = {}

with open('detail.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        detail_data[row['product_URL']] = row
final_list = []

with open('products.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        product_URL = row['product_URL']

        detail = detail_data.get(product_URL, {})

        combined = {**row, **detail}

        final_list.append(combined)
with open('final_products.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            'name',
            'price',
            'rating',
            'fastShip_status',
            'review_count',
            'product_URL',
            'sku',
            'brand_name',
            'color',
            'style',
            'bullets',
            'availability',
            'description',
            'technical_specs'
        ]
    )

    writer.writeheader()
    writer.writerows(final_list)

import csv

data = []

with open('final_products.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        data.append(row)


from openpyxl import Workbook

workbook = Workbook()
sheet = workbook.active
sheet.title = "Products"
headers = list(data[0].keys())

sheet.append(headers)
for row in data:
    sheet.append(list(row.values()))
workbook.save('final_products.xlsx')


          
          


          

             
     
      
          
     







