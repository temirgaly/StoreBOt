import requests


def main():
    urls = [
        'https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll/sr?wb=44,104189,128&wg=3&wc=119&pi={}'
    ]

    response = requests.get(urls[0].format(2))
    if response.status_code == 200:
        response.json()['result']


def urlFormatter(url: str):
    endIndex = url.find('pi=')
    result = url[:endIndex]
    print(result)


if __name__ == '__main__':
    url = 'https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll/sr/new-balance-kadin-t-shirt-x-b128-g1-c73?pi=2&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA'
    response = urlFormatter(url)
