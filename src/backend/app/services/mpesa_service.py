"""
M-Pesa Payment Integration Module

This module handles M-Pesa payments using Safaricom's Daraja API.
Supports STK Push, B2C, B2B, C2B, and Transaction Status queries.
Enhanced with comprehensive error handling, logging, validation, and retry logic.
"""

from __future__ import annotations

import base64
import datetime
import json
import hashlib
import uuid
from typing import Dict, Any, Optional
from dataclasses import dataclass

import httpx
from app.config import settings
from app.exceptions.mpesa_exceptions import (
    MpesaException, MpesaAuthenticationError, MpesaValidationError,
    MpesaAPIError, MpesaTransactionError, MpesaConfigurationError,
    MpesaRetryableError, MpesaErrorCode
)
from app.validators.mpesa_validator import MpesaInputValidator
from app.logging.mpesa_logger import get_mpesa_logger
from app.retry.mpesa_retry import (
    execute_mpesa_with_retry, RetryConfig, RetryStrategy
)

# Initialize M-Pesa logger
logger = get_mpesa_logger()


@dataclass
class MpesaConfig:
    """M-Pesa configuration settings."""
    consumer_key: str
    consumer_secret: str
    passkey: str
    shortcode: str
    initiator_name: str
    callback_url: str
    confirmation_url: str
    validation_url: str
    environment: str = "sandbox"  # sandbox or production


@dataclass
class STKPushRequest:
    """STK Push payment request."""
    phone_number: str
    amount: int
    account_reference: str
    transaction_desc: str
    callback_url: Optional[str] = None


@dataclass
class PaymentResponse:
    """Payment response structure."""
    success: bool
    message: str
    checkout_request_id: Optional[str] = None
    merchant_request_id: Optional[str] = None
    response_code: Optional[str] = None
    response_description: Optional[str] = None
    customer_message: Optional[str] = None


