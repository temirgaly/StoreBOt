from email.mime import image
import requests
from Database import Database
from dotenv import load_dotenv, find_dotenv
import os
import directories

load_dotenv(find_dotenv())


class BaseClass:
    def __init__(self):
        self.db = Database.GetInstance()
        self.trendyol_url = os.environ.get('TRENDYOL_API')
        self.trendy_image_prefix = os.environ.get('IMAGE_PREFIX')

    def InsertProductByURL(self, URL):
        storeProductId = self.GetProductId(URL)

        # check if product already exists in db
        productExists = self.db.CheckProductByStoreId(storeProductId)

        if productExists:
            product = self.db.GetProductByStoreId(storeProductId)
            images = self.db.GetImagesByProductIdx(product['idx'])
            img = [r['url'] for r in images]

            return product['idx'], storeProductId, img
        else:
            product = []
            img = []
            response = self.GetProductDataByID(storeProductId)

            if response:
                if 'brand' in response:
                    if 'name' in response['brand']:
                        responseBrandName = response['brand']['name']
                        brandId = self.GetBrandIdByTitle(responseBrandName)

                        product.append(('bid', brandId))
                    else:
                        # not implemented. If brand not found should do something
                        # logg and deicde write or not
                        pass

                if 'category' in response:
                    if 'name' in response['category']:
                        responseCategoryName = response['category']['name']
                        categoryId = self.GetCategoryIdByTitle(
                            responseCategoryName)

                        product.append(('cid', categoryId))
                    else:
                        # not implemented. If category not found should do something
                        # logg and deicde write or not
                        pass

                if 'contentDescriptions' in response:
                    descriptions = []
                    for d in response['contentDescriptions']:
                        descriptions.append(d['description'])

                    product.append(('description', descriptions))

                if 'name' in response:
                    name = response['name']
                    product.append(('title', name))

                if 'id' in response:
                    storeId = response['id']
                    product.append(('storeId', storeId))

                product.append(('url', URL))

                productId = self.db.InsertValuesToTable('product', product)

                # insert values directly to images table with pid(product id)
                if 'images' in response:
                    for link in response['images']:
                        imageLink = self.trendy_image_prefix.format(link)
                        print(link, imageLink)

                        img.append(imageLink)
                        self.db.InsertValuesToTable(
                            'images', [('pid', productId), ('url', imageLink)])

                if 'variants' in response:
                    for variant in response['variants']:
                        v = [('pid', productId)]
                        v.append(('currency', 'TL'))
                        if 'attributeName' in variant:
                            v.append(
                                ('attributeName', variant['attributeName']))

                        if 'attributeType' in variant:
                            v.append(
                                ('attributeType', variant['attributeType']))

                        if 'attributeValue' in variant:
                            v.append(
                                ('attributeValue', variant['attributeValue']))

                        if 'price' in variant:
                            if 'discountedPrice' in variant['price']:
                                v.append(
                                    ('discountedPrice', variant['price']['discountedPrice']['value']))

                            if 'sellingPrice' in variant['price']:
                                v.append(
                                    ('sellingPrice', variant['price']['sellingPrice']['value']))

                            if 'originalPrice' in variant['price']:
                                v.append(
                                    ('originalPrice', variant['price']['originalPrice']['value']))

                            self.db.InsertValuesToTable('variants', v)

                        # directories.GetProducts()
                        return productId, storeProductId, img

    def GetProductDataByID(self, productId):
        response = requests.get(self.trendyol_url.format(productId))
        if response.status_code == 200:
            return response.json()['result']
        else:
            return None

    def GetProductId(self, URL):
        productId = None
        arr = URL.split('/')
        # short URL
        if arr[2] == 'ty.gl' or len(arr[2].split('.')) < 3:
            r = requests.get(URL, allow_redirects=False)
            for items in r.headers['location'].split('&'):
                if 'ContentId' in items:
                    productId = items.split('=')[1]
                    break
        else:
            if len(arr) >= 4:
                for elem in arr[4].split('-')[::-1]:
                    if elem == 'p':
                        break
                    productId = elem

            if productId:
                index = productId.find('?')
                if index > -1:
                    return productId[0:index]

        return productId

    def GetBrandIdByTitle(self, title):
        for row in directories.brands:
            if row['title'] == title:
                return row['idx']

        request = [('title', title), ('description', None), ('rate', None)]
        idx = self.db.InsertValuesToTable('brands', request)

        directories.GetBrands()
        return idx

    def GetCategoryIdByTitle(self, title):
        for row in directories.categories:
            if row['title'] == title:
                return row['idx']

        request = [('parid', 0), ('title', title), ('description', None)]
        idx = self.db.InsertValuesToTable('category', request)

        directories.GetCategories()
        return idx


if __name__ == '__main__':
    base = BaseClass()
    directories.init()
    response = base.InsertProductByURL('https://ty.gl/q83dnfdgqj')
    print(response)
