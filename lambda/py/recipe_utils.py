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


def getSauceItem(request):
    """
    Returns an object containing the recipe (sauce) ID & spoken value by the User from the JSON request
    Values are computing from slot "Item" or from Alexa.Presentation.APL.UserEvent arguments
    """
    sauceItem = {}
    if(request.type == 'Alexa.Presentation.APL.UserEvent'):
        sauceItem.id = request.arguments[1]
    else:
        itemSlot = request.intent.slots["Item"]
        # Capture spoken value by the user
        if(itemSlot and itemSlot.value):
            sauceItem.spoken = itemSlot.value

        if(itemSlot and
                itemSlot.resolutions and
                itemSlot.resolutions.resolutionsPerAuthority[0] and
                itemSlot.resolutions.resolutionsPerAuthority[0].status and
                itemSlot.resolutions.resolutionsPerAuthority[0].status.code == 'ER_SUCCESS_MATH'):
            sauceItem.id = itemSlot.resolutions.resolutionsPerAuthority[0].values[0].value.id

    logger.info("sauceItem: {}".format(sauceItem))
    return sauceItem


def load_locale_specific_recipe(locale):
    logger.info("loading locale for {}".format(locale[:2]))
    return list(recipes)[locale[:2]]


def getRandomRecipe(handler_input):
    locale = handler_input.request_envelope.request.locale
    randRecipe = random.choice(load_locale_specific_recipe(locale))
    logger.info("random recipe is: {}" + randRecipe)
    return randRecipe
