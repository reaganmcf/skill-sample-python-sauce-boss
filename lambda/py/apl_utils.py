import ask_sdk_core as Alexa
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, ExecuteCommandsDirective, SpeakItemCommand, HighlightMode
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


def recipeScreen(handler_input, sauce_item, selected_recipe):
    speak_output = selected_recipe['instructions']
    reprompt_output = data.RECIPE_REPEAT_MESSAGE
    if(supports_apl(handler_input)):
        handler_input.response_builder.add_directive(
            RenderDocumentDirective(
                token="sauce-boss",
                document=APL_DOCS['recipe'],
                datasources=generateRecipeScreenDatasource(
                    handler_input, sauce_item, selected_recipe)
            )).add_directive(
                ExecuteCommandsDirective(
                    token="sauce-boss",
                    commands=[
                        SpeakItemCommand(
                            component_id="recipeText",
                            highlight_mode=HighlightMode.line)
                    ]
                )
        )

        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes['speak_output'] = speak_output
        session_attributes['reprompt_output'] = reprompt_output


def generateRecipeScreenDatasource(handler_input, sauce_item, selected_recipe):
    random_sauce = recipe_utils.getRandomRecipe(handler_input)
    logger.info("random recipe: {}")
    header_title = data.RECIPE_HEADER_TITLE.format(selected_recipe['name'])
    hint_text = data.HINT_TEMPLATE.format(random_sauce['name'])
    sauce_ssml = "<speak>{}</speak>".format(selected_recipe['instructions'])
    return {
        'sauceBossData': {
            'type': 'object',
            'properties': {
                'headerTitle': header_title,
                'hintText': hint_text,
                'sauceImg': sauce_item['image'],
                'sauceText': selected_recipe['instructions'],
                'sauceSsml': sauce_ssml
            },
            'transformers': [
                {
                    'inputPath': 'sauceSsml',
                    'transformer': 'ssmlToSpeech',
                    'outputName': 'sauceSpeech'
                },
                {
                    'inputPath': 'hintText',
                    'transformer': 'textToHint'
                }
            ]
        }
    }


def generateLaunchScreenDatasource(handler_input):
    # random_recipe = recipe_utils.getRandomRecipe(handler_input)
    header_title = data.HEADER_TITLE.format(data.SKILL_NAME)
    hint_text = data.HINT_TEMPLATE.format("random recipe name")
    # saucesIdsToDisplay = ["BBQ", "CRA", "HON", "PES", "PIZ", "TAR", "THO", "SEC"]
    return {
        'sauceBossData': {
            'type': 'object',
            'properties': {
                'headerTitle': header_title,
                'hintText': hint_text,
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
