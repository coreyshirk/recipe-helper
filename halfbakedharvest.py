import requests
from bs4 import BeautifulSoup

HALFBAKEDHARVEST_LINKINPROFILE_URL = 'https://linkinprofile.com/api/v1/photos/public/halfbakedharvest'

def scrape_halfbakedharvest_recipe_ingredients(url):
    halfbakedharvest_request = requests.get(url)

    if (halfbakedharvest_request.status_code != 200):
        print('Error with status {status} encountered while retrieving latest posts'.format(
            status=halfbakedharvest_request.status_code))
        return None, None

    recipe_page = BeautifulSoup(halfbakedharvest_request.content, 'html.parser')
    post_title = recipe_page.find('h1', attrs={'class': 'post-title'}).text
    ingredients = recipe_page.findAll('li', attrs={'itemprop': 'recipeIngredient'})
    ingredients_list = [i.text.replace('\n', ' ').strip() for i in ingredients]
    return post_title, ingredients_list

response = requests.get(HALFBAKEDHARVEST_LINKINPROFILE_URL).json()
recipe_response = {
    "recipes": [],
    "next_max_id": response['next_max_id'] # This is for paginating linkinprofile for next post set (need ? at end of value)
}
for post in response['photos']:
    halfbakedharvest_recipe_url = post['lip_photo']['url']
    post_title, ingredients_list = scrape_halfbakedharvest_recipe_ingredients(halfbakedharvest_recipe_url)
    post_meta_dict = {
        "post_title": post_title,
        "ingredients_list": ingredients_list,
        "halfbakedharvest_website_url": halfbakedharvest_recipe_url,
        "halfbakedharvest_instagram_url": post['instagram_photo']['images']['thumbnail']['url']
    }
    recipe_response["recipes"].append(post_meta_dict)
