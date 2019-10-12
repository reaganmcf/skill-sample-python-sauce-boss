# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill and using the
# Alexa Skills Kid SDK (v2)
# Please visit https://alexa.design/cookbook for additional examples on
# implementing slots, dialog management,
# session persistence, api calls, and more.

import logging

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler, AbstractResponseInterceptor, AbstractRequestInterceptor
)
from ask_sdk_core.utils import is_request_type, is_intent_name

sb = CustomSkillBuilder()

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)


class LaunchRequestIntentHandler(AbstractRequestHandler):
    """
    Handles LaunchRequest requests sent by Alexa
    Note: this type of request is sent when hte user invokes your skill without providing a specific intent
    """

    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Welcome to sauce boss!"

        handler_input.response_builder.speak(speak_output)
        return handler_input.response_builder.response


class RecipeIntentHandler(AbstractRequestHandler):
    """
    Handles RecipeIntent or APL Touch Event requests sent by Alexa
    """

    def can_handle(self, handler_input):
        return is_intent_name("RecipeIntent")(handler_input) or (is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and handler_input.request_envelope.request.arguments.length > 0 and handler_input.request_envelope.request.arguments[0] == 'sauceInstructions')

    def handle(self, handler_input):
        handler_input.response_builder.speak("should be handling recipe here")
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """
    Handles AMAZON.HelpIntent requests sent by Alexa
    """

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "should be handling help intent here"

        handler_input.response_builder.speak(
            speak_output
        ).ask(speak_output)
        return handler_input.response_builder.response


class RepeatIntentHandler(AbstractRequestHandler):
    """
    Handles AMAZON.RepeatIntent requests sent by Alexa
    """

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        logger.info(session_attr)
        # generate json response
        return handler_input.response_builder.speak("should be handling repeat intent here").response


class ExitIntentHandler(AbstractRequestHandler):
    """
    Handler for AMAZON.CancelIntent and AMAZON.StopIntent
    Note : this request is sent when the user makes a request that corresponds to AMAZON.CancelIntent & AMAZON.StopIntent intents defined in your intent schema.
    """

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.CancelIntent")(handler_input) \
            and is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "should be handling exit intent!"
        handler_input.response_builder.speak(speak_output)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """
    Handler for SessionEndedRequest
    """

    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # Any cleanup logic goes here
        logger.info("~~~~ Session ended: {}".format(
            str(handler_input.request_envelope)))
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """
    Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        speak_output = "should be handling error messages"
        handler_input.response_builder.speak(speak_output).ask(speak_output)
        return handler_input.response_builder.response


class CacheResponseForRepeatInterceptor(AbstractResponseInterceptor):
    """Cache the response sent to the user in session.
    The interceptor is used to cache the handler response that is
    being sent to the user. This can be used to repeat the response
    back to the user, in case a RepeatIntent is being used and the
    skill developer wants to repeat the same information back to
    the user.
    """

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["recent_response"] = response


class RequestLogger(AbstractRequestInterceptor):
    """Log the request envelope."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Request Envelope: {}".format(
            handler_input.request_envelope))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the response envelope."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info("Response: {}".format(response))


# register request / intent handlers
sb.add_request_handler(LaunchRequestIntentHandler())
sb.add_request_handler(RecipeIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# register response interceptors
sb.add_global_response_interceptor(CacheResponseForRepeatInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())


lambda_handler = sb.lambda_handler()
