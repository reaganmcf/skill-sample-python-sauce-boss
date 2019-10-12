import ask_sdk_core as Alexa
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective
)
from ask_sdk_core.utils import (get_supported_interfaces)
import json
import recipes
import recipe_utils
from alexa import data
import logging

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)


def _load_apl_document(file_path):
    """
    Load the apl json document at the path into a dict object
    """
    with open(file_path) as f:
        return json.load(f)


APL_DOCS = {
    'launch': _load_apl_document('./documents/launchRequest.json'),
    'recipe': _load_apl_document('./documents/recipeIntent.json'),
    'help': _load_apl_document('./documents/helpIntent.json')
}


def supports_apl(handler_input):
    """
    Checks whether APL is supported by the User's device
    """
    supported_interfaces = get_supported_interfaces(
        handler_input)
    logger.info("supported interfaces: {}".format(supported_interfaces))
    return supported_interfaces.alexa_presentation_apl != None


def launch_screen(handler_input):
    """
    Adds Launch Screen (APL Template) to Response
    """
    if(supports_apl(handler_input)):
        handler_input.response_builder.add_directive(
            RenderDocumentDirective(
                token="launchToken",
                document=APL_DOCS['launch'],
                datasources=generateLaunchScreenDatasource(handler_input)
            )
        )


def generateLaunchScreenDatasource(handler_input):
    # random_recipe = recipe_utils.getRandomRecipe(handler_input)
    headerTitle = data.HEADER_TITLE.format(data.SKILL_NAME)
    hintText = data.HINT_TEMPLATE.format("random recipe name")
    # saucesIdsToDisplay = ["BBQ", "CRA", "HON", "PES", "PIZ", "TAR", "THO", "SEC"]
    return {
        'sauceBossData': {
            'type': 'object',
            'properties': {
                'headerTitle': headerTitle,
                'hintText': hintText,
                'items': []
            },
            'transformers': [
                {
                    'inputPath': 'hintText',
                    'transformer': 'textToHint'
                }
            ]
        }
    }
