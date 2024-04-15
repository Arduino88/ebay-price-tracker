from google_img_source_search import ReverseImageSearcher


if __name__ == '__main__':
    image_url = 'https://media.discordapp.net/attachments/777240183477239818/1229509162992533626/IMG_5305.jpg?ex=662ff0a3&is=661d7ba3&hm=45cac4d2f8797050d22a7f9dce5e77f6e7c2dd4036150596da57e76f4b523251&=&format=webp&width=526&height=701'

    rev_img_searcher = ReverseImageSearcher()
    res = rev_img_searcher.search(image_url)

    for search_item in res:
        print(f'Title: {search_item.page_title}')
        print(f'Site: {search_item.page_url}')
        print(f'Img: {search_item.image_url}\n')