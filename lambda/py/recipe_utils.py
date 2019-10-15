import logging
import recipes
import random

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

RECIPE_IMAGES = {
    'HON': "https://s3.amazonaws.com/ask-samples-resources/images/sauce-boss/honey mustard-sauce-500x500.png",
    'BBQ': "https://s3.amazonaws.com/ask-samples-resources/images/sauce-boss/barbecue-sauce-500x500.png",
    'THO': "https://s3.amazonaws.com/ask-samples-resources/images/sauce-boss/thousand island-sauce-500x500.png",
    'PES': "https://s3.amazonaws.com/ask-samples-resources/images/sauce-boss/pesto-sauce-500x500.png",
    'TAR': "https://s3.amazonaws.com/ask-samples-resources/images/sauce-boss/tartar-sauce-500x500.png",
    'PIZ': "https://s3.amazonaws.com/ask-samples-resources/images/sauce-boss/pizza-sauce-500x500.png",
    'CRA': "https://s3.amazonaws.com/ask-samples-resources/images/sauce-boss/cranberry-sauce-500x500.png",
    'SEC': "https://s3.amazonaws.com/ask-samples-resources/images/sauce-boss/secret-sauce-500x500.png"
}

RECIPE_DEFAULT_IMAGE = "https://s3.amazonaws.com/ask-samples-resources/images/sauce-boss/secret-sauce-500x500.png"


def getsauce_item(request):
    """
    Returns an object containing the recipe (sauce) ID & spoken value by the User from the JSON request
    Values are computing from slot "Item" or from Alexa.Presentation.APL.UserEvent arguments
    """
    sauce_item = {'id': None, 'spoken': None}
    logger.info("getsauce_item passed request: {}".format(request))
    if(request.object_type == 'Alexa.Presentation.APL.UserEvent'):
        sauce_item['id'] = request.arguments[1]
    else:
        itemSlot = request.intent.slots["Item"]
        # Capture spoken value by the user
        if(itemSlot and itemSlot.value):
            sauce_item['spoken'] = itemSlot.value

        if(itemSlot and
                itemSlot.resolutions and
                itemSlot.resolutions.resolutions_per_authority[0] and
                itemSlot.resolutions.resolutions_per_authority[0].status and
                str(itemSlot.resolutions.resolutions_per_authority[0].status.code) == 'StatusCode.ER_SUCCESS_MATCH'):
            sauce_item['id'] = itemSlot.resolutions.resolutions_per_authority[0].values[0].value.id

    return sauce_item


def getSauceImage(id):
    url = RECIPE_IMAGES[id]
    if(url):
        return url
    else:
        return RECIPE_DEFAULT_IMAGE


def get_locale_specific_recipes(locale):
    logger.info("loading locale for {}".format(locale[:2]))
    return recipes.translations[locale[:2]]


def getRandomRecipe(handler_input):
    locale = handler_input.request_envelope.request.locale
    logger.info("random recipe pool: {}".format(
        get_locale_specific_recipes(locale)))
    randRecipe = random.choice(
        list(get_locale_specific_recipes(locale).items()))
    logger.info("random recipe is: {}".format(randRecipe))
    return randRecipe[1]
