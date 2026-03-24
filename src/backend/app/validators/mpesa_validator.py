"""
M-Pesa Input Validation

Comprehensive input validation for M-Pesa payment requests with detailed error messages.
"""

from __future__ import annotations

import re
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, validator, Field
from app.exceptions.mpesa_exceptions import MpesaValidationError, MpesaErrorCode


class MpesaInputValidator:
    """Validator for M-Pesa input data."""
    
    # Ethiopian phone number regex: 251XXXXXXXXX (12 digits starting with 251)
    ETHIOPIAN_PHONE_REGEX = re.compile(r'^251[0-9]{9}$')
    
    # Amount validation: 1-150,000 ETB
    MIN_AMOUNT = 1
    MAX_AMOUNT = 150000
    
    # Account reference validation: max 12 characters, alphanumeric
    ACCOUNT_REF_MAX_LENGTH = 12
    ACCOUNT_REF_REGEX = re.compile(r'^[a-zA-Z0-9_-]+$')
    
    # Transaction description validation: max 13 characters
    TRANSACTION_DESC_MAX_LENGTH = 13
    
    @staticmethod
    def validate_phone_number(phone_number: str) -> str:
        """
        Validate Ethiopian phone number format.
        
        Args:
            phone_number: Phone number to validate
            
        Returns:
            Normalized phone number
            
        Raises:
            MpesaValidationError: If phone number is invalid
        """
        if not phone_number:
            raise MpesaValidationError(
                message="Phone number is required",
                field="phone_number",
                value=phone_number,
                details={"requirement": "Ethiopian format: 251XXXXXXXXX"}
            )
        
        # Remove any spaces, dashes, or parentheses
        normalized = re.sub(r'[\s\-\(\)]', '', phone_number)
        
        # Check if starts with +251, convert to 251
        if normalized.startswith('+251'):
            normalized = '251' + normalized[4:]
        elif normalized.startswith('0'):
            normalized = '251' + normalized[1:]
        elif not normalized.startswith('251'):
            raise MpesaValidationError(
                message="Invalid phone number format",
                field="phone_number",
                value=phone_number,
                details={
                    "requirement": "Ethiopian format: 251XXXXXXXXX",
                    "examples": ["251712345678", "+251712345678", "0712345678"]
                }
            )
        
        # Validate format
        if not MpesaInputValidator.ETHIOPIAN_PHONE_REGEX.match(normalized):
            raise MpesaValidationError(
                message="Invalid phone number format",
                field="phone_number",
                value=phone_number,
                details={
                    "requirement": "Ethiopian format: 251XXXXXXXXX (12 digits)",
                    "normalized": normalized,
                    "pattern": "251 + 9 digits"
                }
            )
        
        return normalized
    
    @staticmethod
    def validate_amount(amount: int) -> int:
        """
        Validate payment amount.
        
        Args:
            amount: Amount to validate
            
        Returns:
            Validated amount
            
        Raises:
            MpesaValidationError: If amount is invalid
        """
        if not isinstance(amount, (int, float)):
            raise MpesaValidationError(
                message="Amount must be a number",
                field="amount",
                value=amount,
                details={"type": "number_required"}
            )
        
        amount_int = int(amount)
        
        if amount_int < MpesaInputValidator.MIN_AMOUNT:
            raise MpesaValidationError(
                message=f"Amount must be at least {MpesaInputValidator.MIN_AMOUNT} ETB",
                field="amount",
                value=amount_int,
                details={
                    "minimum": MpesaInputValidator.MIN_AMOUNT,
                    "currency": "ETB"
                }
            )
        
        if amount_int > MpesaInputValidator.MAX_AMOUNT:
            raise MpesaValidationError(
                message=f"Amount cannot exceed {MpesaInputValidator.MAX_AMOUNT} ETB",
                field="amount",
                value=amount_int,
                details={
                    "maximum": MpesaInputValidator.MAX_AMOUNT,
                    "currency": "ETB"
                }
            )
        
        return amount_int
    
    @staticmethod
    def validate_account_reference(account_reference: str) -> str:
        """
        Validate account reference.
        
        Args:
            account_reference: Account reference to validate
            
        Returns:
            Validated account reference
            
        Raises:
            MpesaValidationError: If account reference is invalid
        """
        if not account_reference:
            raise MpesaValidationError(
                message="Account reference is required",
                field="account_reference",
                value=account_reference,
                details={"max_length": MpesaInputValidator.ACCOUNT_REF_MAX_LENGTH}
            )
        
        if len(account_reference) > MpesaInputValidator.ACCOUNT_REF_MAX_LENGTH:
            raise MpesaValidationError(
                message=f"Account reference cannot exceed {MpesaInputValidator.ACCOUNT_REF_MAX_LENGTH} characters",
                field="account_reference",
                value=account_reference,
                details={
                    "max_length": MpesaInputValidator.ACCOUNT_REF_MAX_LENGTH,
                    "current_length": len(account_reference)
                }
            )
        
        if not MpesaInputValidator.ACCOUNT_REF_REGEX.match(account_reference):
            raise MpesaValidationError(
                message="Account reference can only contain letters, numbers, underscores, and hyphens",
                field="account_reference",
                value=account_reference,
                details={"allowed_chars": "a-z, A-Z, 0-9, _, -"}
            )
        
        return account_reference.strip()
    
    @staticmethod
    def validate_transaction_description(transaction_desc: str) -> str:
        """
        Validate transaction description.
        
        Args:
            transaction_desc: Transaction description to validate
            
        Returns:
            Validated transaction description
            
        Raises:
            MpesaValidationError: If transaction description is invalid
        """
        if not transaction_desc:
            raise MpesaValidationError(
                message="Transaction description is required",
                field="transaction_desc",
                value=transaction_desc,
                details={"max_length": MpesaInputValidator.TRANSACTION_DESC_MAX_LENGTH}
            )
        
        if len(transaction_desc) > MpesaInputValidator.TRANSACTION_DESC_MAX_LENGTH:
            raise MpesaValidationError(
                message=f"Transaction description cannot exceed {MpesaInputValidator.TRANSACTION_DESC_MAX_LENGTH} characters",
                field="transaction_desc",
                value=transaction_desc,
                details={
                    "max_length": MpesaInputValidator.TRANSACTION_DESC_MAX_LENGTH,
                    "current_length": len(transaction_desc)
                }
            )
        
        return transaction_desc.strip()
    
    @staticmethod
    def validate_checkout_request_id(checkout_request_id: str) -> str:
        """
        Validate checkout request ID.
        
        Args:
            checkout_request_id: Checkout request ID to validate
            
        Returns:
            Validated checkout request ID
            
        Raises:
            MpesaValidationError: If checkout request ID is invalid
        """
        if not checkout_request_id:
            raise MpesaValidationError(
                message="Checkout request ID is required",
                field="checkout_request_id",
                value=checkout_request_id
            )
        
        # Basic validation - should be a non-empty string
        if len(checkout_request_id.strip()) == 0:
            raise MpesaValidationError(
                message="Checkout request ID cannot be empty",
                field="checkout_request_id",
                value=checkout_request_id
            )
        
        return checkout_request_id.strip()
    
    @staticmethod
    def validate_stk_push_request(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate complete STK push request.
        
        Args:
            data: Request data to validate
            
        Returns:
            Validated request data
            
        Raises:
            MpesaValidationError: If any field is invalid
        """
        validated_data = {}
        
        # Validate phone number
        if "phone_number" in data:
            validated_data["phone_number"] = MpesaInputValidator.validate_phone_number(data["phone_number"])
        else:
            raise MpesaValidationError(
                message="Phone number is required",
                field="phone_number",
                value=None
            )
        
        # Validate amount
        if "amount" in data:
            validated_data["amount"] = MpesaInputValidator.validate_amount(data["amount"])
        else:
            raise MpesaValidationError(
                message="Amount is required",
                field="amount",
                value=None
            )
        
        # Validate account reference
        if "account_reference" in data:
            validated_data["account_reference"] = MpesaInputValidator.validate_account_reference(data["account_reference"])
        else:
            raise MpesaValidationError(
                message="Account reference is required",
                field="account_reference",
                value=None
            )
        
        # Validate transaction description
        if "transaction_desc" in data:
            validated_data["transaction_desc"] = MpesaInputValidator.validate_transaction_description(data["transaction_desc"])
        else:
            raise MpesaValidationError(
                message="Transaction description is required",
                field="transaction_desc",
                value=None
            )
        
        # Optional callback URL
        if "callback_url" in data and data["callback_url"]:
            validated_data["callback_url"] = data["callback_url"].strip()
        
        return validated_data


class ValidatedSTKPushRequest(BaseModel):
    """Pydantic model for validated STK push request."""
    
    phone_number: str = Field(..., description="Ethiopian phone number (251XXXXXXXXX)")
    amount: int = Field(..., ge=1, le=150000, description="Amount in ETB (1-150,000)")
    account_reference: str = Field(..., max_length=12, description="Account reference")
    transaction_desc: str = Field(..., max_length=13, description="Transaction description")
    callback_url: Optional[str] = Field(None, description="Callback URL")
    
    @validator('phone_number')
    def validate_phone_format(cls, v):
        if not MpesaInputValidator.ETHIOPIAN_PHONE_REGEX.match(v):
            raise ValueError("Invalid Ethiopian phone number format. Use 251XXXXXXXXX")
        return v
    
    @validator('account_reference')
    def validate_account_ref_format(cls, v):
        if not MpesaInputValidator.ACCOUNT_REF_REGEX.match(v):
            raise ValueError("Account reference can only contain letters, numbers, underscores, and hyphens")
        return v.strip()


class ValidatedTransactionStatusRequest(BaseModel):
    """Pydantic model for validated transaction status request."""
    
    checkout_request_id: str = Field(..., description="Checkout request ID")
    
    @validator('checkout_request_id')
    def validate_checkout_id(cls, v):
        if len(v.strip()) == 0:
            raise ValueError("Checkout request ID cannot be empty")
        return v.strip()


class ValidatedB2CPaymentRequest(BaseModel):
    """Pydantic model for validated B2C payment request."""
    
    phone_number: str = Field(..., description="Ethiopian phone number (251XXXXXXXXX)")
    amount: int = Field(..., ge=1, le=150000, description="Amount in ETB (1-150,000)")
    remarks: str = Field("", max_length=100, description="Payment remarks")
    command_id: str = Field("SalaryPayment", description="Command ID")
    occasion: str = Field("", max_length=100, description="Payment occasion")
    
    @validator('phone_number')
    def validate_phone_format(cls, v):
        if not MpesaInputValidator.ETHIOPIAN_PHONE_REGEX.match(v):
            raise ValueError("Invalid Ethiopian phone number format. Use 251XXXXXXXXX")
        return v
