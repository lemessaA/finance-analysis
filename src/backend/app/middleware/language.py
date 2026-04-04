from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional
import json

# Language mappings
LANGUAGE_MAPPING = {
    'en': 'english',
    'am': 'amharic', 
    'om': 'oromo'
}

# Translation dictionary for common responses
TRANSLATIONS = {
    'en': {
        'error': 'Error',
        'success': 'Success',
        'not_found': 'Not Found',
        'invalid_request': 'Invalid Request',
        'server_error': 'Internal Server Error',
        'validation_error': 'Validation Error',
        'unauthorized': 'Unauthorized',
        'forbidden': 'Forbidden',
        'rate_limit_exceeded': 'Rate Limit Exceeded',
        'service_unavailable': 'Service Unavailable'
    },
    'am': {
        'error': 'ስህተት',
        'success': 'ድሎት',
        'not_found': 'አልተገኘም',
        'invalid_request': 'ዋናይ ጥያቄ',
        'server_error': 'የሰርቨር ስህተት',
        'validation_error': 'የማረጋገጥ ስህተት',
        'unauthorized': 'ያልተፈቀደ',
        'forbidden': 'የተከለከ',
        'rate_limit_exceeded': 'የጊዜ ወሰን ተሞላ',
        'service_unavailable': 'አገልግሎት ያለሽ'
    },
    'om': {
        'error': 'Dogoggora',
        'success': 'Milkaa\'a',
        'not_found': 'Hin argamne',
        'invalid_request': 'Gaaffii gaggeeffame',
        'server_error': 'Dogoggora sarvarraa',
        'validation_error': 'Dogoggora mirkaneessaa',
        'unauthorized': 'Mirkaneessi hin milkaamne',
        'forbidden': 'Dhiifama',
        'rate_limit_exceeded': 'Yeroo waan caale',
        'service_unavailable': 'Taayilee hin jiru'
    }
}

def get_language_from_request(request: Request) -> str:
    """Extract language from request headers or query parameters"""
    # Check Accept-Language header
    accept_language = request.headers.get("accept-language", "")
    if accept_language:
        # Extract primary language (e.g., "en-US" -> "en")
        primary_lang = accept_language.split(",")[0].split("-")[0].lower()
        if primary_lang in TRANSLATIONS:
            return primary_lang
    
    # Check query parameter
    lang = request.query_params.get("lang")
    if lang and lang in TRANSLATIONS:
        return lang
    
    # Check cookie
    lang_cookie = request.cookies.get("language")
    if lang_cookie and lang_cookie in TRANSLATIONS:
        return lang_cookie
    
    # Default to English
    return "en"

def translate_message(message_key: str, language: str) -> str:
    """Get translated message for given language"""
    return TRANSLATIONS.get(language, {}).get(message_key, message_key)

def create_localized_response(
    status_code: int,
    message_key: str,
    data: Optional[dict] = None,
    language: str = "en"
) -> JSONResponse:
    """Create a JSON response with localized messages"""
    message = translate_message(message_key, language)
    
    response_data = {
        "status": "error" if status_code >= 400 else "success",
        "message": message,
        "language": language,
        "data": data
    }
    
    return JSONResponse(
        content=response_data,
        status_code=status_code
    )

def get_localized_prompt(base_prompt: str, language: str, context: Optional[dict] = None) -> str:
    """Get localized version of AI prompts"""
    
    # Language-specific context for AI models
    language_context = {
        'en': {
            'market_context': 'Ethiopian market and business environment',
            'currency': 'Ethiopian Birr (ETB)',
            'region': 'Ethiopia'
        },
        'am': {
            'market_context': 'የኢትዮጵያ ገበች እና የንግድ አካባቢ',
            'currency': 'የኢትዮጵያ ብር (ETB)',
            'region': 'ኢትዮጵያ'
        },
        'om': {
            'market_context': 'Gabaasa biilaa Itoophiyaa fi qindaa\'ina biilaa',
            'currency': 'Birra Itoophiyaa (ETB)',
            'region': 'Itoophiyaa'
        }
    }
    
    if language in language_context:
        context_info = language_context[language]
        if context:
            context_info.update(context)
        
        # Add language-specific instructions to the prompt
        localized_prompt = f"""
        Language: {language.upper()}
        Market Context: {context_info['market_context']}
        Currency: {context_info['currency']}
        Region: {context_info['region']}
        
        Please respond in {language} and provide insights specific to the {context_info['region']} market context.
        
        Original prompt:
        {base_prompt}
        """
        return localized_prompt
    
    return base_prompt

class LanguageMiddleware(BaseHTTPMiddleware):
    """Middleware to handle language detection and response localization"""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Extract language
        language = get_language_from_request(request)

        # Store language in request state for use in endpoints
        request.state.language = language

        # Call the endpoint
        response = await call_next(request)

        # Add language to response headers
        response.headers["Content-Language"] = language

        return response