class MpesaService:
    """M-Pesa payment service implementation with enhanced error handling and retry logic."""
    
    def __init__(self, config: MpesaConfig):
        self.config = config
        self.access_token = None
        self.token_expiry = None
        self.base_url = (
            "https://sandbox.safaricom.et" if config.environment == "sandbox"
            else "https://api.safaricom.et"
        )
        
        # Validate configuration
        self._validate_config()
        
        # Setup retry configuration
        self.retry_config = RetryConfig(
            max_retries=3,
            base_delay=1.0,
            max_delay=30.0,
            strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
            jitter=True
        )
        
        logger.info("M-Pesa service initialized", environment=config.environment, base_url=self.base_url)
    
    def _validate_config(self):
        """Validate M-Pesa configuration."""
        missing_fields = []
        
        if not self.config.consumer_key:
            missing_fields.append("consumer_key")
        if not self.config.consumer_secret:
            missing_fields.append("consumer_secret")
        if not self.config.passkey:
            missing_fields.append("passkey")
        if not self.config.shortcode:
            missing_fields.append("shortcode")
        if not self.config.initiator_name:
            missing_fields.append("initiator_name")
        if not self.config.callback_url:
            missing_fields.append("callback_url")
        
        if missing_fields:
            error_msg = f"Missing required M-Pesa configuration: {', '.join(missing_fields)}"
            logger.error(error_msg, missing_fields=missing_fields)
            raise MpesaConfigurationError(error_msg, missing_fields)
    
    async def get_access_token(self) -> str:
        """Get OAuth access token from M-Pesa with retry logic."""
        if self.access_token and self.token_expiry and datetime.datetime.now() < self.token_expiry:
            logger.debug("Using cached access token")
            return self.access_token
        
        async def _fetch_token():
            """Internal method to fetch token with API call."""
            # Create authentication string
            auth_string = f"{self.config.consumer_key}:{self.config.consumer_secret}"
            auth_bytes = auth_string.encode('ascii')
            auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
            
            headers = {
                "Authorization": f"Basic {auth_b64}",
                "Content-Type": "application/json"
            }
            
            data = {"grant_type": "client_credentials"}
            
            start_time = datetime.datetime.now()
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials",
                    headers=headers,
                    json=data,
                    timeout=30.0
                )
                
                response_time = (datetime.datetime.now() - start_time).total_seconds() * 1000
                
                # Log API call
                logger.log_api_call(
                    method="POST",
                    url=f"{self.base_url}/oauth/v1/generate",
                    status_code=response.status_code,
                    response_time_ms=response_time,
                    success=response.status_code == 200
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    self.access_token = token_data.get("access_token")
                    # Token expires in 1 hour
                    self.token_expiry = datetime.datetime.now() + datetime.timedelta(hours=1)
                    
                    logger.log_authentication(
                        action="token_request",
                        success=True,
                        details={
                            "token_expires_at": self.token_expiry.isoformat(),
                            "response_time_ms": response_time
                        }
                    )
                    
                    return self.access_token
                else:
                    error_data = {}
                    try:
                        error_data = response.json()
                    except:
                        error_data = {"raw_response": response.text}
                    
                    logger.log_authentication(
                        action="token_request",
                        success=False,
                        details={
                            "status_code": response.status_code,
                            "response_data": error_data,
                            "response_time_ms": response_time
                        }
                    )
                    
                    raise MpesaAuthenticationError(
                        message=f"Failed to get access token: {response.status_code}",
                        status_code=response.status_code,
                        response_data=error_data
                    )
        
        try:
            # Execute with retry logic
            return await execute_mpesa_with_retry(
                _fetch_token,
                retry_config=RetryConfig(
                    max_retries=2,  # Fewer retries for auth
                    base_delay=0.5,
                    max_delay=10.0,
                    strategy=RetryStrategy.EXPONENTIAL_BACKOFF
                )
            )
        
        except Exception as e:
            logger.error(
                "Failed to obtain M-Pesa access token after retries",
                exception=e,
                config_environment=self.config.environment
            )
            raise
    
    def _generate_password(self, timestamp: str) -> str:
        """Generate password for STK Push."""
        data = f"{self.config.shortcode}{self.config.passkey}{timestamp}"
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')
    
    async def stk_push(self, request: STKPushRequest) -> PaymentResponse:
        """Initiate STK Push payment with enhanced validation and error handling."""
        # Validate input data
        try:
            validated_data = MpesaInputValidator.validate_stk_push_request({
                "phone_number": request.phone_number,
                "amount": request.amount,
                "account_reference": request.account_reference,
                "transaction_desc": request.transaction_desc,
                "callback_url": request.callback_url
            })
        except MpesaValidationError as e:
            logger.log_validation(
                field_name=e.details.get("field", "unknown"),
                field_value=e.details.get("value", "unknown"),
                success=False,
                error_message=e.message
            )
            return PaymentResponse(
                success=False,
                message=f"Validation error: {e.message}",
                response_code=e.error_code.value
            )
        
        # Log transaction attempt
        transaction_id = f"STK_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        logger.log_transaction(
            transaction_type="STK_PUSH_INITIATED",
            transaction_id=transaction_id,
            phone_number=validated_data["phone_number"],
            amount=validated_data["amount"],
            status="pending"
        )
        
        async def _execute_stk_push():
            """Internal method to execute STK push with API call."""
            access_token = await self.get_access_token()
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            password = self._generate_password(timestamp)
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "BusinessShortCode": self.config.shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": validated_data["amount"],
                "PartyA": validated_data["phone_number"],
                "PartyB": self.config.shortcode,
                "PhoneNumber": validated_data["phone_number"],
                "CallBackURL": validated_data.get("callback_url") or self.config.callback_url,
                "AccountReference": validated_data["account_reference"],
                "TransactionDesc": validated_data["transaction_desc"],
                "CallBackMetadata": [
                    {"Key": "Amount", "Value": validated_data["amount"]},
                    {"Key": "AccountReference", "Value": validated_data["account_reference"]}
                ]
            }
            
            start_time = datetime.datetime.now()
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/mpesa/stkpush/v1/processrequest",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                response_time = (datetime.datetime.now() - start_time).total_seconds() * 1000
                
                # Log API call
                logger.log_api_call(
                    method="POST",
                    url=f"{self.base_url}/mpesa/stkpush/v1/processrequest",
                    status_code=response.status_code,
                    response_time_ms=response_time,
                    success=response.status_code == 200
                )
                
                response_data = response.json()
                
                if response.status_code == 200:
                    response_code = response_data.get("ResponseCode", "")
                    
                    if response_code == "0":  # Success
                        checkout_request_id = response_data.get("CheckoutRequestID")
                        merchant_request_id = response_data.get("MerchantRequestID")
                        
                        logger.log_transaction(
                            transaction_type="STK_PUSH_SUCCESS",
                            transaction_id=checkout_request_id,
                            phone_number=validated_data["phone_number"],
                            amount=validated_data["amount"],
                            status="initiated",
                            success=True
                        )
                        
                        return PaymentResponse(
                            success=True,
                            message="STK Push initiated successfully",
                            checkout_request_id=checkout_request_id,
                            merchant_request_id=merchant_request_id,
                            response_code=response_code,
                            response_description=response_data.get("ResponseDesc", "Success"),
                            customer_message=response_data.get("CustomerMessage", "Please enter your PIN")
                        )
                    else:
                        # Handle M-Pesa specific error codes
                        error_msg = response_data.get("ResponseDesc", "Unknown error")
                        
                        logger.log_transaction(
                            transaction_type="STK_PUSH_FAILED",
                            transaction_id=transaction_id,
                            phone_number=validated_data["phone_number"],
                            amount=validated_data["amount"],
                            status="failed",
                            success=False,
                            error_message=error_msg
                        )
                        
                        raise MpesaTransactionError(
                            message=f"STK Push failed: {error_msg}",
                            transaction_id=transaction_id,
                            response_code=response_code,
                            details=response_data
                        )
                else:
                    # Handle HTTP errors
                    error_data = {}
                    try:
                        error_data = response.json()
                    except:
                        error_data = {"raw_response": response.text}
                    
                    logger.log_transaction(
                        transaction_type="STK_PUSH_ERROR",
                        transaction_id=transaction_id,
                        phone_number=validated_data["phone_number"],
                        amount=validated_data["amount"],
                        status="error",
                        success=False,
                        error_message=f"HTTP {response.status_code}"
                    )
                    
                    raise MpesaAPIError(
                        message=f"STK Push API error: {response.status_code}",
                        status_code=response.status_code,
                        response_data=error_data
                    )
        
        try:
            # Execute with retry logic
            result = await execute_mpesa_with_retry(
                _execute_stk_push,
                retry_config=self.retry_config
            )
            
            logger.info(
                "STK Push completed successfully",
                transaction_id=transaction_id,
                checkout_request_id=result.checkout_request_id
            )
            
            return result
            
        except MpesaException as e:
            logger.error(
                "STK Push failed after retries",
                transaction_id=transaction_id,
                exception=e,
                phone_number=validated_data["phone_number"],
                amount=validated_data["amount"]
            )
            
            return PaymentResponse(
                success=False,
                message=e.message,
                response_code=e.error_code.value if hasattr(e, 'error_code') else "UNKNOWN"
            )
        except Exception as e:
            logger.error(
                "Unexpected error in STK Push",
                transaction_id=transaction_id,
                exception=e,
                phone_number=validated_data["phone_number"],
                amount=validated_data["amount"]
            )
            
            return PaymentResponse(
                success=False,
                message=f"Unexpected error: {str(e)}",
                response_code="UNKNOWN"
            )
    
    async def query_transaction_status(self, checkout_request_id: str) -> PaymentResponse:
        """Query STK Push transaction status."""
        try:
            access_token = await self.get_access_token()
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            password = self._generate_password(timestamp)
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "BusinessShortCode": self.config.shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_request_id,
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/mpesa/stkpushquery/v1/query",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                response_data = response.json()
                
                if response.status_code == 200:
                    response_code = response_data.get("ResponseCode", "")
                    
                    if response_code == "0":
                        result_code = response_data.get("ResultCode", "")
                        if result_code == "0":
                            return PaymentResponse(
                                success=True,
                                message="Transaction completed successfully",
                                response_code=result_code,
                                response_description=response_data.get("ResultDesc", "Success")
                            )
                        else:
                            return PaymentResponse(
                                success=False,
                                message=f"Transaction failed: {response_data.get('ResultDesc', 'Unknown error')}",
                                response_code=result_code,
                                response_description=response_data.get("ResultDesc")
                            )
                    else:
                        return PaymentResponse(
                            success=False,
                            message=f"Query failed: {response_data.get('ResponseDesc', 'Unknown error')}",
                            response_code=response_code,
                            response_description=response_data.get("ResponseDesc")
                        )
                else:
                    return PaymentResponse(
                        success=False,
                        message=f"API error: {response.status_code}",
                        response_code=str(response.status_code)
                    )
        
        except Exception as e:
            logger.error(f"Error querying transaction: {e}")
            return PaymentResponse(
                success=False,
                message=f"Query error: {str(e)}"
            )
    
    async def b2c_payment(self, phone_number: str, amount: int, remarks: str = "") -> PaymentResponse:
        """B2C payment (Disbursement)."""
        try:
            access_token = await self.get_access_token()
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            password = self._generate_password(timestamp)
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "InitiatorName": self.config.initiator_name,
                "SecurityCredential": password,
                "CommandID": "SalaryPayment",
                "Amount": amount,
                "PartyA": self.config.shortcode,
                "PartyB": phone_number,
                "Remarks": remarks,
                "QueueTimeOutURL": self.config.callback_url,
                "ResultURL": self.config.callback_url,
                "Occasion": ""
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/mpesa/b2c/v1/paymentrequest",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                response_data = response.json()
                
                if response.status_code == 200:
                    response_code = response_data.get("ResponseCode", "")
                    
                    if response_code == "0":
                        return PaymentResponse(
                            success=True,
                            message="B2C payment initiated successfully",
                            response_code=response_code,
                            response_description=response_data.get("ResponseDesc", "Success")
                        )
                    else:
                        return PaymentResponse(
                            success=False,
                            message=f"B2C payment failed: {response_data.get('ResponseDesc', 'Unknown error')}",
                            response_code=response_code,
                            response_description=response_data.get("ResponseDesc")
                        )
                else:
                    return PaymentResponse(
                        success=False,
                        message=f"API error: {response.status_code}",
                        response_code=str(response.status_code)
                    )
        
        except Exception as e:
            logger.error(f"Error in B2C payment: {e}")
            return PaymentResponse(
                success=False,
                message=f"B2C error: {str(e)}"
            )


# Global M-Pesa service instance (to be initialized with proper config)
mpesa_service: Optional[MpesaService] = None


def initialize_mpesa():
    """Initialize M-Pesa service with configuration."""
    global mpesa_service
    
    config = MpesaConfig(
        consumer_key=settings.MPESA_CONSUMER_KEY,
        consumer_secret=settings.MPESA_CONSUMER_SECRET,
        passkey=settings.MPESA_PASSKEY,
        shortcode=settings.MPESA_SHORTCODE,
        initiator_name=settings.MPESA_INITIATOR_NAME,
        callback_url=settings.MPESA_CALLBACK_URL,
        confirmation_url=settings.MPESA_CONFIRMATION_URL,
        validation_url=settings.MPESA_VALIDATION_URL,
        environment=settings.MPESA_ENVIRONMENT,
    )
    
    mpesa_service = MpesaService(config)
    logger.info("M-Pesa service initialized")
    return mpesa_service


async def get_mpesa_service() -> MpesaService:
    """Get or initialize M-Pesa service."""
    global mpesa_service
    if not mpesa_service:
        mpesa_service = initialize_mpesa()
    return mpesa_service
